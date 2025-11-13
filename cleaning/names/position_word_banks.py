from collections import defaultdict

'''Word Banks'''
PRESIDENT_WORDS = ["president", "chancellor", "superintendent", "commissioner", "officer-in-charge"]
BOARD_WORDS = ["Trustee", "Regent", "Member", "Fellow", "Overseer", "Governor", "Curator", "Visitor", "Manager"]
POSITION_BANK = ["President", "Chancellor", "Provost", "Director", "Dean", "Controller", "Trustee", "Member", "Regent", "Chairman", "Overseer", "Assistant", "Librarian", "Secretary", 
                "Chaplain", "Minister", "Treasurer", "Senior Counsel", "General Counsel", "Legal Counsel", "University Counsel", "College Counsel", "Special Counsel", "Corporation Counsel", 
                "Corporate Counsel", "Officer", "Chief", "Professor", "Commissioner", "Fellow", "Chairperson", "Manager", "Clergy", "Coordinator", "Auditor", "Governor", "Representative", 
                "Stockbroker", "Advisor", "Commandant", "Rector", "Attorney", "Curator", "Clerk", "Department Head", "Pastor", "Head", "Comptroller", "Deputy", "Inspector General", 
                "Instructor", "Registrar", "Ombuds", "Administrator", "Liaison", "Administrative Associate", "Webmaster", "Specialist", "University Planner", "Architect", "Counselor"]

PROVOST_WORDS = ["provost", "campus provost", "university provost", "executive provost", "provost of the university", "the provost"]

ADMINISTRATION_WORDS = ["academic service", "academics", "academic program", "admissions", "admission", "enrollment service", "student life", "housing", "academic support", "advising", "enrollment management", 
                       "student relations", "academic computing", "academic records", "student service", "student affairs", "student development", "registrar", "financial aid", "media service", "library service", "university librar"]

DESIG_ORDER = ['SubInstitution', 'Administration', 'Finance',  'Satellite Campus',
'Student Affairs', 'Academic Affairs', 'Religion', 'Athletics', 'External Relations',
'Continued Studies', 'Faculty Affairs',
'Board', 'Operations', 'Health Affairs', 'Human Resources', 'Information Systems',
'Library','Advancement Foundation', 'Research' , 'DEI', 'Graduate']


DESIGNATION_KEYWORDS = {
    # "arts and science", "institute",
    "SubInstitution": ["the college", "the arts", "interdisciplinary studies", "life sciences", "agriculture",  "space institute",
                        "agricultural", "liberal arts", "engineering", "law center",  "deaf education center", "informatics center",
                        "institute relations", "dallas center", "arts and sciences", "arts and science", "institute for the deaf", "museum affairs",
                        "institute affairs", "science and technology", "arts, sciences and technology", "global studies"],

    "Administration": ["vice president, administration", "and administration", "administrative",  "legal affairs", "legal services", "institutional affairs", "university affairs", 
                       "employment service", "vice president, quality", "management service", "university compliance" "university operation", "institutional services", "general administration",
                       "of the corporation", "university governance", "materials management", "executive affair"," university operation", "vice president, administration", "institutional compliance",
                       "management and services", "university secretary", "vice president, services", "organizational effectiveness", "strategic management", "regulatory affairs",
                        "general services", "presidentpresidential initiatives", "counsel", "chancellor, administration", "president, administration", "dean, administration",
                       # Planning
                       "assessment", "evaluation", "planner", "special projects", "strategy and measurement", "institutional effectiveness", "presidential initiative", "capital improvement", "strategy and policy",
                 "university projects", "institutional analysis", "commercialization strategies",  "strategic affair", "university initiative", "program development", "strategic initiative", "strategic development",
                 "strategic and", "strategy", "strategic relations", "strategic enterprises", "special program", "economic initiative", "creative services", "university planer",
                 "long-range planning", "vice president, planning", "strategic planning and initiatives", "planning and policy",
                 "planning and institutional improvement", "strategic planning", "university planning and analysis", "campus planning",
                 "institutional planning and effectiveness", "vice chancellor, planning", "institutional planning", "planning and management",
                 "planning, organization development", "policy and planning", "ethics and compliance"],

                       # Finance?
    "Finance" :       ["budget", "finance", "financial", "procurement", "accounting", "marketing", "endowment",  "investment", "business", "fiscal", "and resource management", "institutional resources", "treasury management", "university resources", "audit", ", resource management",
                    "commerce", "asset management", "budgetary affairs", "budgetary initiative", "budgeting and management", "treasury and cash management",
                     "treasury", "purchasing", "cost management", "budgeting", "bursar", "health economics", "controller's office", "audit and compliance",
                     "budgetary administration", "risk and compliance", "chancellor, compliance"],
                      

    "Board": ["of the board", "board of", "board operation", "trustee", "trusted"],
    "Operations": ["sustainability", "facilities", "campus operations", "infrastructure", "environmental", "security", "campus police", "emergency management", "safety", 
                          "campus services", "university services", "facility operation", "university architect", "land, buildings and real estate", "auxiliary", "capital construction",
                          "property management", "plant operations", "construction", "campus residence", "physical resources", "university compliance", "physical plant", "facilities",
                          "land and building", "facility management", "division operations", "plant and operation", "operations and quality", "emergency preparedness",
                          "real estate operation", "real estate", "police services", "energy and the environment", "vice president, operations", "real properties",
                          "vice chancellor, operations", "capital planning and project management", "campus planning and operations", "campus, planning and operations"],

    "Health Affairs": ["health service", "health affair", "ambulatory", "clinical service", "cancer", "patient care", "diagnostic service", "physician",
               "clinical", "care contracting", "outpatient", "patient service", "medical affair", "health system affair", "surgical service", "health system",
               "community health", "health policy", "health science", "medical campus", "health solution", "rural health", "usf health", "health afair",
               "vice president, health", "vice presidentmedical sciences", "vice presidentmedical affairs", "commonwealth medicine", "healthcare affairs",
               "personalized medicine", "us health", "managed care", "hospital affairs", "nursing affairs", "university hospital", "vice president, nursing",
               "hospital systems", "umass biologics"],


    "Academic Affairs": ["provost, academic", "vice provost, education", "undergraduate education", "curriculum", "provost" "undergraduate studies", "instruction", "academic program", "academic development", "academic initiative",
                         "education affair", "undergraduate affair", "academie affairs", "educational and", "teacher education", "experiential education", "academic affair", "academic administration",
                         "undergraduate initiative", "cooperative education", "school program", "interdisciplinary education", "educational outreach", "educational,", "undergraduate studies", "educational affair",
                         "academic service", "academic afair", "academic affair", "educational resource", "academic enrichment", "academic resource", "university studies", "vice president, academics", "academic operation",
                         "educational development", "academic issues", "academic planning", "career development", "academic resources", "academic vice president", "undergraduate program",
                         "main campus", "advances in learning", "teaching and learning", "instructional affair", "academic opportunity", "interdisciplinary affair", "interdisciplinary and cross-campus affair",
                         "vice chancellor, academ", "president, academics", "acacemic affairs", "vice chancellor, academic", "vice president, education", "health education programs",
                         "residential education", "vice presidentacademic affairs", "academic technologies", "academic and instructional services", "learning technologies",
                         "international and area studies", "marine sciences", "unit development", "knowledge development", "aviation programs", "learning innovation",
                         "educational technology", "learning technology", "academic and enrollment services", "academic programs",
                         "undergraduate academic affairs", "undergraduate academics"],

    "Faculty Affairs": ["faculty", "faculty affair", "staff relations", "vice president, faculty", "faculty development", "faculty and staff", "faculty advancement", "research and faculty development",
                        "academic personnel"],

    "Research": ["innovation", "research", "grants", "publication", "biotechnology", "scientific", "sponsored programs", "entrepreneurship", "center for commercialization",
                "translational bioscience", "researcn", "institutional research and assessment", "research and development", "technology transfer"],
    

    "Student Affairs": ["student", "student life", "student service", "support", "wellbeing", "well-being", "campus life", "housing", "counseling", "student affairs", "student initiative", "student service", 
                        "student success", "student activities", "student development", "students", "university life", "student learning", "residence life", "student and community",
                        "career service", "student judicial service", "advisement", "student access", "study abroad", "dining program", "academic life", "university and community life",
                        "career center", "residential services", "academic support and retention", "career counseling and planning center", "family center",
                        "student financial services", "undergraduate studies and student support services", "student financial services",
                        "student life and dean of students", "residential life", "freshman studies", "first year of studies", "freshman",
                        "academic success center"
                        #enrollment?
                        "enrollment", "financial aid", "retention", "registrar", "admission", "enrolment", "admissions", "records", "academic records",
                        "academic records and institutional research", "admissions and orientation", "college enrollment", "enrollment management", "enrollment services",
                         "undergraduate admissions", "graduate admissions", "admissions and financial aid", "university admissions", "college admissions and financial aid",
                         "admissions and records", "university admissions", "college admissions and financial aid", "enrollment and student success",
                         "admissions and enrollment development", "enrollment and dean", "enrollment and dean admission", "student affairs and enrollment services",
                         "enrollment and retention", "undergraduate admission"],
    

    "Information Systems": ["information", "data management", "computer", "computing", "network service", "internet service", "electronic marketing", "converging technologies",
                    "technical service", "vice president, systems", "enterprise system", "system administration", "network telecommunications",
                    "web con", "enterprise operations", "enterprise development", "technology development", "vice chancellor, technology", "vice president, technology",
                    "technology services", "enterprise technology"],


    "DEI": ["diversity", "equity", "inclusion", "affirmative action", "dei", "multicultural affairs", "equal opportunity", "minority affair", "intercultural affair",
                "inclusive excellence", "cultural affair", "civil rights and title ix", "social justice", "social responsibility", "intercultural relations",
                "community education and diversity affairs", "diversity and inclusion"],
    "External Relations": [ "external", "university relation", "college relation", "public relation", "communications", "public affair", "media", 
                            "international", "federal relations", "public events", "institutional relation", "institutional study", "community partnerships",
                           "state relations", "community engagement", "community affair", "civic engagement", "community relation", "corporate relation", 
                           "foundation relation", "legislative", "policy affairs", "defense relation", "constituent relations", "regional affair", "system relation", "regional operation",
                           "federal program", "agency relation", "regional engagement", "communication", "news services", "federal affair", "commonwealth relation", "state affair",  "community services",
                           "intercampus", "urban affairs", "public service", "school relation", "public policy", "district of columbia affair", "d,c, affair", "vice president, engagement", "vice president, policy", 
                           "community development", "silicon valley initiative", "system affair", "globalization", "community initiative", "community and native", "corporate function",
                           "tribal relation", "university spokesperson", "brand integration", "us world", "p-16 initiatives", "television", "media relations",
                           "international programs", "international programs", "vice president, relations", "brand development", "global initiatives", "global affairs",
                           "off-campus programs", "corporate affairs", "global and strategic partnerships", "international and border programs",
                           "international services and programs"],


    #"Planning": ["],
    #"Finance": ["budget", "finance", "financial", "accounting", "marketing", "endowment",  "investment", "business", "fiscal", "and resource management", "institutional resources", "treasury management", "university resources", "audit", ", resource management",
    #            "commerce", "asset management", "budgetary affairs", "budgetary initiative", "budgeting and management", "treasury and cash management",
    #            "treasury", "purchasing", "cost management", "budgeting", "bursar"],
    "Advancement Foundation": ["fundraise", "fundraising", "alumni", "donation", "parent relation", "annual giving", "special events", "principal gifts", "major gift", "campaigns", 
                    "planned giving", "leadership gifts", "gift program", "trusts and estate", "giving", "philanthropy", "constituent program", "institutional advancement", "vice president, advancement", "vice president, development",
                    "university advancement", "university development", "vice president, development", "vice president, advancement", "economic advancement", "economic development",
                    "college advancement", "institute advancement", "and advancement", "resource development", "institutional advancement", "sponsored funds", "college development", "wide advancement", "institution advancement",
                    "regional development", "planned gift", "foundation", "university advancementnorthern", "vice presidentdevelopment", "university advacement",
                    "alumni house", "alumni services", "advancement services", "development and alumn relations", "vice chancellor, development", "vice president, development",
                    "central development", "strategic donor engagement", "presidentuniversity advancement", "chancellor, advancement", "chancellor development",
                    "president,development affairs", "campus advancement", "chancellor, engagement", "gift planning", "economic engagement", "university engagement",
                    ],
    "Human Resources": ["hr", "human resource", "recruitment", "employee relations", "union", "collective bargaining", "labor", "human relations", "human capital", "personnel", "human and", "professional development", "human service", "hiring",
                        "workforce", "employees service", "talent and culture", "talent development", "human, resources"],
    

    "Religion": ["ministry", "mission", "ministries", "church", "religious", "religion", "spiritual", "christian development", "university ministries",
                "chapel"],
    "Satellite Campus": ["satellite campus", "downtown", "at the west campus", "at the tempe campus", "at the downtown phoenix campus", "brooklyn campus",
                            "carlsbad campus", "frost campus", "extended campus", "tri-campus", "regional campuses", "madrid campus", "community college",
                            "university at riverhead", "west campus", "avery point campus", "stamford campus", "brentwood campus", "extension$", "houston center",
                            "daytona beach", "brookhaven affair", "davie campuses", "fort worth campus", "nyc tech campus", "vice president - atlanta",
                            "gulf park campus", "college at wise", "senior vice president, atlanta", "polytechnic campus", "osu-okmulgee",
                            "osu-oklahoma city", "osu-cascades campus"],
    "Athletics": ["athletic", "sports"],

}

DEAN_KEYWORDS = {
   #"SubInstitution":  ["Arts and Sciences", "Engineering", "Applied Science", "Computer Science", "Data Science", "Technology", "Information", "Architecture", "Behavioral Science", "arts",
   #                     "Social Sciences", "Natural Sciences", "Environmental and Earth Science", "Marine Science", "Business", "Hospitality", "Criminal Justice", "Law", "Policy and Affairs", 
   #                     "Agriculture", "Family and Consumer Science", "Culinary", "Journalism", "Communication", "Liberal Arts", "Humanities", "Fine Arts", "Language and Culture", "Nursing", "Physical Therapy and Nutrition", 
   #                     "Pharmacy", "Dentistry", "Optometry", "Veterinary", "Audiology", "Gerontology", "Pathology", "Social Work", "Continued Studies", "Professional Studies", "Honor College", "Hospital",
   #                     "dallas center", "museum affairs", "umass biologics"],
    "Administration": ["vice president, administration", "legal affairs", "legal services", "institutional affairs", "university affairs", 
                       "employment service", "vice president, quality", "management service", "university compliance" "university operation", "institutional services",
                       "of the corporation", "university governance", "materials management", "executive affair"," university operation", "vice president, administration",
                        "campus relations", "change management", "governance and risk", "risk management", "administratior",
                       "institutional integrity", "executive operations", "vice chancellor, management", "corporation affairs and governance",
                       "administrative services"],
    "Board": ["of the board", "board of", "board operation", "board relations", "and trusted", "and trustee"],
    "Operations": ["sustainability", "facilities", "campus operations", "infrastructure", "environmental", "security", "campus police", "emergency management", "safety", 
                          "campus services", "university services", "facility operation", "university architect", "land, buildings and real estate", "auxiliary", "capital construction",
                          "property management", "plant operations", "construction", "campus residence", "physical resources", "university compliance", "physical plant", "campus involvement",
                          "land grant affair", "process management", "operative services", "events and venues", "university operations", "plant management",
                          "space management", "facility services", "campus affair", "facility planning and operations"],
    "Health Affairs": ["health science", "public health", "health profession", "college of health", "school of health", "biomedical science", "and health", "allied health", "physical education",
                        "health and", "health studies", "genome", "medical", "pharmacy", "surgeons", "school of medicine", "college of medicine", "podiatric medicine", "osteopathic medicine",
                        "health care service", "presidentpatient care services", "vice president, medicine", "pediatric services", "biomedical informatics",
                        "children's services", "rehabilitation services"],

    "Library": ["library", "university library", "university libraries", "libraries", "library affair", "scholarly resources"],

    "Academic Affairs": ["undergraduate education", "curriculum", "provost" "undergraduate studies", "instruction", "academic program", "academic development",
                         "education affair", "undergraduate affair", "academie affairs", "educational and", "teacher education", "experiential education", "academic affair", "academic administration",
                         "undergraduate initiative", "cooperative education", "school program", "interdisciplinary education", "educational outreach", "educational,", "undergraduate studies", "educational affair",
                         "academic service", "academic afair", "educational resource", "academic enrichment", "academic resource", "university studies", "vice president, academics", "academic operation",
                         "educational development", "academic issues", "academic planning", "academic department", "academic initiative", "academic effectiveness", "learning and pedagogy", "learning enhancement",
                         "curricular affair", "academic relation", "academic policies", "academic aflairs", "academic affiars", "education policy", "school services",
                         "vice president, education", "dean's office", "vice president, academic", "academic programming", "legal education",
                         "pre-college programs", "weather and climate programs", "school and university programs", "learning innovation"], 
    "Faculty Affairs": ["faculty", "staff relations", "faculties", "college faculty"],
    "Research": ["research", "grants", "publication", "biotechnology", "scientific", "sponsored programs", "basic science",
                "marine program", "scholarship", "basic sciences", "laboratory management", "molecular medicine and genetics",
                "venture and commercialization", "laboratory affairs", "commercialization", "national laboratories", "research administration",
                "research conduct and compliance", "grants and contracts"],
    

    "Student Affairs": ["student", "student life", "student service", "support", "wellbeing", "well-being", "campus life", "housing", "counseling", "student affairs", "student initiative", "student service", 
                        "student success", "student activities", "student development", "students", "university life", "student learning", "residence life", "student and community",
                        "career service", "student judicial service", "advisement", "student access", "study abroad", "dining program", "academic life", "freshmen", "freshman",
                        "career and protective services"],
    #"Enrollment": ["enrollment", "financial aid", "retention", "registrar", "admission", "enrolment", "graduate admissions"],


    "DEI": ["diversity", "equity", "inclusion", "affirmative action", "dei", "multicultural affairs", "equal opportunity", "minority affair", "intercultural affair", "women's issues",
            "muticultural affair", "multicultural awareness"],
    "External Relations": [ "external", "university relation", "college relation", "public relation", "communications", "public affair", "media",
                            "international",  "federal relations", "public events", "institutional relation", "government relations",
                            "government affairs",
                           "state relations", "community engagement", "community affair", "civic engagement", "community relation", "corporate relation", 
                           "foundation relation", "legislative", "policy affairs", "defense relation", "constituent relations", "regional affair", "system relation", "regional operation",
                           "federal program", "agency relation", "regional engagement", "communication", "news services", "federal affair", "commonwealth relation", "state affair", "community services",
                           "intercampus", "urban affairs", "public service", "school relation", "public policy", "district of columbia affair", "d,c, affair", "vice president, engagement", "vice president, policy",
                           "community development", "urban program", "university communication", "internationalization", "europe", "federal governmental relation",
                           "community and governmental", "public broadcasting", "vice president, community", "federal and washington relations", "institutional collaborations",
                           "statewide educational services", "governmental relations", "governmental affairs", "texas/border initiatives", "dc relations", "regional higher education",
                           "system integration", "design services", "global education", "public engagement", "regional programs",
                           "extended programs and educational outreach", "extended programs and outreach", "outreach programs", "international education"],


    "Advancement Foundation": ["fundraise", "fundraising", "alumni", "donation", "parent relation", "annual giving", "special events", "principal gifts", "major gift", "campaigns", 
                    "planned giving", "leadership gifts", "gift program", "trusts and estate", "giving", "philanthropy", "constituent program", "institutional advancement", "vice president, advancement", "vice president, development",
                    "university advancement", "university development", "vice president, development", "vice president, advancement", "economic advancement", "economic development",
                    "college advancement", "institute advancement", "and development", "and advancement", "resource development", "institutional advancement", "sponsored funds", "college development", "wide advancement", "institution advancement",
                    "regional development",   "presidentalumni relations", "institutional advancment", "donor engagement", "manhattanville development",
                    "institutional advancementuniversity relations", "university advancemen", "strategic engagement", "systemwide advancement",
                    "corporate and venture development"],
    "Human Resources": ["hr", "human resource", "human resources", "personnel", "recruitment", "employee relations", "union", "collective bargaining", "labor", "human relations", "human capital", "personnel", "human and", "professional development", "human service", "hiring",
                        "workforce", "human res", "compensation management"],

    "Religion": ["ministry", "mission", "ministries", "church", "religious", "religion", "spiritual", "christian development", "calvary lutheran church",
                "rockefeller memorial chapel", "marsh chapel", "hendricks chapel"],
    "Satellite Campus": ["satellite campus", "macarthur campu", "polvtechnic campus", "treasure coast campus", "edwards campus", "commonwealth campuses",
                        "broward campuses", "extended campuses", "northern campuses", "south charleston campus", "gulf coast"],
    "Athletics": ["athletic", "sports"],
    "Continued Studies": ["extended studies", "extended education", "continuing education", "continued education", "continuing studies", "lifelong learning", "professional programs", "extended learning", "adult learning",
                           "adult education", "online learning", "adult student", "lifelong education", "continuing and", "university extension", "distance learning", "continuous education", "extended university",
                           "distance education", "summer session", "advanced studies", "extended study", "extended university program", "university learning", "extended education",
                           "career education", "experiential learning", "executive education", "service learning", "digital learning", "online education", "atlas learning resources", "extended programs",
                           "cooperative extension", "edgo", "educational system", "online credit", "learner services", "enterprise learning", "extended services", "cooperative extension division",
                           "interprofessional programs", "online programs"],
    "Graduate": ["graduate program", "graduate school", "graduate and", "advanced study", "graduate education", "graduate studies", "graduate affair", "graduate sciences"],
    
    
}

SCHOOL_KEYWORDS = {
    "Arts and Sciences": ["arts and science", "arts and sciences", "letters and science", "arts, sciences, and letters", "arts, sciences", "letters and sciences",
                    "arts & sciences", "letters, sciences", "arts and letters", "arts & letters", "yeshiva college", "yale college", "college for women", "city college",
                    "southampton college", "wake forest college", "harvard college",  "university college", "oxford college", "applied sciences and arts",
                     "georgetown college", "behrend college", "hillyer college",  "college of university studies", "college of undergraduate studies",
                    "commonwealth college", "undergraduate college", "great falls college", "radcliffe institute", "school for university studies",
                    "new college", "college of general registration", "livingston college", "emory college", "global college", "rutgers college",
                    "tulane college"],


    "Engineering": ["engineering", "mines", "aerospace", "aeronautics", "polytechnic studies", "aviation", "applied science", "technology", 
    "polytechnic institute", "applied sciences", "nanoscience and nanoengineering"],
    
    "Computer Science": ["computer science", "computer,", "software engineering", "and computer", "computing", "computational science", "computational sciences",
                        "computer and cyber sciences"],
    "Data Science": ["data science", "artificial intelligence", "machine learning"],

    "Information": ["information science", "information sciences", "information management", "information systems", "information study", "information studies", "library science", 
                    "and information", "library study", "library studies", "informatics", "school of information", "division of library sciences",
                    "information and", "information school", "college of information"],
    "Archictecure": ["architecture", "architectural", "urban design", "urban planning", "environmental design", "environment and design", "design, construction", "school of construction",
    "built environments"],
    

    "Behavioral Science": ["psychology", "psychological", "human science", "human ecology", "behavioral", "human and", "childhood stud", "early childhood studies",
    "social science", "social sciences", "social and", "social ecology", "human sciences", "social research"],

    "Natural Sciences": ['natural science', "natural sciences", "mathematics", "chemistry", "biology", "mathematical", "physical science", "life science", "life sciences" , "biological science", "biological sciences",
                        "biochemistry", "natural and", "basic", "college of science", "school of science", ", science, and", ", science and", "physics", "college of the sciences", "college of sciences",
                        "physical sciences", "biomedical sciences", "biomedical education", "lyman briggs college"],
    "Environmental and Marine Science": ["environmental science", "forestry", "natural resource", "natural resources", "college of forest", "earth and mineral sciences", "environment and life sciences",
                              "school of forest", "school of environment ", "environmental and", "geology", "oceanography", "earth science", "geophysics", "seismology", "volcanology", "earth and" 
                              "paleontology", "mineral science", "geoscience", "earth science", "earth studies", "atmospheric", "college of the environment", "school of ecology", "school of environment",
                              "marine science", "marine study", "ocean science", "oceanography", "oceanographic", "ocean and", "environmental sciences", "geosciences", "fisheries and ocean sciences", "earth sciences",
                              "coast and environment", "marine studies", "earth and energy", "college of environment", "freshwater sciences", "materials energy and earth resources",
                              "marine sciences", "school for environment", "cook college"],
    
    "Business": ["business", "commerce", "mba", "college of economics", "and economics", "finance", "entrepreneurship", "school of management", "and management", "accounting", "economic,", "accountancy", "schools of management", "college of management",
                "industry management", "industrial administration", "systems and enterprises", "administrative sciences", "school of administration", "industrial administratio",
                "organizational management", "metropolitan college"],
    "Hospitality": ["hospitality", "hotel administration", "hotel management", "restaurant management"],
    "Education": ["college of education", "school of education", "teaching", "teach", "curriculum development", "human development", "and education", 
                ", education and", "teachers college", "teacher education", "college of educational", "teacher preparation", "peabody college"],
    "Criminal Justice": ["criminal justice", "criminology", "criminal", "forensics"],


    "Law": ["law", "legal studies", "industrial and labor relations", "labor and employee relations"],
    "Policy and Affairs": ["public policy", "international policy", "public affairs", "international affairs", "environmental affairs", "urban affairs", "metropolitan affairs", "international service", "leadership studies", 
                           "diplomacy", "diplomat", "international studies", "public administration", "urban policy", "global studies", "international relations", "social policy", "peace studies", "global management", "policy studies",
                           "policy, planning", "school of leadership", "policy science", "school of government", "policy planning", "public programs", "foreign service",
                           "global policy and strategy", "global affairs", "international belations and pacific studies", "james madison college", "rockefeller college"],
    

    "Agriculture": ["agriculture", "agricultural", "agribusiness"],
    "Family and Consumer Science": ["family and", "home economics", "consumer science", "family science", "home", "family studies", "family sciences", "family consumer sciences", "family life"],
    "Culinary": ["culinary", "cooking", "gastronomy"],


    "Journalism": ["journalism", "reed college of media", "college of media"],
    "Communication": ["communication", "communications"],
    "Liberal Arts": ["liberal art", "liberal studies", "interdisciplinary studies", "general studies", "liberal and", "individualized study", "liberal arts", 
                    "college of arts", "school of arts", "college of pacific", "columbia college", "general college", "douglass college", "richard l connolly college",
                    "eugene lang college"],

    "Humanities": ["humanities", "history", "historical", "philosophy", "literature", "political"],

    "Fine Arts": ["fine arts", "music", "theater", "creative", "theatre", "film", "performing art", "the arts", "design art", "dramatic arts", "dance", "visual and performing arts",
                   "visual arts", "school of drama", "recording arts", "ceramics", "fine and applied art", "school of design", "art and design", "fine", "college of design",
                   "cinema", "art ", "art, ", "studio art", "media art", "arts and performance", "drama", "arts and media", "textiles", "applied arts", "musical arts",
                   "performing arts", "hartt school", "media arts and design", "herron school of art", "school for design", "cinematic arts", "tvler school of art",
                   "innovation and design", "peabody institute"],
    "Language and Culture": ["languages", "lingusitics", "cultures", "translational studies", "intercultural studies", "ethnic studies", "hebraic studies", "cultural stud", "asian studies", "culture ", " hawaiian knowledge", 
                             "jewish", "asian and pacific studies"],


    "Nursing": ["nursing"],
    "Physical Therapy and Nutrition": ["physical therapy", "kinesiology", "nutrition", "physiotherapy", "nutritional therapy", "rehab", "human performance", "physical activity and sport sciences",
                                        "sport and human dynamics"],
    "Medical": ["medical", "pharmacy", "surgeons", "school of medicine", "college of medicine", "podiatric medicine", "osteopathic medicine", "human medicine", "pharmacology", "medicine"],

    "Dentistry" : ["dentistry", "dental", "denistry"],
    "Optometry" : ["optometry", "optics", "optical science", "optical sciences"],
    "Veterinary" : ['veterinary'],
    "Audiology": ["audiology", "institute for deaf", "speech"],
    "Gerontology": ["gerontology"],
    "Pathology": ["pathology"],
    "Health Science": ["health science", "public health", "health profession", "college of health", "school of health", "biomedical science", "and health", "physical education",
                        "health and", "health studies", "genome", "occupational therapy", "community health sciences", "applied health sciences", "graduate health sciences",
                        "summit college", "rehabilitative health sciences", "public heath", "health sciences", "population health", "health center", "graduate school of biomedical",
                        "college of applied life studies"],


    "Religious Studies": ["religious", "theology", "divinity", "biblical", "theological", "religion", "seminary", "religous", "christ college", "talmudic", "torah", "quran", "bible", "bernard revel graduate school"],
    "Social Work": ["social work", "social welfare", "community service", "human service", "human services", "social service", "public service", "social administration", "rural and community development"],
    

    #"Graduate": ["graduate school", "graduate studies", "graduate college", "college of graduate", "school of graduate",  "advancing", "advanced study", "graduate division", "graduate and professional studies", "doctoral", "graduate study", "graduate "],
    "Continued Studies": ["extended studies", "extended education", "continuing education", "continued education", "continuing studies", "lifelong learning", "professional programs", "extended learning", "adult learning",
                           "adult education", "online learning", "adult student", "lifelong education", "continuing and", "university extension", "distance learning", "continuous education", "extended university",
                           "distance education", "summer session", "armour college", "school for new learning", "evening college", "college of advancing studies"],

    "Professional Studies": ["professional studies", "professional development", "professional education", "school of professions", "professional campus", 
                            "professional schools and colleges", "college of rural alaska", "community and technical college"],
    
    "Honor College": ["honor college", "honors college", "scholar program", "honors program", "honors tutorial college"],

    "Foundation": ['foundation', "fondation"],
    "Library" : ['libraries', "library services", "university library", "zimmerman library", "dupre library", "academic library", "library affairs",
    "kramer family library", "kresge library", "galvin library", "penrose library", "z smith reynolds library", "briggs library",
    "ottenheimer library", "kraemer family library", "j willard marriott library"],
    "Satellite Campus": ["satellite campus", "downtown", "west campus", "tempe campus", "downtown phoenix campus", "brooklyn campus", "east", "midtown campus", "salkehatchie",
                            "carlsbad campus", "frost campus", "extended campus", "tri-campus", "regional campuses", "madrid campus", "community college", "harrisburg",
                            "university at riverhead", "west campus", "avery point campus", "stamford campus", "brentwood campus", "extension$", "houston center",
                            "daytona beach", "brookhaven affair", "davie campuses", "fort worth campus", "nyc tech campus", "vice president - atlanta", "edwardsville", "city center",
                            "gulf park campus", "college at wise", "senior vice president, atlanta", "polytechnic campus", "osu-okmulgee", "west", "rose hill", "tulsa",
                            "osu-oklahoma city", "osu-cascades campus", "macarthur campu", "polvtechnic campus", "treasure coast campus", "edwards campus", "commonwealth campuses",
                        "broward campuses", "cw post campus", "c w post campus", "imperial valley campus", "newark", "camden", "new brunswick", "lincoln center",
                        "calumet", "ambler", "sarasota manatee", "iupui", "stpetersburg campus", "st petersburg campus", "norman campus", "campus", "center city",
                        "lancaster", "sumter", "usc union", "vancouver", "carbondale", "wayne college", "bgsu firelands", "kent state university at geauga",
                        "carnegie mellon university in qatar", "rensselaer at hartford", "uc clermont college"],

    "Board": ["of the board", "board of", "board operation", "board relations", "council of trustees"],
    "Health System" : ["health sciences center", "health system", "baylormedcare", "health care", "ucla healthcare", "healtheare", "allied health", "health systems", "hospital", "hospitals"]
}

DESIGNATION_SET = defaultdict(set)
for wordbank in [DESIGNATION_KEYWORDS, DEAN_KEYWORDS]:
    for desig in DESIG_ORDER:
        if desig in wordbank and len(wordbank[desig]) > 0:

            DESIGNATION_SET[desig].update(set(wordbank[desig]))
            DESIGNATION_SET[desig].update(set([w+'s' for w in wordbank[desig]]))
