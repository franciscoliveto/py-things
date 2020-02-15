
annual_salary = float(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = float(input("Enter the cost of your dream house: "))
semi_annual_raise = float(input("Enter the semi-annual raise, as decimal: "))

portion_down_payment = 0.25 # 25%
annual_return = 0.04 # 4%

down_payment = total_cost * portion_down_payment

months = 0
current_savings = 0.0
while current_savings < down_payment:
    monthly_saved = (annual_salary / 12) * portion_saved
    current_savings += monthly_saved + current_savings*annual_return/12
    months += 1
    if months % 6 == 0:
        annual_salary += annual_salary * semi_annual_raise

print("Number of months:", months)
