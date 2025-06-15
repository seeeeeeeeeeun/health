def predict_medical_cost(gender, age, hospital, diagnosis, treatment):
    base_cost = 150000
    if "수술" in treatment:
        base_cost += 800000
    elif "진료" in treatment:
        base_cost += 30000
    insurance = "Y" if gender == "F" else "N"
    deductible = int(base_cost * 0.2)
    return base_cost, insurance, deductible
