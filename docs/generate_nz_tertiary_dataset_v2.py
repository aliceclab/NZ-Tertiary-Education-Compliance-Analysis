"""
=============================================================================
New Zealand Tertiary Student Experience & SDR Compliance Analytics Engine
=============================================================================
"""
import random
import datetime
import pandas as pd
import numpy as np

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

N_STUDENTS = 6500
SURVEY_RESPONSE_RATE = 0.78
ACADEMIC_YEAR = 2024
REFERENCE_DATE = datetime.date(ACADEMIC_YEAR, 7, 1)
OUTPUT_DIR = "."
DOMESTIC_ONLY_FUNDING_CODE = "S05"

FIRST_NAMES_F = [
    "Aroha","Mere","Hine","Ngaio","Whina","Sophie","Emma","Olivia",
    "Charlotte","Mia","Isabella","Grace","Lily","Ava","Lucy","Chloe","Mei","Lin",
    "Wei","Aisha","Priya","Fatima","Maria","Leilani","Sina","Teuila","Moana","Amelia","Ruby"
]
FIRST_NAMES_M = [
    "Tama","Rangi","Wiremu","Hemi","Matiu","James","William","Oliver",
    "Noah","Lucas","Jack","Ethan","Mason","Liam","Logan","Henry","Caleb","Wei","Ming",
    "Raj","Amir","Sione","Tupou","Carlos","Miguel","Finn","Oscar","Leo","Sam","Ben","Max"
]
FIRST_NAMES_NB = [
    "Alex","Jordan","Taylor","Riley","Morgan","Quinn","Avery","Casey",
    "Jamie","Peyton","Reece","Sage","Skyler","Drew","Robin","Blake"
]
SURNAMES = [
    "Smith","Jones","Williams","Brown","Wilson","Taylor","Anderson","Thomas",
    "Walker","Harris","Martin","Thompson","Tūhoe","Ngāta","Parata","Te Hau","Māhaki",
    "Faleolo","Tuilagi","Fono","Seu","Latu","Ioane","Chen","Wang","Li","Zhang","Liu",
    "Nguyen","Patel","Singh","Kumar","Kim","Santos","Ferreira","Costa","Park","Sato",
    "O'Brien","Murphy","McCarthy","Fitzgerald","Sullivan","Stewart","Campbell","Fraser"
]


def _name(gender):
    if gender == "Female":
        pool = FIRST_NAMES_F
    elif gender == "Male":
        pool = FIRST_NAMES_M
    else:
        pool = FIRST_NAMES_NB
    return random.choice(pool), random.choice(SURNAMES)


COURSE_CATALOGUE = [
    ("BUS101", "Introduction to Business", "Business & Economics", 0.125, ["S02", "S03"]),
    ("BUS201", "Marketing Principles", "Business & Economics", 0.125, ["S02", "S03"]),
    ("BUS301", "Strategic Management", "Business & Economics", 0.125, ["S02", "S03"]),
    ("ACCT101", "Financial Accounting", "Business & Economics", 0.125, ["S02", "S03"]),
    ("ECON201", "Microeconomics", "Business & Economics", 0.125, ["S02", "S03"]),
    ("MBA501", "MBA Core", "Business & Economics", 0.250, ["S02", "S03", "S13"]),
    ("COMP101", "Introduction to Computing", "Science & Technology", 0.125, ["S02", "S03"]),
    ("COMP201", "Data Structures & Algorithms", "Science & Technology", 0.125, ["S02", "S03"]),
    ("COMP301", "Machine Learning", "Science & Technology", 0.125, ["S02", "S03"]),
    ("DATA201", "Data Analytics", "Science & Technology", 0.125, ["S02", "S03"]),
    ("STAT101", "Statistics I", "Science & Technology", 0.125, ["S02", "S03"]),
    ("ENGI301", "Engineering Systems", "Science & Technology", 0.250, ["S02", "S03", "S13"]),
    ("NURS101", "Foundations of Nursing", "Health Sciences", 0.250, ["S02", "S03", "S09"]),
    ("HLTH201", "Public Health", "Health Sciences", 0.125, ["S02", "S03", "S09"]),
    ("PHAR301", "Pharmacology", "Health Sciences", 0.125, ["S02", "S03"]),
    ("MIDW101", "Midwifery Practice I", "Health Sciences", 0.250, ["S02", "S09"]),
    ("SOCI101", "Sociology", "Arts & Social Sciences", 0.125, ["S02", "S03"]),
    ("PSYC101", "Psychology I", "Arts & Social Sciences", 0.125, ["S02", "S03"]),
    ("MAOR101", "Te Reo Māori I", "Arts & Social Sciences", 0.125, ["S02", "S03", "S05"]),
    ("HIST201", "New Zealand History", "Arts & Social Sciences", 0.125, ["S02", "S03"]),
    ("ENGL101", "Academic Writing", "Arts & Social Sciences", 0.125, ["S02", "S03"]),
    ("EDUC101", "Foundations of Education", "Education", 0.125, ["S02", "S03", "S05"]),
    ("EDUC301", "Curriculum Design", "Education", 0.125, ["S02", "S03", "S05"]),
    ("TEAC401", "Teaching Practicum", "Education", 0.250, ["S02", "S03", "S05"]),
    ("FDTN001", "Foundation Studies", "Foundation Studies", 0.250, ["S02", "S05", "S12"]),
    ("FDTN002", "Academic English", "Foundation Studies", 0.125, ["S02", "S05", "S12"]),
]
C2F = {c[0]: c[2] for c in COURSE_CATALOGUE}
C2E = {c[0]: c[3] for c in COURSE_CATALOGUE}
C2FC = {c[0]: c[4] for c in COURSE_CATALOGUE}
ALL_CC = [c[0] for c in COURSE_CATALOGUE]

ETH_OPT = ["NZ European", "Māori", "Pacific Peoples", "Asian", "MELAA", "Other", "Unknown/Not Stated"]
ETH_W = [0.48, 0.16, 0.09, 0.15, 0.03, 0.05, 0.04]
CIT_OPT = ["NZ Citizen", "NZ Permanent Resident", "International"]
CIT_W = [0.60, 0.15, 0.25]
GEN_OPT = ["Female", "Male", "Non-binary / Gender Diverse", "Not Stated"]
GEN_W = [0.52, 0.44, 0.025, 0.015]
THEMES = [
    "Enjoyed the hands-on learning approach",
    "Would appreciate more feedback on assessments",
    "Support services were very helpful",
    "Timetabling clashes made study difficult",
    "Great sense of community in my programme",
    "Library resources met my needs",
    "English language support was invaluable",
    "Felt isolated during online delivery",
    "Lecturers were approachable and knowledgeable",
    "Workload felt unmanageable at times",
    "Campus facilities are excellent",
    "Would benefit from more career guidance",
    "Cultural events helped me feel included",
    "Clear pathway to employment in my field",
    "Administrative processes were confusing",
    "Scholarship support made a real difference",
    "Course content felt outdated in places",
    "Strong industry connections in my programme",
]


ERR = []


def lerr(nsn_, record_type, error_code, description, related_key=""):
    ERR.append(
        {
            "NSN": nsn_,
            "Record_Type": record_type,
            "Error_Code": error_code,
            "Error_Description": description,
            "Related_Key": related_key,
        }
    )



def nsn(i):
    return str(1_000_000_000 + i)



def dob(citizenship):
    age = random.randint(18, 38) if citizenship == "International" else random.randint(17, 55)
    return REFERENCE_DATE - datetime.timedelta(days=age * 365 + random.randint(0, 364))



def ethnicity(citizenship):
    if citizenship == "International":
        return random.choices(["Asian", "MELAA", "Other", "Unknown/Not Stated"], [0.60, 0.10, 0.20, 0.10])[0]
    return random.choices(ETH_OPT, ETH_W)[0]



def courses(citizenship):
    n = random.choices([1, 2, 3, 4], [0.20, 0.40, 0.30, 0.10])[0]
    pool = [c for c in ALL_CC if c not in ("FDTN001", "FDTN002", "MIDW101")] if citizenship == "International" else ALL_CC
    return random.sample(pool, min(n, len(pool)))



def dom_fac(course_list):
    faculties = [C2F[c] for c in course_list]
    return max(set(faculties), key=faculties.count)



def dates(year, term):
    windows = {
        "T1": (datetime.date(year, 2, 20), datetime.date(year, 6, 14)),
        "T2": (datetime.date(year, 7, 8), datetime.date(year, 11, 8)),
        "T3": (datetime.date(year, 11, 11), datetime.date(year, 12, 20)),
        "FY": (datetime.date(year, 2, 20), datetime.date(year, 11, 8)),
    }
    start, end = windows.get(term, windows["T1"])
    return (
        start + datetime.timedelta(random.randint(-3, 3)),
        end + datetime.timedelta(random.randint(-3, 3)),
    )



def choose_funding_code(course_code, citizenship):
    options = list(C2FC[course_code])
    if citizenship == "International":
        options = [code for code in options if code != DOMESTIC_ONLY_FUNDING_CODE]
    return random.choice(options)



def make_bad_nsn(original_nsn, used_bad_nsns):
    while True:
        remove_pos = random.randint(0, len(original_nsn) - 1)
        bad_nsn = original_nsn[:remove_pos] + original_nsn[remove_pos + 1 :]
        if bad_nsn not in used_bad_nsns:
            used_bad_nsns.add(bad_nsn)
            return bad_nsn



def build_lear(n_students):
    print(f"  Building LEAR ({n_students:,} students)...")
    rows = []
    student_courses = {}

    for i in range(n_students):
        original_nsn = nsn(i)
        citizenship = random.choices(CIT_OPT, CIT_W)[0]
        course_list = courses(citizenship)
        student_courses[original_nsn] = course_list
        faculty_home = dom_fac(course_list)
        gender = random.choices(GEN_OPT, GEN_W)[0]
        first_name, surname = _name(gender)

        rows.append(
            {
                "NSN": original_nsn,
                "First_Name": first_name,
                "Surname": surname,
                "DOB": dob(citizenship).isoformat(),
                "Gender": gender,
                "Ethnicity": ethnicity(citizenship),
                "Citizenship_Status": citizenship,
                "Residency_Status": "International" if citizenship == "International" else "Domestic",
                "Faculty_Home": faculty_home,
                "Enrolment_Status": random.choices(["Enrolled", "Withdrawn", "Completed"], [0.72, 0.14, 0.14])[0],
                "Year_of_Study": random.choices([1, 2, 3, 4], [0.35, 0.30, 0.22, 0.13])[0],
                "Disability_Flag": random.choices(["Y", "N"], [0.08, 0.92])[0],
                "First_in_Family": random.choices(["Y", "N"], [0.32, 0.68])[0],
            }
        )

    df = pd.DataFrame(rows)
    rng = np.random.default_rng
    used_bad_nsns = set()

    for idx in rng(1).choice(len(df), 15, replace=False):
        original_nsn = df.at[idx, "NSN"]
        bad_nsn = make_bad_nsn(original_nsn, used_bad_nsns)
        lerr(original_nsn, "LEAR", "E01", f"NSN malformed to 9 digits (was {original_nsn})", f"NSN={bad_nsn}")
        df.at[idx, "NSN"] = bad_nsn
        student_courses[bad_nsn] = student_courses.pop(original_nsn)

    for idx in rng(2).choice(len(df), 20, replace=False):
        lerr(df.at[idx, "NSN"], "LEAR", "E02", "Ethnicity blank/missing")
        df.at[idx, "Ethnicity"] = ""

    for idx in rng(3).choice(len(df), 5, replace=False):
        future_dob = datetime.date(ACADEMIC_YEAR + random.randint(1, 5), random.randint(1, 12), random.randint(1, 28))
        lerr(df.at[idx, "NSN"], "LEAR", "E03", f"DOB after reference date {REFERENCE_DATE}: {future_dob}")
        df.at[idx, "DOB"] = future_dob.isoformat()

    for idx in rng(4).choice(len(df), 5, replace=False):
        under_16_dob = datetime.date(ACADEMIC_YEAR - random.randint(12, 15), random.randint(1, 12), random.randint(1, 28))
        lerr(df.at[idx, "NSN"], "LEAR", "E04", f"Student younger than 16 as at {REFERENCE_DATE} (DOB={under_16_dob})")
        df.at[idx, "DOB"] = under_16_dob.isoformat()

    for idx in rng(5).choice(len(df), 10, replace=False):
        lerr(df.at[idx, "NSN"], "LEAR", "E05", "Gender blank/missing")
        df.at[idx, "Gender"] = ""

    return df, student_courses



def build_enrl(lear_df, student_courses):
    print("  Building ENRL table...")
    rows = []
    terms = ["T1", "T2", "T3", "FY"]
    term_weights = [0.40, 0.38, 0.10, 0.12]

    for _, student in lear_df.iterrows():
        student_nsn = student["NSN"]
        citizenship = student["Citizenship_Status"]

        for course_code in student_courses.get(student_nsn, courses(citizenship)):
            term = random.choices(terms, term_weights)[0]
            start_date, end_date = dates(ACADEMIC_YEAR, term)
            rows.append(
                {
                    "NSN": student_nsn,
                    "Course_Code": course_code,
                    "Faculty": C2F[course_code],
                    "Academic_Year": ACADEMIC_YEAR,
                    "Term": term,
                    "Start_Date": start_date.isoformat(),
                    "End_Date": end_date.isoformat(),
                    "EFTS": C2E[course_code],
                    "Funding_Code": choose_funding_code(course_code, citizenship),
                    "Completion_Status": random.choices(["Passed", "Failed", "Withdrew", "In Progress"], [0.60, 0.10, 0.12, 0.18])[0],
                    "Delivery_Mode": random.choices(["On-campus", "Online", "Blended"], [0.55, 0.25, 0.20])[0],
                }
            )

    df = pd.DataFrame(rows).reset_index(drop=True)
    rng = np.random.default_rng

    for idx in rng(6).choice(len(df), 30, replace=False):
        start_date = datetime.date.fromisoformat(df.at[idx, "Start_Date"])
        bad_end_date = start_date - datetime.timedelta(random.randint(1, 30))
        lerr(df.at[idx, "NSN"], "ENRL", "E06", f"End_Date ({bad_end_date}) before Start_Date ({start_date})", df.at[idx, "Course_Code"])
        df.at[idx, "End_Date"] = bad_end_date.isoformat()

    overlap_nsns = [student_nsn for student_nsn, group in df.groupby("NSN") if len(group) >= 2][:40]
    overlap_rows = []
    for student_nsn in overlap_nsns:
        row_copy = df[df["NSN"] == student_nsn].iloc[0].copy()
        new_start = (datetime.date.fromisoformat(row_copy["Start_Date"]) + datetime.timedelta(random.randint(5, 20))).isoformat()
        new_end = (datetime.date.fromisoformat(row_copy["End_Date"]) - datetime.timedelta(random.randint(1, 10))).isoformat()
        row_copy["Start_Date"] = new_start
        row_copy["End_Date"] = new_end
        lerr(student_nsn, "ENRL", "E07", f"Overlapping enrolment same NSN in {row_copy['Term']}", row_copy["Course_Code"])
        overlap_rows.append(row_copy)
    if overlap_rows:
        df = pd.concat([df, pd.DataFrame(overlap_rows)], ignore_index=True)

    for idx in rng(8).choice(len(df), 20, replace=False):
        bad_efts = round(float(np.random.uniform(1.2, 2.5)), 3)
        lerr(df.at[idx, "NSN"], "ENRL", "E08", f"EFTS ({bad_efts}) exceeds max 1.0", df.at[idx, "Course_Code"])
        df.at[idx, "EFTS"] = bad_efts

    international_nsns = set(lear_df[lear_df["Citizenship_Status"] == "International"]["NSN"])
    e09_candidates = df[
        (df["NSN"].isin(international_nsns))
        & (df["Funding_Code"] != DOMESTIC_ONLY_FUNDING_CODE)
    ].index.tolist()
    for idx in rng(9).choice(e09_candidates, min(25, len(e09_candidates)), replace=False):
        lerr(df.at[idx, "NSN"], "ENRL", "E09", f"International student has domestic-only Funding_Code {DOMESTIC_ONLY_FUNDING_CODE}", df.at[idx, "Course_Code"])
        df.at[idx, "Funding_Code"] = DOMESTIC_ONLY_FUNDING_CODE

    duplicate_indices = rng(10).choice(len(df), 15, replace=False)
    duplicate_rows = df.iloc[duplicate_indices].copy()
    for _, row in duplicate_rows.iterrows():
        lerr(row["NSN"], "ENRL", "E10", "Exact duplicate enrolment row", row["Course_Code"])
    df = pd.concat([df, duplicate_rows], ignore_index=True)

    for idx in rng(11).choice(len(df), 15, replace=False):
        lerr(df.at[idx, "NSN"], "ENRL", "E11", "Faculty field blank/missing", df.at[idx, "Course_Code"])
        df.at[idx, "Faculty"] = ""

    return df.reset_index(drop=True)



def build_survey(lear_df):
    print("  Building SURVEY table...")
    rng2 = np.random.default_rng(SEED)
    respondents = lear_df.sample(int(len(lear_df) * SURVEY_RESPONSE_RATE), random_state=SEED).reset_index(drop=True)
    faculty_adjustments = {
        "Foundation Studies": (-1.2, -1.5),
        "Arts & Social Sciences": (-0.4, -0.5),
        "Health Sciences": (0.3, 0.2),
        "Business & Economics": (0.1, -0.1),
        "Science & Technology": (-0.2, 0.1),
        "Education": (0.4, 0.5),
    }
    rows = []

    for _, student in respondents.iterrows():
        citizenship = student["Citizenship_Status"]
        ethnic_group = student["Ethnicity"]
        disability_flag = student["Disability_Flag"]
        first_in_family = student["First_in_Family"]
        faculty = student["Faculty_Home"]
        teaching_adj, support_adj = faculty_adjustments.get(faculty, (0.0, 0.0))

        teaching_score = float(np.clip(rng2.normal(7.2, 1.4) + teaching_adj, 1, 10))
        support_score = float(np.clip(rng2.normal(6.8, 1.6) + support_adj, 1, 10))

        belonging_base = rng2.normal(6.5, 1.8)
        if ethnic_group in ("Māori", "Pacific Peoples"):
            belonging_base -= rng2.uniform(0.3, 0.8)
        if citizenship == "International":
            belonging_base -= rng2.uniform(0.2, 0.6)
        belonging_score = float(np.clip(belonging_base, 1, 10))

        admin_score = float(np.clip(rng2.normal(6.3, 1.9), 1, 10))
        retention_base = 0.35 * teaching_score + 0.30 * support_score + 0.20 * belonging_score + 0.15 * admin_score

        penalty = 0.0
        if citizenship == "International":
            penalty += rng2.uniform(0.3, 0.7)
        if ethnic_group == "Māori":
            penalty += rng2.uniform(0.2, 0.5)
        if ethnic_group == "Pacific Peoples":
            penalty += rng2.uniform(0.2, 0.5)
        if disability_flag == "Y":
            penalty += rng2.uniform(0.1, 0.4)
        if first_in_family == "Y":
            penalty += rng2.uniform(0.1, 0.3)
        if faculty == "Foundation Studies":
            penalty += rng2.uniform(0.2, 0.6)

        retention_likelihood = float(np.clip(retention_base - penalty + rng2.normal(0, 0.4), 1, 10))

        rows.append(
            {
                "NSN": student["NSN"],
                "Faculty": faculty,
                "Citizenship_Status": citizenship,
                "Ethnicity": student["Ethnicity"],
                "Gender": student["Gender"],
                "Year_of_Study": student["Year_of_Study"],
                "Disability_Flag": disability_flag,
                "First_in_Family": first_in_family,
                "Teaching_Score": round(teaching_score, 1),
                "Support_Score": round(support_score, 1),
                "Sense_of_Belonging": round(belonging_score, 1),
                "Admin_Experience": round(admin_score, 1),
                "Retention_Likelihood": round(retention_likelihood, 1),
                "Survey_Response_Flag": "Y",
                "Survey_Year": ACADEMIC_YEAR,
                "Free_Text_Theme": random.choice(THEMES),
            }
        )

    survey_df = pd.DataFrame(rows)
    print(f"    → {len(survey_df):,} survey responses generated.")
    return survey_df


if __name__ == "__main__":
    print("=" * 65)
    print("NZ Tertiary SDR Compliance & Student Experience Analytics Engine")
    print("=" * 65)

    lear_df, student_courses = build_lear(N_STUDENTS)
    lear_df.to_csv(f"{OUTPUT_DIR}/SDR_LEAR.csv", index=False)
    print(f"  ✓ SDR_LEAR.csv          ({len(lear_df):,} rows)")

    enrl_df = build_enrl(lear_df, student_courses)
    enrl_df.to_csv(f"{OUTPUT_DIR}/SDR_ENRL.csv", index=False)
    print(f"  ✓ SDR_ENRL.csv          ({len(enrl_df):,} rows)")

    survey_df = build_survey(lear_df)
    survey_df.to_csv(f"{OUTPUT_DIR}/STUDENT_SURVEY.csv", index=False)
    print(f"  ✓ STUDENT_SURVEY.csv    ({len(survey_df):,} rows)")

    errors_df = pd.DataFrame(ERR)
    errors_df.to_csv(f"{OUTPUT_DIR}/EXPECTED_ERRORS.csv", index=False)
    print(f"  ✓ EXPECTED_ERRORS.csv   ({len(errors_df):,} injected errors)")

    print()
    print("-" * 65)
    print("GENERATION SUMMARY")
    print("-" * 65)
    print(f"  Students (LEAR)       : {len(lear_df):,}")
    print(f"  Enrolment rows (ENRL) : {len(enrl_df):,}")
    print(f"  Survey responses      : {len(survey_df):,}")
    print(f"  Injected errors       : {len(errors_df):,}")
    print()
    print("  Error breakdown:")
    for code, group in errors_df.groupby("Error_Code"):
        print(f"    {code}: {len(group):>4}  — {group['Error_Description'].iloc[0][:55]}")
    print()
    print("  Avg Retention Likelihood by Faculty:")
    for faculty, score in survey_df.groupby("Faculty")["Retention_Likelihood"].mean().sort_values().round(2).items():
        print(f"    {faculty:<28} {score}")
    print()
    print("  Avg Retention Likelihood by Ethnicity:")
    for ethnic_group, score in survey_df.groupby("Ethnicity")["Retention_Likelihood"].mean().sort_values().round(2).items():
        print(f"    {ethnic_group:<28} {score}")
    print()
    print("=" * 65)
    print("All CSV files saved. Dataset ready. ✓")
    print("=" * 65)
