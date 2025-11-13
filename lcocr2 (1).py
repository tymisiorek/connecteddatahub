import os
import json
import pandas as pd
import numpy as np

import ollama
from openai import OpenAI
from ocrmac import ocrmac

import re
import unicodedata
from unidecode import  unidecode
from nameparser import HumanName

from sklearn.neighbors import NearestNeighbors
from scipy.sparse.csgraph import connected_components

def ocrmac2text(mactext, col_break = 0.5):
	"""
	(text, confidence, (x, y, width, height))
	The bounding box (x, y, width, height) is composed of numbers between 0 and 1,
		that represent a percentage from total image (width, height) accordingly.
		
	"""
	macocrcols = ['Text', 'Confidence', 'X', 'Y', 'Width', 'Height']
	textdf = pd.DataFrame([[line[0],line[1]]+[line[2][i] for i in range(4)] for line in mactext], columns=macocrcols)
	
	column_break_point = get_column_break(textdf, col_break)

	textdf['Column'] = np.where(textdf.X <= column_break_point, 0, 1)

	textdf['Line'] = textdf.groupby('Column', group_keys=False)['Y'].transform(get_line_labels)

	textdf.sort_values(by=['Column', 'Line', 'X'], ascending=[False, True, True], inplace=True)

	return ["\n".join(textdf[textdf['Column'] == icol]['Text'].values) for icol in range(2)]

def get_column_break(textdf, col_break=0.5):
	boxpoints = textdf[['X', 'Y']].values

	# get the connected components from the nearest neighbor graph
	nbrs = NearestNeighbors(radius=0.1).fit(boxpoints)
	connectgraph = nbrs.radius_neighbors_graph(boxpoints, radius=0.05)
	n_components, labels = connected_components(connectgraph, directed=False, return_labels=True)

	check_break = True
	column_break_point = col_break

	while check_break:
		check_break = False

		for c in range(n_components):
			csize = np.sum(labels == c)
			x = boxpoints[labels == c][:,0]
			# if the connected component crosses the breakpoint 
			if csize > 3 and column_break_point > np.min(x) and column_break_point < np.max(x):
				column_break_point = 0.99*np.min(x)
				if column_break_point < 0.3:
					raise AttributeError("Page is too rotated: " + str(column_break_point))
				check_break = True

	return column_break_point

def get_line_labels(coldf):
    col_ypts = coldf.values.reshape(-1, 1)
    nbrs = NearestNeighbors(radius=0.01).fit(col_ypts)
    connectgraph = nbrs.radius_neighbors_graph(col_ypts, radius=0.005)
    n_components, line_labels = connected_components(connectgraph, directed=False, return_labels=True)
    return line_labels
	

def strip_accents(text):
	try:
		text = unicode(text, 'utf-8')
	except (TypeError, NameError): # unicode is a default on python 3
		pass
	text = unicodedata.normalize('NFD', text)
	text = text.encode('ascii', 'ignore')
	text = text.decode("utf-8")
	return str(text)

def strip_punct(name, remove_parentheses=True):

    if remove_parentheses:
        name = re.sub("[\(\[].*?[\)\]]", "", name) # remove text between () and []
        if '(' in name:
            name=name[:name.index('(')]
        for c in [')', ']','.']:
            name=name.replace(c, '')
    for c in [',', ' - ', '- ', ' -']:
        name=name.replace(c, '-')
    name = name.replace(' & ', '&')
    return name.strip()

def clean_name(name_text):
    name = HumanName(name_text)
    if len(strip_punct(name.first).strip()) < 2:
        return " ".join([name.first, name.middle, name.last])
    else:
        return " ".join([name.first, name.last])

def clean_ocr_text(text, main_institutions=[], phrases2remove=[]):
	
	for phrase in phrases2remove:
		text = text.replace(phrase, '')
	text = strip_accents(text)
	for p in ['...','...','...', '..', ' . ', '..', '.\n']:
		text = text.replace(p, '')
	linetext=[]
	for s in text.splitlines():
		if s.strip() in main_institutions:
			linetext.append('\n')
			linetext.append(s)
		elif s:
			linetext.append(s)
	text = os.linesep.join(linetext)
	return text

def list_remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
    
def model_response2df(response):
	content = response['message']['content']
	if "None," in content or "None\n" in content:
		content = content.replace("None", """ "None" """)
	df = pd.DataFrame(json.loads(content))
	return df

def clean_institution_name(name):
    for s2space in [' – ',' - ', '–', '-','   ', '  ']:
        name = name.replace(s2space, ' ')
    for s2remove in ['.', ',', 'The ', "'", '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        name= name.replace(s2remove, '')
    for miss, corr in [('Universite', 'University'), ('Colege', 'College')]:
        name = name.replace(miss, corr)
    return name.strip().title()

bold_prompt_old = """You are part of a data processing pipeline. Your task is to identify the primary 
institutions mentioned in the 'page text' and return a list. Only list the primary institution names with no additional 
annotations or explanations, or it will break the process.  

The only valid primary insitutions are from this list: {}.

Sometimes no primary institutions are mentioned in the page text, in which case you should return an empty list.

The primary insitutions always appear on a line by itself, and the next line is their address often followed by history and enrollment.
Do not include the institution if it is preceeded by 'Affiliation:''.
Do not include the institution if it is preceeded by 'Education:'.
Do not include the institution if it is preceeded by 'Career:'.

Do not say 'Here is the list of primary institutions'.

The page text: {}

The primary institutions mentioned in the page text:
"""
bold_prompt = """You are part of a data processing pipeline. 

Your task is to identify the primary institutions mentioned in the 'text excerpt' and return a list separated by newlines '\n'. 

Only list the primary institution names with no additional annotations or explanations, or it will break the process.  

The primary insitution is always identified by a Heading Section which contains the primary institution name, followed by the address and telephone.
Other information in the heading section often includes 'History:', 'Enrollment:', 'Faculty:', 'Year Founded', 'Fax', and 'Internet'
The primary institution almost always contains 'University' or 'College' in the name.

The text excerpt may not contain a Heading Section and therefore not mention a primary institution name, in which case you should return an empty list.
The text excerpt may contain up to two primary institution names.  

The first person following the name of a primary institution is the President or Chancellor.

There are other many instutions mentioned in the text excerpt related to the education of individual people, but these are not the primary insitutions!
Do not include the institution if it is in a 'Affiliation', 'Education', 'Career' or 'Employment' section.
Do not include the institution if it has an acronym (for example NYU, CUNY, MIT, SUNY).
Again, DO NOT include an institution if it is related to a specific person.

Do not say 'Here is the list of primary institutions'.

EXAMPLES
These are examples of potential solutions.  Do not consider these when 

1) The text excerpt:
"Adelphi University
1 South Avenue, Garden City, NY 11530-7000
Tel: (516) 877-3000 Fax: (516) 877-3805 Internet: www.adelphi.edu
Enrollment: Over 8,000 Faculty: Over 700 Year Founded: 1896
Robert Allyn Scott
President"

The primary institution list: Adelphi University\n

2) The text excerpt:
"Robert Allyn Scott
President
Education: Bucknell BA; Cornell 1976 PhD
Career: Associate Dean and Senior Administrator,
College of Arts and Sciences, Cornell University;
President and Chief Executive Officer, Ramapo

Dean, Derner Institute of Advanced Psychological
Studies Jean Lau Chin
.. (516) 877-4800
E-mail: chin@adelphi.edu
Education: Brooklyn BS; Columbia 1976 MD, EdD"

The primary institution is: EMPTY
Explaination: the text does not contain a heading section

3) The text excerpt:
"Harrold D. Owen . . . . . . . . . . . . . . ...
.. Senior Board Trustee
Affiliation: Owner, Owen Oil Tools, Inc.
Fort Worth, TX
H. Lynn Packer
. Trustee
Dallas, TX
Hubert Pickett, Jr..
... . . . ..
Assistant Secretary
Affiliation: Principal, Jefferson Middle School
Tel: (915) 677-3505
Ted Poe... . . . ... ........
.. ... Trustee
Affiliation: Judge, 228th State District Court
Houston, TX
Tel: (713) 755-6650"

The primary institution is: EMPTY
Explaination: the text does not contain a heading section

4) The text excerpt:
"Case Western Reserve University
159
Case Western Reserve
University
10900 Euclid Avenue, Cleveland, OH 44106
Tel: (216) 368-2000
Internet: http://www.cwru.edu
Enrollment: Over 9,900 Faculty: Over 1,900 Year Founded: 1826
Administration
COLLEGES AND UNIVERSITIES
President Agnar Pytte*
... (216) 368-4344"

The primary institution list: Case Western Reserve University\n


5) The text excerpt:
"California Polytechnic State University, San
Luis Obispo
San Luis Obispo, CA 93407
Tel: (805) 756-1111
Enrollment: Over 17,000 Faculty: Over 850
President Warren J. Baker
.... (805) 756-6000
Fax: (805) 756-1129
Executive Assistant Daniel Howard-Greene
.. (805) 756-6000
E-mail: dhgreene@calpoly.edu
California State Polytechnic University,
Pomona
3801 West Temple Avenue, Pomona, CA 91768
Tel: (909) 869-7659
Internet: http://www.csupomona.edu
Enrollment: Over 16,000 Faculty: Over 950 Year Founded: 1938
President Bob H. Suzuki ......
. (909) 869-2290
Education: UC Berkeley 1960 BS;
Cal Tech 1962 MS, 1967 PhD
Executive Assistant Anita R. Martin..
..(909) 869-2286"

The primary institution list: California Polytechnic State University, SanLuis Obispo\n California State Polytechnic University,Pomona

So again, use the following text excerpt (disregard text in the above Examples) and return the list of primary institutions found in Heading Sections, or an empty list.
The most often response is an empty list.

Correct the error that an institution is included from a specific person's Affiliation information.

The text excerpt: {}

The list of primary institutions mentioned in the text excerpt:
"""
def get_bolded_institutions(col_text, master_institutions):
    
    #specific_prompt = bold_prompt.format(focus_institutes, col_text)
    specific_prompt = bold_prompt.format(col_text)
    response = ollama.chat(model='llama3:instruct', options = {'temperature': 0 }, 
                           messages=[{'role': 'user', 'content': specific_prompt}])
    
    main_institutions = response['message']['content'].replace('[', '').replace(']', '').split("\n")
    main_institutions = [strip_accents(s).replace('"','').replace("'","").strip() for s in main_institutions]
    main_institutions = [clean_institution_name(s) for s in main_institutions]
    main_institutions = [s for s in main_institutions if s != 'Empty' and s!='None' and len(s) > 0 and s in master_institutions]

    return main_institutions


structure_prompt_llama = """Your task is to parse the data into a JSON format list, with no additional annotations or explanations. 
Do not say 'Here is the parsed JSON list'.  Only return a valid JSON list without extra spaces.

Organize the raw text into a JSON with the following fields: 
- Name: the person's name (if Vacant put "Vacant") including prefixes and suffixes
- Position: the person's position including prefixes and specific positions
- Institution: The Institution should only be from this list: {}.  The Institution maintains consistency, altering only once or twice when the Institution name explicitly appears and applying to all later entries.
- SubInstitution: When the Position is Dean or Associate Dean or related to a university foundation, include the school, college or foundation otherwise do not include
- Education: if mentioned, text following the phrase "Education" otherwise do not include
- Other Affiliation: if mentioned, text following the phrase "Career" or "Affiliation" but not the current institution or subinstitution

Create a new row for each name that is extracted.  It is very important that you include every name in the JSON.

The Position usually appears before the Name when the Name is near a phone number or email, otherwise it is after the Name.

The Position and Name fields are never empty. 

Here is the raw text to parse:
{}

Here is the parsed JSON list:"""
def get_leadership_data_llama(institute_list, text):
	response = ollama.chat(model='llama3:instruct', options = {'temperature': 0 }, messages=[{'role': 'user', 'content': structure_prompt_llama.format(",".join(institute_list), text)}])
	return  model_response2df(response)

structure_prompt_gpt = """Your task is to parse the data into a JSON format list, with no additional annotations or explanations. 
Do not say 'Here is the parsed JSON list'.  Only return a valid JSON list without extra spaces.

Organize the raw text into a JSON with only the following fields (no others): 
- Name: the person's name (if Vacant put "Vacant") including prefixes and suffixes and titles
- Position: the person's position including prefixes and specific functions
- Institution: The Institution should {}.  The Institution maintains consistency, altering only once or twice when the Institution name explicitly appears and applying to all later entries. If you are not certain, put None.
- SubInstitution: If the Position is Dean or Associate Dean, include the school or college.  If the position is associated with a Foundation, include the foudation. otherwise do not include
- Education: if mentioned, text following the phrase "Education" otherwise do not include
- Other Affiliation: if mentioned, text following the phrase "Career" or "Affiliation" but not the institution or subinstitution or notes

Create a new row for each name or position that is extracted.  It is very important that you include every name and position in the JSON.

When the Position is vacant, include the Position and use Vacant for the Name.

The Position and Name fields are never empty. Do not include the Position in the Name.
Correct the labeling error where the Position appears in the Name. 

The Position usually appears before the Name when the Name is near a phone number or email, otherwise the Position usually appears after the Name.

The Education and Other Affiliation always appear after the Name.

Correct the labeling error where a school or college mentioned for a dean is incorrectly labeled as the Institution rather than the SubInstitution.  
The Board of Trustees is not an Insitution, keep using the previous Institution.

Here is the raw text to parse:
{}

Here is the parsed JSON list:"""
def get_leadership_data_gpt(institute_list, text, oai_key="",print_output=False):
	gpt_client = OpenAI(api_key=oai_key)

	if len(institute_list) > 0:
		institute_text = "only be from this list: {} or None".format(", ".join(institute_list))
	else:
		institute_text = "just be None.  No primary instutions appear on this page"

	completion = gpt_client.chat.completions.create(
		model= "gpt-4o-mini", #"gpt-3.5-turbo", #gpt-4o-mini
		messages=[{"role": "system", "content": structure_prompt_gpt.format(institute_text, text)}], 
		temperature = 0.0)
	gpt_output = completion.choices[0].message.content
	gpt_output = gpt_output.replace(' None', ' "None"')
	gpt_output = gpt_output.replace(' null', ' "None"')
	if print_output:
		print(gpt_output)
	return pd.DataFrame(json.loads(gpt_output))


