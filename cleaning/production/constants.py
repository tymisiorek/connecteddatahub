'''Word Banks'''
PRESIDENT_WORDS = ["president", "chancellor", "superintendent", "commissioner", "officer-in-charge"]
BOARD_WORDS = ["Trustee", "Regent", "Member", "Fellow", "Overseer", "Governor", "Curator", "Visitor", "Manager"]
POSITION_BANK = ["President", "Chancellor", "Provost", "Director", "Dean", "Controller", "Trustee", "Member", "Regent", "Chairman", "Overseer", "Assistant", "Librarian", "Secretary", "Chaplain", "Minister", "Treasurer", "Senior Counsel", "General Counsel", "Legal Counsel", "University Counsel", "College Counsel", "Special Counsel", "Corporation Counsel", "Officer", "Chief", "Professor", "Commissioner", "Fellow", "Chairperson", "Manager", "Clergy", "Coordinator", "Auditor", "Governor", "Representative", "Stockbroker", "Advisor", "Commandant", "Rector", "Attorney", "Curator", "Clerk", "Department Head", "Pastor", "Head", "Comptroller", "Deputy", "Inspector General"]
POSITION_BANK = ["President", "Chancellor", "Provost", "Director", "Dean", "Controller", "Trustee", "Member", "Regent", "Chairman", "Overseer", "Assistant", "Librarian", "Secretary", "Chaplain", "Minister", "Treasurer", "Senior Counsel", "General Counsel", "Legal Counsel", "University Counsel", "College Counsel", "Special Counsel", "Corporation Counsel", "Corporate Counsel", "Officer", "Chief", "Professor", "Commissioner", "Fellow", "Chairperson", "Manager", "Clergy", "Coordinator", "Auditor", "Governor", "Representative", "Stockbroker", "Advisor", "Commandant", "Rector", "Attorney", "Curator", "Clerk", "Department Head", "Pastor", "Head", "Comptroller", "Deputy", "Inspector General", "Instructor", "Registrar", "Ombuds", "Administrator", "Liaison", "Administrative Associate", "Webmaster", "Specialist", "University Planner", "Architect"]
DEAN_WORDS = ["summer", "student", "faculty", "academic service", "academics", "academic program", "admissions", "admission", "enrollment", "student life", "housing", "academic support", "advising", "enrollment management", 
                       "student relations", "academic computing", "academic records", "student service", "student affairs", "student development", "registrar", "financial aid", "media service", "library service", "university librar",
                       "internation affair", "special program", "continuing education", "external relation", "development", "services"]

ADMINISTRATION_WORDS = ["academic service", "academics", "academic program", "admissions", "admission", "enrollment service", "student life", "housing", "academic support", "advising", "enrollment management", 
                       "student relations", "academic computing", "academic records", "student service", "student affairs", "student development", "registrar", "financial aid", "media service", "library service", "university librar"]
VP_KEYWORDS = {
    "SubInstitution": ["arts and science", "the college", "the arts", "interdisciplinary studies", "life sciences", "agriculture", "agricultural", "liberal arts", "engineering", "law center"],
    "Generic": [],
    "Foundation": ["foundation"],


    "Administration": ["vice president, administration", "and administration", "administrative", "audit and compliance", "legal affairs", "legal services", "institutional affairs", "university affairs", "vice president, operations", 
                       "employment service", "vice president, quality", "management service", "university compliance" "university operation", "institutional services", "general administration",
                       "of the corporation", "special program", "university governance", "materials management", "executive affair"," university operation", "vice president. administration"],
    "Boards": ["of the board", "board of", "board operation"],
    "Campus Operations": ["sustainability", "facilities", "campus operations", "infrastructure", "environmental", "security", "campus police", "emergency management", "safety", 
                          "campus services", "university services", "facility operation", "university architect", "land, buildings and real estate", "auxiliary", "capital construction",
                          "property management", "plant operations", "construction", "campus residence", "physical resources", "university compliance", "physical plant", "facilities"],

    "Health Affairs": ["health service", "health affair", "ambulatory", "clinical service", "cancer", "patient care", "diagnostic service", "physicians",
               "clinical", "care contracting", "outpatient", "patient service", "medical affair", "health system affairs", "surgical service", "health system",
               "community health", "health policy"],


    "Academic Affairs": ["undergraduate education", "curriculum", "provost" "undergraduate studies", "graduate studies", "instruction", "academic program", "academic development",
                         "education affair", "undergraduate affair", "academie affairs", "educational and", "teacher education", "experiential education", "academic affair", "academic administration",
                         "undergraduate initiative", "cooperative education", "school program", "interdisciplinary education", "educational outreach", "educational,", "undergraduate studies", "educational affair",
                         "academic service", "academic afair", "educational resource", "academic enrichment", "academic resource", "university studies", "vice president, academics", "academic operation",
                         "educational development", "academic issues", "academic planning", "career development", "academic vice president"],
    "Faculty Affairs": ["faculty affair", "staff relations", "vice president, faculty"],
    "Research": ["innovation", "research", "grants", "publication", "biotechnology", "scientific", "sponsored programs"],
    

    "Student Affairs": ["student", "student life", "student service", "support", "wellbeing", "well-being", "campus life", "housing", "counseling", "student affairs", "student initiative", "student service", 
                        "student success", "student activities", "student development", "students", "university life", "student learning", "residence life", "student and community",
                        "career service", "student judicial service", "advisement", "student access", "study abroad", "dining program", "academic life"],
    "Enrollment": ["enrollment", "financial aid", "retention", "registrar", "admission", "enrolment"],
    

    "Information Service": ["technology", "information", "librar", "data management", "computer", "computing", "network service", "internet service", "electronic marketing", "converging technologies",
                    "technical service", "vice president, systems", "enterprise system", "records", "system administration"],


    "DEI": ["diversity", "equity", "inclusion", "affirmative action", "dei", "multicultural affairs", "equal opportunity", "minority affair", "intercultural affair"],
    "External Relations": [ "external", "university relation", "college relation", "public relation", "communications", "public affair", "media", "outreach", "partnership", "global",
                            "international", "study abroad", "federal relations", "public events", "institutional relation",
                           "government", "state relations", "community engagement", "community affair", "civic engagement", "community relation", "corporate relation", 
                           "foundation relation", "legislative", "policy affairs", "defense relation", "constituent relations", "regional affair", "system relation", "regional operation",
                           "federal program", "agency relation", "regional engagement", "communication", "news services", "federal affair", "commonwealth relation", "state affair", "institute relation", "community services",
                           "intercampus", "urban affairs", "public service", "school relation", "public policy", "district of columbia affair", "d.c. affair", "vice president, engagement", "vice president, policy", "institute affair",
                           "community development"],


    "Planning": ["planning", "assessment", "evaluation", "planner", "special projects", "strategy and measurement", "institutional effectiveness", "presidential initiative", "capital improvement", "strategy and policy",
                 "university projects", "institutional analysis", "commercialization strategies", "procurement", "strategic affair", "university initiative", "program development", "strategic initiative", "strategic development",
                 "strategic and"],
    "Finance": ["budget", "finance", "financial", "accounting", "marketing", "endowment",  "investment", "business", "fiscal", "and resource management", "institutional resources", "treasury management", "university resources", "audit", ", resource management",
                "commerce", "asset management"],
    "Advancement": ["fundraise", "fundraising", "alumni", "donation", "parent relation", "annual giving", "special events", "principal gifts", "major gift", "campaigns", 
                    "planned giving", "leadership gifts", "gift program", "trusts and estate", "giving", "philanthropy", "constituent program", "institutional advancement", "vice president, advancement", "vice president, development",
                    "university advancement", "university development", "vice president. development", "vice president. advancement", "economic advancement", "economic development",
                    "college advancement", "institute advancement", "and development", "and advancement", "resource development", "institutional advancement", "sponsored funds", "college development", "wide advancement", "institution advancement",
                    "regional development", "planned gift"],
    "Human Resources": ["hr", "human resource", "personnel", "recruitment", "employee relations", "union", "collective bargaining", "labor", "human relations", "human capital", "personnel", "human and", "professional development", "human service", "hiring",
                        "workforce"],
    

    "Religious": ["ministry", "mission", "ministries", "church", "religious", "religion", "spiritual", "christian development"],
    "Satellite Campus": ["satellite campus"],
    "Athletics": ["athletic", "sports"],

    "Other": []
}


KEYWORDS = {
    "Arts and Sciences": ["arts and science", "letters and science", "arts, sciences, and letters", "arts, sciences", "arts & sciences", "letters, sciences", "arts and letters", "arts & letters"],
    "Engineering": ["engineering", "mines", "aerospace", "aeronautics", "polytechnic studies", "aviation", "applied science", "computational science"],
    
    "Computer Science": ["computer science", "computer,", "software engineering", "and computer", "computing"],
    "Data Science": ["data science", "artificial intelligence", "machine learning"],
    "Technology": ["technology"],
    "Information": ["information science", "information management", "information systems", "information stud", "library science", "and information", "library stud", "informatics", "school of information", 
                    "information and", "information school"],
    "Archictecure": ["architecture", "architectural", "urban design", "urban planning", "environmental design", "environment and design", "design, construction", "school of construction"],
    

    "Behavioral Science": ["psychology", "psychological", "human science", "human ecology", "behavioral", "human and", "childhood stud"],
    "Social Sciences": ["social science", "social and", "social ecology"],
    "Natural Sciences": ['natural science', "mathematics", "chemistry", "biology", "mathematical", "physical science", "life science", "biological science", 
                        "biochemistry", "natural and", "basic", "college of science", "school of science", ", science, and", ", science and", "physics", "college of the sciences"],
    "Environmental and Earth Science": ["environmental science", "forestry", "natural resource", "college of forest", 
                              "school of forest", "school of environment ", "environmental and", "geology", "oceanography", "earth science", "geophysics", "seismology", "volcanology", "earth and" 
                              "paleontology", "mineral science", "geoscience", "earth science", "earth studies", "atmospheric", "college of the environment", "school of ecology", "school of environment"],
    "Marine Science": ["marine science", "marine stud", "ocean science", "oceanography", "oceanographic", "ocean and"],

    
    "Business": ["business", "commerce", "mba", "college of economics", "and economics", "finance", "entrepreneurship", "school of management", "and management", "accounting", "agribusiness", "economic,", "accountancy", "schools of management", "college of management"],
    "Hospitality": ["hospitality", "hotel administration", "hotel management", "restaurant management"],
    "Education": ["college of education", "school of education", "teaching", "teach", "curriculum development", "human development", "and education", ", education and"],
    "Criminal Justice": ["criminal justice", "criminology", "criminal", "forensics"],


    "Law": ["law", "legal studies"],
    "Policy and Affairs": ["public policy", "international policy", "public affairs", "international affairs", "environmental affairs", "urban affairs", "metropolitan affairs", "international service", "leadership studies", 
                           "diplomacy", "diplomat", "international studies", "public administration", "urban policy", "global studies", "international relations", "social policy", "peace studies", "global management", "policy studies",
                           "policy, planning", "school of leadership", "policy science"],
    

    "Agriculture": ["agriculture", "agricultural", "agribusiness"],
    "Family and Consumer Science": ["family and", "home economics", "consumer science", "family science", "home", "family studies"],
    "Culinary": ["culinary", "cooking", "gastronomy"],


    "Journalism": ["journalism"],
    "Communication": ["communication"],
    "Liberal Arts": ["liberal art", "liberal studies", "interdisciplinary studies", "general studies", "liberal and", "individualized study"],
    "Humanities": ["humanities", "history", "historical", "philosophy", "literature", "political"],
    "Fine Arts": ["fine arts", "music", "theater", "creative", "theatre", "film", "performing art", "the arts", "design art", "dramatic arts", "dance",
                   "visual arts", "school of drama", "recording arts", "ceramics", "fine and applied art", "school of design", "art and design", "fine", 
                   "cinema", "art ", "art, ", "studio art", "media art", "arts and performance", "drama", "arts and media", "textiles", "applied arts"],
    "Language and Culture": ["languages", "lingusitics", "cultures", "translational studies", "intercultural studies", "ethnic studies", "hebraic studies", "cultural stud", "asian studies", "culture ", " hawaiian knowledge", 
                             "jewish", "asian and pacific studies"],


    "Nursing": ["nursing"],
    "Physical Therapy and Nutrition": ["physical therapy", "nutrition", "physiotherapy", "nutritional therapy", "rehab", "human performance"],
    "Medical": ["medical", "pharmacy", "surgeons", "school of medicine", "college of medicine", "podiatric medicine", "osteopathic medicine", "human medicine"],
    "Pharmacy": ["pharmacy", "pharmacology"],
    "Dentistry" : ["dentistry", "dental", "denistry"],
    "Optometry" : ["optometry", "optics", "optical science"],
    "Veterinary" : ['veterinary'],
    "Audiology": ["audiology"],
    "Gerontology": ["gerontology"],
    "Pathology": ["pathology"],
    "Health Science": ["health science", "public health", "health profession", "college of health", "school of health", "biomedical science", "and health", "allied health", "physical education",
                        "health and", "health studies", "genome", "occupational therapy"],


    "Religious Studies": ["religious", "theology", "divinity", "biblical", "theological", "religion", "seminary", "religous", "christ college", "talmudic", "torah", "quran", "bible"],
    "Social Work": ["social work", "social welfare", "community service", "human service", "social service", "public service", "social administration"],
    

    "Graduate": ["graduate school", "graduate studies", "graduate college", "college of graduate", "school of graduate",  "advancing", "advanced study", "graduate division", "graduate and professional studies", "doctoral", "graduate study", "graduate "],
    "Continued Studies": ["extended studies", "extended education", "continuing education", "continued education", "continuing studies", "lifelong learning", "professional programs", "extended learning", "adult learning",
                           "adult education", "online learning", "adult student", "lifelong education", "continuing and", "university extension", "distance learning", "continuous education", "extended university"],
    "Professional Studies": ["professional studies", "professional development", "professional education", "school of professions", "professional campus"],
    # "Administration": ["academic service", "academics", "academic program", "admissions", "admission", "enrollment service", "student life", "housing", "academic support", "advising", "enrollment management", 
    #                    "student relations", "academic computing", "academic records", "student service", "student affairs", "student development", "registrar", "financial aid", "media service", "library service", 
    #                    "university librar", "information service", "information access", "library access", "residence", "academic affairs", "library affairs", "academic succes", "first year student",
    #                    "undergraduate studies", "undergraduate education"],
    "Honor College": ["honor college", "honors college", "scholar program"],

    # "Satellite Campus": ["campus"],
    # "Foundation": ["foundation"],
    # "Boards": ["board of", "regents", "trustees", "council of"],
    "Hospital": ["hospital"],
    "University College": ["university college"],
    "Error": []
}

ADMIN_TYPES = ["Human Resources", "Advancement", "Finance", "Planning", "Academic Affairs", "Faculty Affairs", "External Relations", "Campus Operations", "Research", "Board VP", "Administration", "Foundation", "Generic", "Enrollment" ]

DEAN_KEYWORDS = {
    # "Head VP": ["head vice president"],
    # "SubInstitution": ["arts and science", "the college", "the arts", "interdisciplinary studies", "life sciences", "agriculture", "agricultural", "liberal arts", "engineering", "law center"],
    "Generic": [],
    "Foundation": ["foundation"],


    "Administration": ["vice president, administration", "and administration", "administrative", "audit and compliance", "legal affairs", "legal services", "institutional affairs", "university affairs", "vice president, operations", 
                       "employment service", "vice president, quality", "management service", "university compliance" "university operation", "institutional services",
                       "of the corporation", "special program", "university governance", "materials management", "executive affair"," university operation", "vice president. administration", "administration",
                       "resources"],
    "Board VP": ["of the board", "board of", "board operation"],
    "Campus Operations": ["sustainability", "facilities", "campus operations", "infrastructure", "environmental", "security", "campus police", "emergency management", "safety", 
                          "campus services", "university services", "facility operation", "university architect", "land, buildings and real estate", "auxiliary", "capital construction",
                          "property management", "plant operations", "construction", "campus residence", "physical resources", "university compliance", "physical plant", "campus involvement"],
    "Health Science": ["health science", "public health", "health profession", "college of health", "school of health", "biomedical science", "and health", "allied health", "physical education",
                        "health and", "health studies", "genome"],
    "Medical": ["medical", "pharmacy", "surgeons", "school of medicine", "college of medicine", "podiatric medicine", "osteopathic medicine"],



    "Academic Affairs": ["undergraduate education", "curriculum", "provost" "undergraduate studies", "graduate studies", "instruction", "academic program", "academic development",
                         "education affair", "undergraduate affair", "academie affairs", "educational and", "teacher education", "experiential education", "academic affair", "academic administration",
                         "undergraduate initiative", "cooperative education", "school program", "interdisciplinary education", "educational outreach", "educational,", "undergraduate studies", "educational affair",
                         "academic service", "academic afair", "educational resource", "academic enrichment", "academic resource", "university studies", "vice president, academics", "academic operation",
                         "educational development", "academic issues", "academic planning", "academic department"],
    "Faculty Affairs": ["faculty", "staff relations", "faculties"],
    "Research": ["innovation", "research", "grants", "publication", "biotechnology", "scientific", "sponsored programs"],
    

    "Student Affairs": ["student", "student life", "student service", "support", "wellbeing", "well-being", "campus life", "housing", "counseling", "student affairs", "student initiative", "student service", 
                        "student success", "student activities", "student development", "students", "university life", "student learning", "residence life", "student and community",
                        "career service", "student judicial service", "advisement", "student access", "study abroad", "dining program", "academic life", "freshmen", "freshman"],
    "Enrollment": ["enrollment", "financial aid", "retention", "registrar", "admission", "enrolment"],
    

    "Information and Technology": ["technology", "information", "librar", "data management", "computer", "computing", "network service", "internet service", "electronic marketing", "converging technologies",
                    "technical service", "vice president, systems", "enterprise system", "records", "system administration"],


    "DEI": ["diversity", "equity", "inclusion", "affirmative action", "dei", "multicultural affairs", "equal opportunity", "minority affair", "intercultural affair"],
    "External Relations": [ "external", "university relation", "college relation", "public relation", "communications", "public affair", "media", "outreach", "partnership", "global",
                            "international", "study abroad", "federal relations", "public events", "institutional relation",
                           "government", "state relations", "community engagement", "community affair", "civic engagement", "community relation", "corporate relation", 
                           "foundation relation", "legislative", "policy affairs", "defense relation", "constituent relations", "regional affair", "system relation", "regional operation",
                           "federal program", "agency relation", "regional engagement", "communication", "news services", "federal affair", "commonwealth relation", "state affair", "institute relation", "community services",
                           "intercampus", "urban affairs", "public service", "school relation", "public policy", "district of columbia affair", "d.c. affair", "vice president, engagement", "vice president, policy", "institute affair",
                           "community development"],


    "Planning": ["planning", "assessment", "evaluation", "planner", "special projects", "strategy and measurement", "institutional effectiveness", "presidential initiative", "capital improvement", "strategy and policy",
                 "university projects", "institutional analysis", "commercialization strategies", "procurement", "strategic affair", "university initiative", "program development", "strategic initiative", "strategic development",
                 "strategic and", "project", "program"],
    "Finance": ["budget", "finance", "financial", "accounting", "marketing", "endowment",  "investment", "business", "fiscal", "and resource management", "institutional resources", "treasury management", "university resources", "audit", ", resource management",
                "commerce", "asset management"],
    "Advancement": ["fundraise", "fundraising", "alumni", "donation", "parent relation", "annual giving", "special events", "principal gifts", "major gift", "campaigns", 
                    "planned giving", "leadership gifts", "gift program", "trusts and estate", "giving", "philanthropy", "constituent program", "institutional advancement", "vice president, advancement", "vice president, development",
                    "university advancement", "university development", "vice president. development", "vice president. advancement", "economic advancement", "economic development",
                    "college advancement", "institute advancement", "and development", "and advancement", "resource development", "institutional advancement", "sponsored funds", "college development", "wide advancement", "institution advancement",
                    "regional development", "development", "advancement"],
    "Human Resources": ["hr", "human resource", "personnel", "recruitment", "employee relations", "union", "collective bargaining", "labor", "human relations", "human capital", "personnel", "human and", "professional development", "human service", "hiring",
                        "workforce"],
    

    "Religion": ["ministry", "mission", "ministries", "church", "religious", "religion", "spiritual", "christian development"],
    "Satellite Campus": ["satellite campus"],
    "Athletics": ["athletic", "sports"],
    # "Agriculture": ["agriculture", "agricultural"],
    # "Continued Studies": ["extended studies", "extended education", "continuing education", "continued education", "continuing studies", "lifelong learning", "professional programs", "extended learning",
    #                        "adult education", "online learning", "adult student", "lifelong education", "continuing and", "university extension", "extended program", "distance learning", "continuous education",
    #                        "online program", "online school", "online college", "online university", "distance education", "extended service"],
    "Graduate": ["graduate program", "graduate school", "graduate and", "advanced study", "graduate education", "graduate studies", "graduate "],
    "Subinstitution Match":  ["Arts and Sciences", "Engineering", "Applied Science", "Computer Science", "Data Science", "Technology", "Information", "Architecture", "Behavioral Science", "Social Sciences", "Natural Sciences", "Environmental and Earth Science", "Marine Science", "Business", "Hospitality", "Criminal Justice", "Law", "Policy and Affairs", "Agriculture", "Family and Consumer Science", "Culinary", "Journalism", "Communication", "Liberal Arts", "Humanities", "Fine Arts", "Language and Culture", "Nursing", "Physical Therapy and Nutrition", "Pharmacy", "Dentistry", "Optometry", "Veterinary", "Audiology", "Gerontology", "Pathology", "Social Work", "Continued Studies", "Professional Studies", "Honor College", "Hospital"],
    "Other": []
}
