from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(
    __name__,
    static_folder='static/s',
    template_folder='templates'
)

app.secret_key = "studentguide-development-key"

# Temporary storage until database integration
users = {}
student_profiles = {}


# Login protection
def login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if 'email' not in session:
            flash('Please login first.')
            return redirect(url_for('login'))

        return route_function(*args, **kwargs)

    return wrapper# ==========================================
# STUDENT GUIDANCE COURSE DATA
# ==========================================

def make_guidance_course(
    name, level, stream, category, description,
    eligibility, duration, subjects, admission,
    entrance_exams, careers, higher_studies
):
    return {
        "name": name,
        "level": level,
        "stream": stream,
        "category": category,
        "description": description,
        "eligibility": eligibility,
        "duration": duration,
        "subjects": subjects,
        "admission": admission,
        "entrance_exams": entrance_exams,
        "careers": careers,
        "higher_studies": higher_studies
    }


# Main course list
STUDENT_GUIDANCE_COURSES = [

    # ======================================
    # AFTER 10TH - SCHOOL GROUPS
    # ======================================

    make_guidance_course(
        "Computer Science with Mathematics",
        "After 10th", "Science", "School Group",
        "A higher secondary group for students interested in computing, mathematics and technology.",
        "Completion of Class 10. Admission depends on school rules and available seats.",
        "2 years",
        "Physics, Chemistry, Mathematics, Computer Science, English",
        "Apply for Class 11 admission in a school offering this group.",
        "Usually no common entrance exam for school admission.",
        "Useful foundation for software, engineering and computing careers.",
        "B.E., B.Tech, B.Sc Computer Science, BCA and other related degrees."
    ),

    make_guidance_course(
        "Biology with Mathematics",
        "After 10th", "Science", "School Group",
        "A science group combining biological sciences with mathematics.",
        "Completion of Class 10. School admission requirements apply.",
        "2 years",
        "Physics, Chemistry, Biology, Mathematics, English",
        "Apply to a school offering the Biology-Mathematics combination.",
        "Usually no common entrance exam for school admission.",
        "Foundation for medicine, engineering, biotechnology and research.",
        "MBBS, BDS, B.Sc, B.Tech and other related courses."
    ),

    make_guidance_course(
        "Biology without Mathematics",
        "After 10th", "Science", "School Group",
        "A biology-focused science group for students interested in life sciences and healthcare.",
        "Completion of Class 10. School admission requirements apply.",
        "2 years",
        "Physics, Chemistry, Biology, English and applicable language subjects",
        "Apply to a school offering the Biology group without Mathematics.",
        "Usually no common entrance exam for school admission.",
        "Foundation for healthcare, medicine and life-science fields.",
        "MBBS, BDS, Nursing, Pharmacy, Agriculture and B.Sc Life Sciences."
    ),

    make_guidance_course(
        "Commerce with Mathematics",
        "After 10th", "Commerce", "School Group",
        "A commerce group combining business studies, accounting and mathematics.",
        "Completion of Class 10. School admission requirements apply.",
        "2 years",
        "Accountancy, Commerce, Economics, Mathematics, English",
        "Apply to a school offering Commerce with Mathematics.",
        "Usually no common entrance exam for school admission.",
        "Accounting, banking, finance and business-related careers.",
        "B.Com, BBA, Economics, CA and other finance-related courses."
    ),

    make_guidance_course(
        "Commerce with Computer Applications",
        "After 10th", "Commerce", "School Group",
        "A commerce group combining business subjects with computer applications.",
        "Completion of Class 10. School admission requirements apply.",
        "2 years",
        "Accountancy, Commerce, Economics, Computer Applications, English",
        "Apply to a school offering this subject combination.",
        "Usually no common entrance exam for school admission.",
        "Business administration, accounting and computer-based office work.",
        "B.Com Computer Applications, BCA, BBA and related degrees."
    ),

    make_guidance_course(
        "Arts and Humanities",
        "After 10th", "Arts", "School Group",
        "A group for students interested in society, history, languages and humanities.",
        "Completion of Class 10. School admission requirements apply.",
        "2 years",
        "History, Geography, Economics, Political Science, English",
        "Apply to a school offering Arts and Humanities subjects.",
        "Usually no common entrance exam for school admission.",
        "Teaching, public administration, journalism and social services.",
        "B.A. History, Economics, Political Science, English and related degrees."
    ),

    # ======================================
    # AFTER 12TH - SCIENCE COURSES
    # ======================================

    make_guidance_course(
        "B.E. Computer Science and Engineering",
        "After 12th", "Science", "Engineering",
        "An engineering degree focused on computer systems, programming, software and computing technologies.",
        "Usually Class 12 with Mathematics and required science subjects. Exact eligibility varies by institution.",
        "4 years",
        "Programming, Data Structures, Algorithms, Operating Systems, DBMS, Computer Networks",
        "Apply through the relevant university or state counselling process.",
        "Examples include JEE Main and state-level engineering entrance exams, depending on the institution.",
        "Software Developer, Systems Engineer, Application Developer, Software Tester.",
        "M.E., M.Tech, M.S. and related postgraduate programmes."
    ),

    make_guidance_course(
        "B.Tech Artificial Intelligence and Data Science",
        "After 12th", "Science", "Engineering",
        "An engineering programme covering artificial intelligence, data analysis, machine learning and computing.",
        "Usually Class 12 with Mathematics and required science subjects. Check institution-specific rules.",
        "4 years",
        "Python, Mathematics, Statistics, Machine Learning, Artificial Intelligence, Data Science",
        "Apply through the institution's admission process or engineering counselling.",
        "JEE Main or state-level engineering entrance exams where applicable.",
        "Data Analyst, AI Developer, Machine Learning Engineer, Data Engineer.",
        "M.Tech AI, M.Tech Data Science, M.S. and related postgraduate courses."
    ),

    make_guidance_course(
        "B.Tech Information Technology",
        "After 12th", "Science", "Engineering",
        "An engineering degree focused on information systems, software and network technologies.",
        "Usually Class 12 with Mathematics and required science subjects. Institution rules vary.",
        "4 years",
        "Programming, Web Technology, Database Systems, Networks, Cyber Security",
        "Apply through the relevant college or engineering counselling process.",
        "JEE Main or state-level engineering entrance exams where applicable.",
        "IT Engineer, Web Developer, Network Administrator, Software Developer.",
        "M.E., M.Tech, M.S. and related postgraduate programmes."
    ),

    make_guidance_course(
        "MBBS",
        "After 12th", "Science", "Medical",
        "A professional medical degree that prepares students for the practice of medicine.",
        "Class 12 with Physics, Chemistry and Biology, with applicable minimum marks and age requirements.",
        "5.5 years including compulsory internship in India.",
        "Anatomy, Physiology, Biochemistry, Pathology, Pharmacology, Medicine, Surgery",
        "Admission through the applicable national medical counselling process.",
        "NEET-UG is required for admission in India.",
        "Doctor after completing the degree, internship and applicable registration requirements.",
        "MD, MS and other recognised postgraduate medical programmes."
    ),

    make_guidance_course(
        "BDS",
        "After 12th", "Science", "Medical",
        "A professional degree focused on dental health, oral diseases and dental treatment.",
        "Class 12 with Physics, Chemistry and Biology, subject to applicable admission rules.",
        "5 years including internship.",
        "Dental Anatomy, Oral Pathology, Oral Medicine, Periodontics, Orthodontics",
        "Admission through the applicable medical and dental counselling process.",
        "NEET-UG is required for admission in India.",
        "Dental Surgeon after completing required training and registration.",
        "MDS and other recognised postgraduate dental programmes."
    ),

    make_guidance_course(
        "B.Sc Nursing",
        "After 12th", "Science", "Healthcare",
        "A professional undergraduate programme that prepares students for nursing and patient care.",
        "Usually Class 12 with Physics, Chemistry and Biology. Institution-specific criteria apply.",
        "4 years",
        "Anatomy, Physiology, Nutrition, Nursing Foundations, Community Health Nursing",
        "Apply through the college or university admission process.",
        "Entrance requirements vary by institution and state.",
        "Staff Nurse after meeting applicable registration requirements, Nursing Educator.",
        "M.Sc Nursing and related postgraduate programmes."
    ),

    make_guidance_course(
        "B.Sc Agriculture",
        "After 12th", "Science", "Agriculture",
        "A degree covering crop production, soil science, agricultural technology and farm management.",
        "Class 12 with eligible science or agriculture subjects as specified by the institution.",
        "Usually 4 years.",
        "Agronomy, Soil Science, Plant Breeding, Horticulture, Agricultural Economics",
        "Apply through the university or state admission process.",
        "ICAR-related or state and university entrance processes where applicable.",
        "Agriculture Officer, Farm Manager, Agricultural Research Assistant.",
        "M.Sc Agriculture and related agricultural specialisations."
    ),

    make_guidance_course(
        "B.Sc Computer Science",
        "After 12th", "Science", "Science",
        "A science degree focused on programming, computer systems and software concepts.",
        "Class 12. Mathematics or Computer Science requirements vary by college.",
        "Usually 3 years; some institutions offer a 4-year honours programme.",
        "Programming, Data Structures, Computer Networks, DBMS, Operating Systems",
        "Apply through merit or the university admission process.",
        "CUET or institution-specific entrance exams where applicable.",
        "Programmer, Software Tester, IT Support Executive, Junior Developer.",
        "M.Sc Computer Science, MCA and related postgraduate courses."
    ),

    # Part 3 will continue this same list.# ======================================
    # AFTER 12TH - MORE SCIENCE COURSES
    # ======================================

    make_guidance_course(
        "B.E. Electronics and Communication Engineering",
        "After 12th", "Science", "Engineering",
        "An engineering degree focused on electronic devices, communication systems and embedded technologies.",
        "Class 12 with Mathematics, Physics and Chemistry, subject to college rules.",
        "4 years",
        "Electronic Circuits, Signals and Systems, Digital Electronics, Communication Systems, Embedded Systems",
        "Apply through engineering counselling or the institution's admission process.",
        "JEE Main or state-level engineering entrance exams where applicable.",
        "Electronics Engineer, Communication Engineer, Embedded Systems Engineer.",
        "M.E., M.Tech and M.S. in related specialisations."
    ),

    make_guidance_course(
        "B.E. Electrical and Electronics Engineering",
        "After 12th", "Science", "Engineering",
        "A degree covering electrical machines, power systems and electronic circuits.",
        "Class 12 with Mathematics, Physics and Chemistry, subject to college rules.",
        "4 years",
        "Electrical Machines, Power Systems, Control Systems, Circuit Theory, Power Electronics",
        "Apply through engineering counselling or college admission.",
        "JEE Main or state-level engineering entrance exams where applicable.",
        "Electrical Engineer, Power Systems Engineer, Maintenance Engineer.",
        "M.E. or M.Tech in Electrical Engineering and related fields."
    ),

    make_guidance_course(
        "B.E. Mechanical Engineering",
        "After 12th", "Science", "Engineering",
        "An engineering programme dealing with machines, manufacturing and mechanical systems.",
        "Class 12 with Mathematics, Physics and Chemistry, subject to college rules.",
        "4 years",
        "Engineering Mechanics, Thermodynamics, Manufacturing, Machine Design, Fluid Mechanics",
        "Apply through engineering counselling or college admission.",
        "JEE Main or state-level engineering entrance exams where applicable.",
        "Mechanical Engineer, Design Engineer, Production Engineer.",
        "M.E., M.Tech and M.S. in mechanical specialisations."
    ),

    make_guidance_course(
        "B.E. Civil Engineering",
        "After 12th", "Science", "Engineering",
        "An engineering degree focused on buildings, roads, bridges and infrastructure.",
        "Class 12 with Mathematics, Physics and Chemistry, subject to college rules.",
        "4 years",
        "Structural Engineering, Surveying, Construction Materials, Geotechnical Engineering, Hydraulics",
        "Apply through engineering counselling or college admission.",
        "JEE Main or state-level engineering entrance exams where applicable.",
        "Civil Engineer, Site Engineer, Structural Design Assistant.",
        "M.E. or M.Tech in Civil Engineering specialisations."
    ),

    make_guidance_course(
        "B.Tech Biotechnology",
        "After 12th", "Science", "Science",
        "A degree combining biology and technology to develop products and processes for healthcare and industry.",
        "Class 12 with eligible science subjects. Mathematics or Biology requirements vary by institution.",
        "4 years",
        "Cell Biology, Genetics, Microbiology, Biochemistry, Genetic Engineering",
        "Apply through the college or university admission process.",
        "Institution-specific entrance exams or other accepted admission routes.",
        "Biotechnology Assistant, Research Assistant, Laboratory Associate.",
        "M.Sc Biotechnology, M.Tech Biotechnology and related programmes."
    ),

    make_guidance_course(
        "B.Pharm",
        "After 12th", "Science", "Pharmacy",
        "A professional degree covering medicines, drug development and pharmaceutical sciences.",
        "Class 12 with Physics, Chemistry and Biology or Mathematics, according to applicable rules.",
        "4 years",
        "Pharmaceutics, Pharmacology, Pharmaceutical Chemistry, Pharmacognosy",
        "Apply through the college or state admission process.",
        "Relevant state or university entrance exams where applicable.",
        "Pharmacy-related roles after meeting applicable registration requirements.",
        "M.Pharm, Pharm.D and related postgraduate programmes."
    ),

    make_guidance_course(
        "B.Sc Physics",
        "After 12th", "Science", "Science",
        "A science degree studying matter, energy, motion and physical laws.",
        "Class 12 with Physics and usually Mathematics, as required by the college.",
        "Usually 3 years; some institutions offer a 4-year programme.",
        "Mechanics, Optics, Electricity, Magnetism, Thermodynamics, Modern Physics",
        "Apply through merit or university admission.",
        "CUET or institution-specific entrance exams where applicable.",
        "Laboratory Assistant, Research Assistant, Science Educator.",
        "M.Sc Physics, specialised research programmes and related higher studies."
    ),

    make_guidance_course(
        "B.Sc Chemistry",
        "After 12th", "Science", "Science",
        "A degree studying chemical substances, reactions and laboratory methods.",
        "Class 12 with Chemistry and other required science subjects.",
        "Usually 3 years; some institutions offer a 4-year programme.",
        "Organic Chemistry, Inorganic Chemistry, Physical Chemistry, Analytical Chemistry",
        "Apply through merit or university admission.",
        "CUET or institution-specific entrance exams where applicable.",
        "Laboratory Assistant, Quality Control Assistant, Research Assistant.",
        "M.Sc Chemistry and specialised chemistry programmes."
    ),

    make_guidance_course(
        "B.Sc Mathematics",
        "After 12th", "Science", "Science",
        "A degree focused on mathematical theories, calculations and problem-solving.",
        "Class 12 with Mathematics.",
        "Usually 3 years; some institutions offer a 4-year programme.",
        "Algebra, Calculus, Statistics, Differential Equations, Real Analysis",
        "Apply through merit or university admission.",
        "CUET or institution-specific entrance exams where applicable.",
        "Mathematics Educator, Statistical Assistant, Research Assistant.",
        "M.Sc Mathematics, Statistics and related postgraduate programmes."
    ),

    make_guidance_course(
        "B.Sc Microbiology",
        "After 12th", "Science", "Science",
        "A degree studying microorganisms and their applications in healthcare, food and research.",
        "Class 12 with Biology or other accepted science subjects, depending on the college.",
        "Usually 3 years; some institutions offer a 4-year programme.",
        "Microbiology, Immunology, Genetics, Biochemistry, Virology",
        "Apply through merit or university admission.",
        "CUET or institution-specific entrance exams where applicable.",
        "Laboratory Assistant, Microbiology Technician, Research Assistant.",
        "M.Sc Microbiology and related life-science programmes."
    ),

    make_guidance_course(
        "BCA",
        "After 12th", "Science", "Computer Applications",
        "An undergraduate programme focused on computer applications, programming and software development.",
        "Class 12. Mathematics requirements vary between institutions.",
        "Usually 3 years; some institutions offer a 4-year programme.",
        "Programming, Database Management, Web Development, Computer Networks, Software Engineering",
        "Apply through merit or the institution's admission process.",
        "CUET or institution-specific entrance exams where applicable.",
        "Junior Programmer, Web Developer, Software Support Associate.",
        "MCA, M.Sc Computer Science and related postgraduate courses."
    ),

    # ======================================
    # AFTER 12TH - COMMERCE COURSES
    # ======================================

    make_guidance_course(
        "B.Com",
        "After 12th", "Commerce", "Commerce",
        "An undergraduate degree covering accounting, business, finance and commerce.",
        "Class 12 from a recognised board. Subject requirements vary by college.",
        "Usually 3 years; some institutions offer a 4-year programme.",
        "Financial Accounting, Business Law, Economics, Taxation, Auditing",
        "Apply through merit or university admission.",
        "CUET or institution-specific entrance exams where applicable.",
        "Accounts Assistant, Finance Executive, Tax Assistant.",
        "M.Com, MBA, CA and other professional qualifications."
    ),

    make_guidance_course(
        "B.Com Accounting and Finance",
        "After 12th", "Commerce", "Finance",
        "A commerce degree specialising in accounting practices and financial management.",
        "Class 12. Commerce or Mathematics may be preferred by some institutions.",
        "Usually 3 years; some institutions offer a 4-year programme.",
        "Financial Accounting, Cost Accounting, Taxation, Financial Management, Auditing",
        "Apply through merit or the college admission process.",
        "CUET or institution-specific entrance exams where applicable.",
        "Accounts Executive, Finance Assistant, Audit Assistant.",
        "M.Com, MBA Finance, CA and CMA qualifications."
    ),

    make_guidance_course(
        "B.Com Computer Applications",
        "After 12th", "Commerce", "Computer Applications",
        "A degree combining commerce subjects with computer and business applications.",
        "Class 12. Exact subject requirements depend on the institution.",
        "Usually 3 years; some institutions offer a 4-year programme.",
        "Accounting, Commerce, Business Statistics, Computer Applications, Database Basics",
        "Apply through merit or college admission.",
        "CUET or institution-specific entrance exams where applicable.",
        "Accounts Assistant, Computer Applications Assistant, Business Support Executive.",
        "M.Com, MCA where eligible, MBA and related courses."
    ),

    make_guidance_course(
        "BBA",
        "After 12th", "Commerce", "Management",
        "An undergraduate programme covering business operations, management and administration.",
        "Class 12 from a recognised board. Minimum marks and subject rules vary.",
        "Usually 3 years; some institutions offer a 4-year programme.",
        "Management Principles, Marketing, Finance, Human Resources, Business Communication",
        "Apply through merit or the institution's admission process.",
        "CUET or institution-specific management entrance exams where applicable.",
        "Management Trainee, Business Development Assistant, Operations Executive.",
        "MBA, PGDM and related postgraduate programmes."
    ),

    make_guidance_course(
        "B.A. Economics",
        "After 12th", "Commerce", "Economics",
        "A degree studying markets, money, public policy and economic systems.",
        "Class 12. Mathematics requirements vary by institution.",
        "Usually 3 years; some institutions offer a 4-year programme.",
        "Microeconomics, Macroeconomics, Statistics, Indian Economy, Public Finance",
        "Apply through merit or university admission.",
        "CUET or institution-specific entrance exams where applicable.",
        "Research Assistant, Economic Data Assistant, Business Analyst Trainee.",
        "M.A. Economics and related postgraduate programmes."
    ),

    make_guidance_course(
        "B.Com Banking and Insurance",
        "After 12th", "Commerce", "Finance",
        "A commerce programme focused on banking, insurance and financial services.",
        "Class 12 from a recognised board. College-specific criteria apply.",
        "Usually 3 years; some institutions offer a 4-year programme.",
        "Banking, Insurance, Financial Accounting, Risk Management, Business Law",
        "Apply through merit or university admission.",
        "CUET or institution-specific entrance exams where applicable.",
        "Banking Assistant, Insurance Operations Assistant, Finance Executive.",
        "M.Com, MBA Finance and related postgraduate programmes."
    ),

    make_guidance_course(
        "B.Com Corporate Secretaryship",
        "After 12th", "Commerce", "Commerce",
        "A degree introducing company administration, corporate law and governance.",
        "Class 12 from a recognised board. College-specific criteria apply.",
        "Usually 3 years; some institutions offer a 4-year programme.",
        "Company Law, Business Law, Accounting, Corporate Governance, Taxation",
        "Apply through merit or university admission.",
        "CUET or institution-specific entrance exams where applicable.",
        "Corporate Office Assistant, Company Administration Assistant.",
        "M.Com, MBA and Company Secretary professional studies."
    ),

    # ======================================
    # AFTER 12TH - ARTS COURSES
    # ======================================

    make_guidance_course(
        "B.A. English Literature",
        "After 12th", "Arts", "Languages",
        "A degree studying English literature, language, writing and communication.",
        "Class 12 from a recognised board. College-specific criteria apply.",
        "Usually 3 years; some institutions offer a 4-year programme.",
        "Poetry, Drama, Fiction, Literary Criticism, Communication Skills",
        "Apply through merit or university admission.",
        "CUET or institution-specific entrance exams where applicable.",
        "Content Writer, Editorial Assistant, Language Educator.",
        "M.A. English, Journalism and related postgraduate programmes."
    ),

    make_guidance_course(
        "B.A. History",
        "After 12th", "Arts", "Humanities",
        "A degree studying historical events, societies, cultures and civilisations.",
        "Class 12 from a recognised board.",
        "Usually 3 years; some institutions offer a 4-year programme.",
        "Ancient History, Medieval History, Modern History, Indian History, World History",
        "Apply through merit or university admission.",
        "CUET or institution-specific entrance exams where applicable.",
        "History Research Assistant, Museum Assistant, Educator.",
        "M.A. History, Archaeology and related postgraduate programmes."
    ),

    make_guidance_course(
        "B.A. Political Science",
        "After 12th", "Arts", "Social Sciences",
        "A degree studying government, political systems, public administration and international relations.",
        "Class 12 from a recognised board.",
        "Usually 3 years; some institutions offer a 4-year programme.",
        "Political Theory, Indian Government, Public Administration, International Relations",
        "Apply through merit or university admission.",
        "CUET or institution-specific entrance exams where applicable.",
        "Research Assistant, Public Policy Assistant, Administrative Support roles.",
        "M.A. Political Science, Public Administration and related courses."
    ),

    make_guidance_course(
        "B.A. Psychology",
        "After 12th", "Arts", "Social Sciences",
        "A degree studying human behaviour, thinking, emotions and psychological research.",
        "Class 12 from a recognised board. Subject requirements vary by institution.",
        "Usually 3 years; some institutions offer a 4-year programme.",
        "General Psychology, Social Psychology, Developmental Psychology, Research Methods",
        "Apply through merit or university admission.",
        "CUET or institution-specific entrance exams where applicable.",
        "Research Assistant, Human Resources Assistant, Psychology Support roles.",
        "M.A. Psychology and further recognised training for professional practice."
    ),

    make_guidance_course(
        "B.A. Sociology",
        "After 12th", "Arts", "Social Sciences",
        "A degree studying society, communities, institutions and social relationships.",
        "Class 12 from a recognised board.",
        "Usually 3 years; some institutions offer a 4-year programme.",
        "Sociological Theory, Social Research, Indian Society, Social Institutions",
        "Apply through merit or university admission.",
        "CUET or institution-specific entrance exams where applicable.",
        "Social Research Assistant, Community Programme Assistant.",
        "M.A. Sociology, Social Work and related postgraduate courses."
    ),

    make_guidance_course(
        "B.A. Journalism and Mass Communication",
        "After 12th", "Arts", "Media",
        "A degree covering news reporting, media production, communication and digital journalism.",
        "Class 12 from a recognised board.",
        "Usually 3 years; some institutions offer a 4-year programme.",
        "Journalism, Reporting, Media Law, Advertising, Public Relations, Digital Media",
        "Apply through merit or the college admission process.",
        "Institution-specific entrance tests or interviews where applicable.",
        "Reporter, Content Writer, Media Production Assistant.",
        "M.A. Journalism, Mass Communication and related postgraduate courses."
    ),

    make_guidance_course(
        "B.S.W. Social Work",
        "After 12th", "Arts", "Social Sciences",
        "A degree preparing students to understand community needs and support social development.",
        "Class 12 from a recognised board.",
        "Usually 3 years; some institutions offer a 4-year programme.",
        "Social Work Practice, Community Development, Social Policy, Human Behaviour",
        "Apply through merit or university admission.",
        "Institution-specific admission requirements where applicable.",
        "Community Programme Assistant, Social Service Assistant, NGO Programme Support.",
        "M.S.W. and related postgraduate programmes."
    ),

    make_guidance_course(
        "B.A. Geography",
        "After 12th", "Arts", "Humanities",
        "A degree studying places, environments, populations and geographical patterns.",
        "Class 12 from a recognised board. Subject requirements vary.",
        "Usually 3 years; some institutions offer a 4-year programme.",
        "Physical Geography, Human Geography, Climatology, Cartography, GIS Basics",
        "Apply through merit or university admission.",
        "CUET or institution-specific entrance exams where applicable.",
        "Geography Research Assistant, GIS Assistant, Survey Support roles.",
        "M.A. Geography, GIS and related postgraduate courses."
    ),

    make_guidance_course(
        "B.A. Tamil Literature",
        "After 12th", "Arts", "Languages",
        "A degree studying Tamil language, classical literature and modern literary works.",
        "Class 12 from a recognised board. Tamil subject requirements vary by college.",
        "Usually 3 years; some institutions offer a 4-year programme.",
        "Tamil Grammar, Classical Literature, Modern Literature, Literary Criticism",
        "Apply through merit or university admission.",
        "Institution-specific entrance requirements where applicable.",
        "Tamil Language Educator, Content Writer, Editorial Assistant.",
        "M.A. Tamil, M.Phil. where offered, and Ph.D. programmes."
    ),

    # ======================================
    # DIPLOMA COURSES
    # ======================================

    make_guidance_course(
        "Diploma in Electrical and Electronics Engineering",
        "After 10th", "All Streams", "Diploma",
        "A technical programme covering electrical systems and electronic equipment.",
        "Class 10 pass or equivalent, subject to state and institution-specific rules.",
        "Usually 3 years.",
            "Electrical Engineering, Electronics, Circuit Theory, Electrical Machines, Power Systems.",
            "Apply through merit or state-level diploma admission process.",
            "State-level polytechnic entrance exams, where applicable.",
            "Electrical Technician, Junior Engineer, Maintenance Technician.",
            "B.E./B.Tech through lateral entry, or other higher diploma programmes."
        ),

    make_guidance_course(
        "Diploma in Electronics and Communication Engineering",
        "After 10th", "All Streams", "Diploma",
        "A technical programme covering electronic devices, communication systems and circuits.",
        "Class 10 pass or equivalent, subject to state and institution-specific rules.",
        "Usually 3 years.",
        "Electronic Devices, Digital Electronics, Communication Systems, Microprocessors.",
        "Apply through merit or state-level diploma admission process.",
        "State-level polytechnic entrance exams, where applicable.",
        "Electronics Technician, Communication Technician, Service Engineer.",
        "B.E./B.Tech through lateral entry or related higher studies."
    ),

    make_guidance_course(
        "Diploma in Automobile Engineering",
        "After 10th", "All Streams", "Diploma",
        "A programme focused on vehicle design, maintenance and automobile technology.",
        "Class 10 pass or equivalent, subject to state and institution-specific rules.",
        "Usually 3 years.",
        "Automobile Engines, Vehicle Systems, Workshop Technology, Automobile Design.",
        "Apply through merit or state-level diploma admission process.",
        "State-level polytechnic entrance exams, where applicable.",
        "Automobile Technician, Service Technician, Workshop Supervisor.",
        "B.E./B.Tech Automobile or Mechanical Engineering through lateral entry."
    ),

    make_guidance_course(
        "Diploma in Mechatronics Engineering",
        "After 10th", "All Streams", "Diploma",
        "Combines mechanical, electrical and electronic systems with automation.",
        "Class 10 pass or equivalent, subject to state and institution-specific rules.",
        "Usually 3 years.",
        "Mechanical Systems, Electronics, Robotics, Automation, Control Systems.",
        "Apply through merit or state-level diploma admission process.",
        "State-level polytechnic entrance exams, where applicable.",
        "Mechatronics Technician, Automation Technician, Maintenance Technician.",
        "B.E./B.Tech Mechatronics, Mechanical or related engineering."
    ),

    make_guidance_course(
        "Diploma in Chemical Engineering",
        "After 10th", "All Streams", "Diploma",
        "Introduces chemical processes, industrial production and plant operations.",
        "Class 10 pass or equivalent; science and mathematics requirements may vary.",
        "Usually 3 years.",
        "Chemical Process, Applied Chemistry, Fluid Mechanics, Plant Operations.",
        "Apply through merit or state-level diploma admission process.",
        "State-level polytechnic entrance exams, where applicable.",
        "Chemical Plant Technician, Process Assistant, Production Technician.",
        "B.E./B.Tech Chemical Engineering through lateral entry."
    ),

    make_guidance_course(
        "Diploma in Computer Science Engineering",
        "After 10th", "All Streams", "Diploma",
        "Covers computer hardware, software development and programming fundamentals.",
        "Class 10 pass or equivalent, subject to institution rules.",
        "Usually 3 years.",
        "Programming, Data Structures, Database Management, Networking, Web Technology.",
        "Apply through merit or state-level diploma admission process.",
        "State-level polytechnic entrance exams, where applicable.",
        "Junior Programmer, IT Support Technician, Web Developer.",
        "B.E./B.Tech Computer Science through lateral entry."
    ),

    make_guidance_course(
        "Diploma in Information Technology",
        "After 10th", "All Streams", "Diploma",
        "Focuses on software, computer networks, databases and information systems.",
        "Class 10 pass or equivalent, subject to institution rules.",
        "Usually 3 years.",
        "Programming, Networking, Database Systems, Web Development.",
        "Apply through merit or state-level diploma admission process.",
        "State-level polytechnic entrance exams, where applicable.",
        "IT Support Technician, Junior Developer, Network Technician.",
        "B.E./B.Tech Information Technology or related courses."
    ),

    make_guidance_course(
        "Diploma in Medical Laboratory Technology",
        "After 12th", "Science", "Medical Diploma",
        "Trains students in laboratory testing and medical sample analysis.",
        "12th pass with required science subjects; rules vary by institution.",
        "Usually 2 years.",
        "Clinical Biochemistry, Microbiology, Pathology, Laboratory Techniques.",
        "Apply through institution admission process.",
        "Entrance or merit-based admission as applicable.",
        "Medical Laboratory Technician, Lab Assistant.",
        "B.Sc MLT or related healthcare higher studies."
    ),

    make_guidance_course(
        "Diploma in Medical Imaging Technology",
        "After 12th", "Science", "Medical Diploma",
        "Introduces medical imaging equipment and diagnostic imaging procedures.",
        "12th pass with required science subjects; rules vary by institution.",
        "Usually 2 years.",
        "Radiographic Techniques, Imaging Physics, Anatomy, Patient Care.",
        "Apply through institution admission process.",
        "Entrance or merit-based admission as applicable.",
        "Imaging Technician, Radiology Assistant.",
        "B.Sc Medical Imaging Technology or related higher studies."
    ),

    make_guidance_course(
        "Diploma in Operation Theatre Technology",
        "After 12th", "Science", "Medical Diploma",
        "Prepares students to assist healthcare teams in operation theatre settings.",
        "12th pass with required science subjects; rules vary by institution.",
        "Usually 2 years.",
        "Operation Theatre Techniques, Anatomy, Infection Control, Patient Care.",
        "Apply through institution admission process.",
        "Entrance or merit-based admission as applicable.",
        "Operation Theatre Technician, Theatre Assistant.",
        "B.Sc Operation Theatre Technology or related higher studies."
    ),

    make_guidance_course(
        "Diploma in Dialysis Technology",
        "After 12th", "Science", "Medical Diploma",
        "Covers dialysis equipment, procedures and patient-care support.",
        "12th pass with required science subjects; rules vary by institution.",
        "Usually 2 years.",
        "Human Anatomy, Dialysis Technology, Medical Equipment, Patient Care.",
        "Apply through institution admission process.",
        "Entrance or merit-based admission as applicable.",
        "Dialysis Technician, Healthcare Assistant.",
        "B.Sc Dialysis Technology or related higher studies."
    ),

    make_guidance_course(
        "Diploma in Pharmacy",
        "After 12th", "Science", "Pharmacy Diploma",
        "Introduces medicines, pharmaceutical preparations and pharmacy practice.",
        "12th pass with Physics and Chemistry and Biology or Mathematics, subject to regulations.",
        "Usually 2 years.",
        "Pharmaceutics, Pharmacology, Pharmaceutical Chemistry, Pharmacy Practice.",
        "Apply through approved institution admission process.",
        "Merit or entrance-based admission as applicable.",
        "Pharmacy Assistant, Medical Store Assistant, Pharmacy Technician.",
        "B.Pharm through applicable lateral-entry rules."
    ),

    make_guidance_course(
        "Diploma in Fashion Design",
        "After 10th", "All Streams", "Design Diploma",
        "Develops skills in clothing design, textiles and fashion illustration.",
        "Class 10 or 12 pass depending on institution.",
        "Usually 1 to 3 years.",
        "Fashion Illustration, Textile Studies, Garment Construction, Design Basics.",
        "Apply through institution admission process.",
        "Portfolio or aptitude test where applicable.",
        "Fashion Assistant, Design Assistant, Boutique Assistant.",
        "Advanced Diploma or degree in Fashion Design."
    ),

    make_guidance_course(
        "Diploma in Interior Design",
        "After 10th", "All Streams", "Design Diploma",
        "Teaches planning and designing functional indoor spaces.",
        "Class 10 or 12 pass depending on institution.",
        "Usually 1 to 3 years.",
        "Space Planning, Design Drawing, Materials, Interior Styling.",
        "Apply through institution admission process.",
        "Aptitude test or portfolio where applicable.",
        "Interior Design Assistant, Drafting Assistant.",
        "Advanced Diploma or degree in Interior Design."
    ),

    make_guidance_course(
        "Diploma in Graphic Design",
        "After 10th", "All Streams", "Design Diploma",
        "Covers visual communication and digital graphic design.",
        "Class 10 or 12 pass depending on institution.",
        "Usually 1 to 2 years.",
        "Typography, Digital Illustration, Layout Design, Image Editing.",
        "Apply through institution admission process.",
        "Portfolio or aptitude test where applicable.",
        "Graphic Design Assistant, Visual Design Assistant.",
        "Advanced Diploma or degree in Graphic Design."
    ),

    make_guidance_course(
        "Diploma in Hotel Management",
        "After 10th", "All Streams", "Hospitality Diploma",
        "Introduces hotel operations, food service and hospitality management.",
        "Class 10 or 12 pass depending on institution.",
        "Usually 1 to 3 years.",
        "Food Production, Front Office, Housekeeping, Hospitality Operations.",
        "Apply through institution admission process.",
        "Merit or institution-level selection where applicable.",
        "Hotel Operations Assistant, Front Office Assistant.",
        "Advanced Diploma or degree in Hotel Management."
    ),

    make_guidance_course(
        "Diploma in Agriculture",
        "After 10th", "All Streams", "Diploma",
        "Introduces agricultural science, crop production and farming practices.",
        "Class 10 pass or equivalent, subject to state and institution rules.",
        "Usually 2 to 3 years.",
        "Crop Science, Soil Science, Horticulture, Agricultural Practices.",
        "Apply through state or institution admission process.",
        "Merit or entrance-based admission as applicable.",
        "Agriculture Assistant, Farm Supervisor, Field Assistant.",
        "B.Sc Agriculture or related higher studies, subject to eligibility."
    ),

    make_guidance_course(
        "Diploma in Web Designing",
        "After 10th", "All Streams", "Diploma",
        "Teaches the fundamentals of designing and developing websites.",
        "Class 10 or 12 pass depending on institution.",
        "Usually 6 months to 2 years.",
        "HTML, CSS, JavaScript, UI Design, Web Development.",
        "Apply through institution admission process.",
        "Usually merit or direct admission, depending on institution.",
        "Web Design Assistant, Frontend Developer Trainee.",
        "Advanced Diploma or degree in Computer Science or Design."
    ),

    # ==============================
    # ITI COURSES
    # ==============================

    make_guidance_course(
        "ITI Electrician",
        "After 10th", "All Streams", "ITI",
        "Provides practical training in electrical wiring, installation and maintenance.",
        "Usually Class 10 pass with required subjects, subject to trade rules.",
        "Usually 2 years.",
        "Electrical Wiring, Electrical Machines, Safety, Workshop Practice.",
        "Apply through the state ITI admission process.",
        "Merit-based selection or state-specific process.",
        "Electrician, Electrical Maintenance Assistant.",
        "Apprenticeship, advanced trade training or related diploma."
    ),

    make_guidance_course(
        "ITI Fitter",
        "After 10th", "All Streams", "ITI",
        "Provides practical training in fitting, assembly and maintenance work.",
        "Usually Class 10 pass, subject to trade rules.",
        "Usually 2 years.",
        "Workshop Calculation, Engineering Drawing, Fitting, Machine Tools.",
        "Apply through the state ITI admission process.",
        "Merit-based selection or state-specific process.",
        "Fitter, Assembly Technician, Maintenance Assistant.",
        "Apprenticeship or advanced trade training."
    ),

    make_guidance_course(
        "ITI Welder",
        "After 10th", "All Streams", "ITI",
        "Teaches basic welding processes and workshop safety.",
        "Usually Class 8 or 10 pass depending on trade rules.",
        "Usually 1 year.",
        "Welding Processes, Workshop Practice, Engineering Drawing, Safety.",
        "Apply through the state ITI admission process.",
        "Merit-based selection or state-specific process.",
        "Welder, Fabrication Assistant.",
        "Apprenticeship or advanced welding training."
    ),

    make_guidance_course(
        "ITI Computer Operator and Programming Assistant",
        "After 10th", "All Streams", "ITI",
        "Introduces computer operation, office applications and programming basics.",
        "Usually Class 10 pass, subject to trade rules.",
        "Usually 1 year.",
        "Computer Fundamentals, Office Applications, Internet, Programming Basics.",
        "Apply through the state ITI admission process.",
        "Merit-based selection or state-specific process.",
        "Computer Operator, Data Entry Assistant, Office Assistant.",
        "Advanced IT training or related diploma courses."
    )
]

# End of Student Guidance course list
# ==============================
# HOME PAGE
# ==============================

@app.route('/')
def home():
    return render_template('index.html')


# ==============================
# REGISTER
# ==============================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not all([name, email, password, confirm_password]):
            flash('Please fill in all fields.')
            return redirect(url_for('register'))

        if email in users:
            flash('Email already registered.')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('register'))

        users[email] = {
            'name': name,
            'password': generate_password_hash(password)
        }

        flash('Registration successful. Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')


# ==============================
# LOGIN
# ==============================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = users.get(email)

        if user and check_password_hash(user['password'], password):
            session['email'] = email
            session['name'] = user['name']

            flash('Login successful.')
            return redirect(url_for('dashboard'))

        flash('Invalid email or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


# ==============================
# DASHBOARD
# ==============================

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


# ==============================
# STUDENT GUIDANCE / CHOOSE GROUP
# ==============================

@app.route('/choose-group')
@app.route('/choose-group/course/<int:course_id>')
@login_required
def choose_group(course_id=None):

    selected_level = request.args.get('level', '')
    selected_stream = request.args.get('stream', '')
    selected_category = request.args.get('category', '')
    search_query = request.args.get('q', '').strip().lower()

    selected_course = None

    if course_id is not None:
        if 0 <= course_id < len(STUDENT_GUIDANCE_COURSES):
            selected_course = STUDENT_GUIDANCE_COURSES[course_id]

    indexed_courses = list(enumerate(STUDENT_GUIDANCE_COURSES))

    filtered_courses = []

    for index, course in indexed_courses:

        if selected_level and course['level'] != selected_level:
            continue

        if selected_stream and course['stream'] not in [selected_stream, 'All Streams']:
            continue

        if selected_category and course['category'] != selected_category:
            continue

        if search_query and search_query not in course['name'].lower():
            continue

        filtered_courses.append((index, course))

    return render_template(
        'choose_group.html',
        courses=filtered_courses,
        selected_course=selected_course,
        selected_level=selected_level,
        selected_stream=selected_stream,
        selected_category=selected_category,
        search_query=search_query
    )# ==============================
# SCHOLARSHIPS
# ==============================

@app.route('/scholarships')
@login_required
def scholarships():
    return render_template('scholarships.html')


# ==============================
# GOVERNMENT SCHEMES
# ==============================

@app.route('/schemes')
@login_required
def schemes():
    return render_template('schemes.html')


# ==============================
# ENTRANCE EXAMS
# ==============================

@app.route('/exams')
@login_required
def exams():
    return render_template('exams.html')


# ==============================
# STUDENT PROFILE
# ==============================

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    if request.method == 'POST':

        email = session.get('email')

        name = request.form.get('name', '').strip()
        qualification = request.form.get('qualification', '').strip()
        percentage_text = request.form.get('percentage', '').strip()
        skills = request.form.get('skills', '').strip()
        interest = request.form.get('interest', '').strip()
        preferred_course = request.form.get('preferred_course', '').strip()
        career_goal = request.form.get('career_goal', '').strip()
        school_sports_experience = request.form.get(
            'school_sports_experience', ''
        ).strip()

        if not all([
            name, qualification, percentage_text,
            skills, interest, preferred_course, career_goal
        ]):
            flash('Please fill in all required fields.')
            return redirect(url_for('profile'))

        try:
            percentage = float(percentage_text)

            if not 0 <= percentage <= 100:
                raise ValueError

        except ValueError:
            flash('Enter a valid percentage between 0 and 100.')
            return redirect(url_for('profile'))

        student_profiles[email] = {
            'name': name,
            'qualification': qualification,
            'percentage': percentage,
            'skills': skills,
            'interest': interest,
            'preferred_course': preferred_course,
            'career_goal': career_goal,
            'school_sports_experience': school_sports_experience
        }

        flash('Profile submitted successfully.')
        return redirect(url_for('dashboard'))

    return render_template('profile.html')


# ==============================
# LOGOUT
# ==============================

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))


# ==============================
# ERROR HANDLING
# ==============================

@app.errorhandler(404)
def page_not_found(error):
    return 'Page not found (404).', 404


@app.errorhandler(500)
def internal_server_error(error):
    return 'Internal server error (500).', 500


# ==============================
# RUN APPLICATION
# ==============================

if __name__ == '__main__':
    app.run(debug=True)