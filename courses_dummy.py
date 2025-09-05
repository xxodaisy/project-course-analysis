# -- IMPORT THE LIBRARIES --
import pandas as pd
import numpy as np
from faker import Faker
import random
import uuid
from datetime import datetime, timedelta, time
from sqlalchemy import create_engine, text
import os 
from dotenv import load_dotenv

# --- LOAD ENV ---
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

fake = Faker('id_ID')

# --- HELPER ---
def normalize_date(dt):
    if isinstance(dt, datetime):
        return dt
    return datetime.combine(
        dt,
        time(
            hour=random.randint(0, 23),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        )
    )


# --- PARAMETER ---
NUM_USERS = 5_000
NUM_VOUCHERS = 10_000
NUM_ORDERS = 5_000
TARGET_TX = 15_000
VOUCHER_USAGE_RATE = 0.5
COURSES_PER_ORDER = (1, 3)

# -- USERS --
majors = [
    "Teknik Informatika", "Ilmu Komputer", "Bisnis", "Teknik Elektro", "Teknik Mesin", "Teknik Sipil", "Akuntansi", 
    "Manajemen", "Hukum", "Kedokteran", "Farmasi", "Psikologi", "Ilmu Komunikasi", "Arsitektur", "Teknik Kimia", 
    "Teknik Industri", "Sastra Inggris", "Sastra Indonesia", "Matematika", "Statistika", "Fisika", "Biologi", "Kimia"
]
major_occupation_mapping = {
    "Teknik Informatika": ["Software Engineer", "Data Scientist", "Web Developer", "System Analyst"],
    "Ilmu Komputer": ["Software Developer", "AI Specialist", "IT Consultant", "Network Engineer"],
    "Bisnis": ["Business Analyst", "Marketing Manager", "Entrepreneur", "Financial Advisor"],
    "Teknik Elektro": ["Electrical Engineer", "Electronics Technician", "Power Systems Engineer"],
    "Teknik Mesin": ["Mechanical Engineer", "Automotive Engineer", "HVAC Engineer"],
    "Teknik Sipil": ["Civil Engineer", "Construction Manager", "Structural Engineer"],
    "Akuntansi": ["Accountant", "Auditor", "Tax Consultant", "Financial Analyst"],
    "Manajemen": ["Project Manager", "HR Manager", "Operations Manager", "Business Consultant"],
    "Hukum": ["Lawyer", "Legal Advisor", "Judge", "Notary"],
    "Kedokteran": ["Doctor", "Surgeon", "General Practitioner", "Medical Researcher"],
    "Farmasi": ["Pharmacist", "Pharmaceutical Researcher", "Clinical Pharmacist"],
    "Psikologi": ["Psychologist", "Counselor", "Clinical Therapist", "HR Specialist"],
    "Ilmu Komunikasi": ["Journalist", "Public Relations Officer", "Content Creator", "Media Planner"],
    "Arsitektur": ["Architect", "Interior Designer", "Urban Planner"],
    "Teknik Kimia": ["Chemical Engineer", "Process Engineer", "Petroleum Engineer"],
    "Teknik Industri": ["Industrial Engineer", "Quality Control Manager", "Supply Chain Analyst"],
    "Sastra Inggris": ["Translator", "English Teacher", "Content Writer"],
    "Sastra Indonesia": ["Writer", "Editor", "Journalist"],
    "Matematika": ["Mathematician", "Data Analyst", "Actuary"],
    "Statistika": ["Statistician", "Data Scientist", "Market Researcher"],
    "Fisika": ["Physicist", "Researcher", "Astronomer"],
    "Biologi": ["Biologist", "Microbiologist", "Environmental Scientist"],
    "Kimia": ["Chemist", "Chemical Analyst", "Lab Technician"]
}
low_education_occupations = ["Student", "Freelancer", "Cashier", "Waiter/Waitress", "Sales Assistant", "Driver"]

def generate_email(first_name, last_name):
    email_local_part = f"{first_name.lower()}.{last_name.lower()}"
    if random.random() < 0.2:
        email_local_part += str(random.randint(1, 99))
    domain = fake.free_email_domain()
    return f"{email_local_part}@{domain}"

#age group and weights 
age_groups = {
    "Under 20": (17,19),
    "20-29": (20,29),
    "30-39": (30-39),
    "40-49": (40,49),
    "50+": (50,60)
}

#bobot distributions
weights = {
    "Under 20": 0.10,
    "20-29": 0.35,
    "30-39": 0.35,
    "40-49": 0.15,
    "50+": 0.05
}

def generate_age():
    group = np.random.choice(list(age_groups.keys()), p=list(weights.values()))
    low, high = age_groups[group]
    return random.randint(low, high)

users = []
for _ in range(10000):
    education = random.choice(["Middle School", "High School", "Bachelor", "Master", "PhD"])
    if education in ["Bachelor", "Master", "PhD"]:
        major = random.choice(majors)
        occupation = random.choice(major_occupation_mapping[major])
    else:
        major = None
        occupation = random.choice(low_education_occupations)
    gender = random.choice(["Male", "Female"])
    first_name = fake.first_name_male() if gender == "Male" else fake.first_name_female()
    last_name = fake.last_name()
    full_name = f"{first_name} {last_name}"
    email = generate_email(first_name, last_name)
    username = f"{first_name.lower()}_{last_name.lower()}"
    users.append({
        "user_id": str(uuid.uuid4()), #pake uuid.uuid4()
        "user_name": username,
        "name": full_name,
        "age": generate_age,
        "gender": gender,
        "email": email,
        "phone_number": fake.phone_number(),
        "occupation": occupation,
        "region": fake.city_name(),
        "education": education,
        "major": major
    })
users_df = pd.DataFrame(users)

# -- COURSES --
category_courses = {
    "Data": [
        "Python for Data Science", "Python for Software Engineering", "NLP Analysis", "Linear Regression Analysis",
        "Machine Learning Basics", "SQL for Data Analyst", "Learn SPSS from Beginner to Advance", "Google Data Studio Course",
        "Excel: Data Cleaning and Analysis Techniques", "Business Analysis Fundamental", "Data Warehouse Fundamental for Beginners",
        "Data Analytics with R", "Power BI fundamental", "Tableau for Business Intelligence", "Web Scraping using BeautifulSoup",
        "Google Analytics", "Business Analysis Modelling", "ETL pipeline for Data Engineer", "AI & Deep Learning with TensorFlow",
        "Data Visualization with Python", "Data Science Capstone Project", "Big Data Analysis with Hadoop", "Apache Spark for Data Engineers",
        "Time Series Analysis with Python", "Data Governance & Quality Management"
    ],
    "Cloud Computing": [
        "Introduction to Cloud Computing", "AWS Certified Cloud Practitioner - AWS Certification", "AWS Fundamental",
        "Google Cloud Essentials", "Azure for DevOps", "Google Cloud Certification", "Microsoft Azure: Hands On Training: AZ-900",
        "Cloud Security Essentials", "Kubernetes for Beginners", "Cloud Automation with Terraform", "Cloud Cost Optimization Strategies",
        "Serverless Architecture with AWS Lambda", "Multi-Cloud Deployment Strategies", "Advanced Cloud Networking"
    ],
    "Web Development": [
        "Full Stack Webdev", "React & Node.js", "REST API for Backend Developer", "Selenium Webdriver with Java (Basic to Advance)",
        "Learn Programming with .NET Course", "AngularJS Course: Beginner to Advance", "JavaScript for Beginner",
        "Java Spring Boot Course: from Beginner to Advance", "C# for Backend Developer", "Vue.js Essentials",
        "Responsive Web Design with HTML and CSS", "Building Modern Websites with Next.js"
    ],
    "Business": [
        "Marketing Analysis", "Financial Analysis", "Project Management", "Agile Project Management: Include Scrum and Kanban",
        "How to be Product Manager", "B2B Sales Analytics", "Business Development", "Digital Marketing Strategy",
        "Introduction to Entrepreneurship", "Leadership and Team Management"
    ],
    "Mobile Development": [
        "Android App Development with Kotlin", "iOS App Development with Swift", "Flutter for Beginners",
        "React Native: Build Mobile Apps", "Advanced Android Architecture", "Mobile App Deployment & CI/CD",
        "Building Mobile APIs", "Mobile UI/UX Design Principles", "Cross-Platform Performance Optimization", "Testing Mobile Apps with Appium"
    ],
    "Design & UI/UX": [
        "UI/UX Design with Figma", "Adobe XD for Beginner", "Graphic Design with Canva",
        "Design Thinking Workshop", "UX Research & Prototyping", "Web & App Accessibility Design",
        "Advanced Interaction Design", "Visual Design for Product Managers"
    ],
    "Cybersecurity":[
        "Ethical Hacking Fundamental", "Network Security Basics", "SOC Analyst Training", "Zero Trust Architecture",
        "Cybersecurity for Cloud Platforms", "Incident Response & Forensics", "Penetration Testing with Kali Linux",
        "OWASP Top 10 for Web Developers", "Ransomware Defense Strategies", "Data Ethics & Privacy Management", "Cloud Incident Response Playbook"
    ],
    "Soft Skills & Productivity":[
        "Effective Business Communication", "Negotiation Skills for Professionals", "Public Speaking & Presentation Mastery",
        "Time Management for Busy People", "Critical Thinking & Problem Solving", "Emotional Intelligence at Work",
        "Remote Team Collaboration Tools", "Conflict Resolution in the Workplace", "Advance Problem-Solving for Leaders", "Creative Thinking & Innovation"
    ]
}

all_courses = [(c, cat) for cat, courses in category_courses.items() for c in courses]
courses = [{
    "course_id": str(uuid.uuid4()), #pake uuid.uuid4
    "course_name": name,
    "category": cat,
    "price": random.choice([100_000, 150_000, 200_000, 250_000, 300_000]),
    "duration_days": random.randint(7, 90)
} for name, cat in all_courses]

courses_df = pd.DataFrame(courses)

# -- VOUCHERS --
today = datetime.now()
vouchers = []
for _ in range(NUM_VOUCHERS):
    user = random.choice(users)
    start_date = normalize_date(fake.date_between(start_date="-1y", end_date="today"))
    end_date = normalize_date(start_date + timedelta(days=random.randint(30, 120)))
    status = "Upcoming" if today < start_date else "Active" if start_date <= today <= end_date else "Expired"
    vouchers.append({
        "voucher_id": str(uuid.uuid4()),
        "user_id": user["user_id"],
        "voucher_code": fake.bothify(text="VOUCHER-####"),
        "discount_percent": random.choice([10, 20, 30, 40, 50, 60, 70, 80]),
        "status": status,
        "start_date": start_date,
        "end_date": end_date
    })
vouchers_df = pd.DataFrame(vouchers)

# -- ORDERS --
orders = []
for _ in range(NUM_ORDERS):
    user = random.choice(users)
    order_date = normalize_date(fake.date_between(start_date="-1y", end_date="today"))
    orders.append({
        "order_id": str(uuid.uuid4()),
        "user_id": user["user_id"],
        "order_date": order_date,
        "status": random.choice(["Pending", "Completed", "Refunded", "Canceled"]),
        "payment_method": random.choice(["Bank Transfer", "Gopay", "OVO", "Dana", "Jago","linkaja", "qris", "Shopeepay" ]),
        "total_price": 0
    })
orders_df = pd.DataFrame(orders)

# --- ORDER DETAILS / REDEMPTION / COMPLETION ---
order_details, redemption, completion = [], [], []

for _, order in orders_df.iterrows():
    num_courses = random.randint(*COURSES_PER_ORDER)
    selected_courses = courses_df.sample(num_courses)

    for _, course in selected_courses.iterrows():
        voucher = vouchers_df.sample(1).iloc[0] if random.random() < VOUCHER_USAGE_RATE else None
        price = course["price"]
        discount = voucher["discount_percent"] if voucher is not None else 0
        final_price = price - (price * discount / 100)

        voucher_date = normalize_date(order["order_date"] + timedelta(days=random.randint(0, 2))) if voucher is not None else None
        redemption_date = normalize_date(voucher_date + timedelta(days=random.randint(1, 3))) if voucher_date else None
        enrollment_date = normalize_date((redemption_date or order["order_date"]) + timedelta(days=random.randint(1, 10)))
        # completion_status = random.choice(["Completed", "In Progress", "Not Started", "Not Completed"])
        # completion_date = normalize_date(enrollment_date + timedelta(days=random.randint(7, 90))) if completion_status == "Completed" else None

        order_detail_id = str(uuid.uuid4())
        order_details.append({
            "order_detail_id": order_detail_id,
            "order_id": order["order_id"],
            "course_id": course["course_id"],
            "voucher_id": voucher["voucher_id"] if voucher is not None else None,
            "voucher_date": voucher_date,
            "price": price,
            "discount_percent": discount,
            "final_price": final_price,
            "enrollment_date": enrollment_date
        })

        if voucher is not None:
            start, end = normalize_date(voucher['start_date']), normalize_date(voucher['end_date'])
            if redemption_date and start <= redemption_date <= end:
                redemption_status = "Used"
            elif redemption_date and redemption_date > end:
                redemption_status = "Expired"
            else:
                redemption_status = "Invalid"
        else:
            redemption_status = "No Redeem"
            redemption_date = None
        
        if redemption_status in ["Expired", "Invalid"]:
            completion_status = "Not Completed"
            completion_date = None
        else:
            completion_status = random.choice(["Completed", "In Progress", "Not Started"])
            completion_date = (
                normalize_date(enrollment_date + timedelta(days=random.randint(7,90)))
            )    if completion_status == "Completed" else None
            

        redemption.append({
            "redemption_id": str(uuid.uuid4()),
            "order_detail_id": order_detail_id,
            "voucher_id": voucher["voucher_id"] if voucher is not None else None,
            "redemption_date": redemption_date,
            "redemption_status": redemption_status
        })

        completion.append({
            "completion_id": str(uuid.uuid4()),
            "order_detail_id": order_detail_id,
            "completion_status": completion_status,
            "completion_date": completion_date
        })

order_details_df = pd.DataFrame(order_details)
redemption_df = pd.DataFrame(redemption)
completion_df = pd.DataFrame(completion)

# --- UPDATE TOTAL PRICE ---
order_totals = order_details_df.groupby("order_id")["final_price"].sum().reset_index()
orders_df = orders_df.merge(order_totals, on="order_id", how="left")
orders_df["total_price"] = orders_df["final_price"].fillna(0)
orders_df.drop(columns=["final_price"], inplace=True)

# -- list of tables whose contents you want to refresh
tables_to_refresh = ["redemption", "completion", "order_details", "orders", "vouchers", "users"]

#-- delete old data from table
with engine.begin() as conn:
    for table in tables_to_refresh:
        conn.execute(text(f"DELETE FROM {table}"))

# -- SAVE TO DATABASE --
users_df.to_sql("users", engine, if_exists="append", index=False)
courses_df.to_sql("courses", engine, if_exists="append", index=False)
vouchers_df.to_sql("vouchers", engine, if_exists="append", index=False)
orders_df.to_sql("orders", engine, if_exists="append", index=False)
order_details_df.to_sql("order_details", engine, if_exists="append", index=False)
redemption_df.to_sql("redemption", engine, if_exists="append", index=False)
completion_df.to_sql("completion", engine, if_exists="append", index=False)
print("Dummy data created successfully!")
