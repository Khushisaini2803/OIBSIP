
# Oasis Infobyte Python Internship
# Task 1: BMI Calculator
name = input("Enter your name: ").strip()
if not name:
    print("Error: Name cannot be empty.")
while True:
    try:
        weight = float(input("Enter your weight in kg: "))
        height = float(input("Enter your height in meters: "))
        if weight <= 0 or height <=0:
            print("Error:Weight and height must be greater than zero.")
            continue
        break
    except ValueError:
        print("Error: Please enter numbers only. Try again.")
                  

if weight <= 0 or height <= 0:
    print("Error: Weight and height must be greater thyan zero:")
else:
    bmi = weight / (height ** 2)
    print("\n----- BMI calculator -----")
    print("Name:", name)
    print("Your BMI is:", round(bmi, 2))
    if bmi < 18.5:
        print("Category: Underweight")
    elif bmi < 25:
        print("Category: Normal weight")
    elif bmi < 30:
        print("Category: Overweight")
    else:
        print("Category: Obesity")

print("Name:", name)
print("Your BMI is:", round(bmi, 2))
print("Bmi is a general screening measure, not a diagnosis.")

if bmi < 18.5:
    print("Category: Underweight")
elif bmi < 25:
    print("Category: Normal weight")
elif bmi < 30:
    print("Category: Overweight")
else:
    print("Category: Obesity")
