import random
from datetime import datetime, timedelta
import pandas as pd

random.seed(42)

# ---------- CONFIG ----------
num_records = 1500
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)

departments = ["Cardiology", "Neurology", "Orthopedics", "Pediatrics", "Oncology", "Emergency"]
genders = ["Male", "Female"]
payment_modes = ["Cash", "Card", "Insurance", "UPI"]

doctor_map = {
    "Cardiology": ["Dr. Sharma", "Dr. Reddy"],
    "Neurology": ["Dr. Mehta", "Dr. Kumar"],
    "Orthopedics": ["Dr. Singh", "Dr. Patel"],
    "Pediatrics": ["Dr. Rao", "Dr. Das"],
    "Oncology": ["Dr. Khan", "Dr. Iyer"],
    "Emergency": ["Dr. Ali", "Dr. Verma"]
}

diagnosis_map = {
    "Cardiology": ["Heart Attack", "Arrhythmia"],
    "Neurology": ["Stroke", "Migraine"],
    "Orthopedics": ["Fracture", "Arthritis"],
    "Pediatrics": ["Fever", "Infection"],
    "Oncology": ["Cancer", "Tumor"],
    "Emergency": ["Accident", "Trauma"]
}

# ---------- GENERATE DATA ----------
data = []
date_range_days = (end_date - start_date).days

for i in range(1, num_records + 1):

    dept = random.choice(departments)
    doctor = random.choice(doctor_map[dept])
    diagnosis = random.choice(diagnosis_map[dept])

    admission_date = start_date + timedelta(days=random.randint(0, date_range_days))
    stay_days = random.randint(1, 10)
    discharge_date = admission_date + timedelta(days=stay_days)

    age = random.randint(1, 90)
    gender = random.choice(genders)
    payment = random.choice(payment_modes)

    # realistic cost logic
    base = random.randint(20000, 100000)
    expense = int(base * random.uniform(0.5, 0.8))
    revenue = int(base * random.uniform(1.0, 1.5))

    data.append({
        "Patient_ID": i,
        "Patient_Name": f"Patient_{i}",
        "Age": age,
        "Gender": gender,
        "Department": dept,
        "Doctor_Name": doctor,
        "Diagnosis": diagnosis,
        "Admission_Date": admission_date.strftime("%Y-%m-%d"),
        "Discharge_Date": discharge_date.strftime("%Y-%m-%d"),
        "Length_of_Stay": stay_days,
        "Bed_Number": random.randint(1, 200),
        "Payment_Mode": payment,
        "Revenue": revenue,
        "Expense": expense,
        "Profit": revenue - expense
    })

df = pd.DataFrame(data)
df = df.sort_values("Admission_Date").reset_index(drop=True)

# ---------- SAVE ----------
df.to_csv("data/hospital_data.csv", index=False)

print("Dataset created successfully!")
print("Rows:", len(df))
print(df.head())