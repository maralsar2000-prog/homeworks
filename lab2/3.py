# 1
from datetime import datetime

data = [
    ("user_1", "LOGIN", ""),
    ("user_2", "LOGIN", ""),
    ("user_1", "BUY", 120),
    ("user_3", "LOGIN", ""),
    ("user_2", "BUY", 300),
    ("user_1", "BUY", 50),
    ("user_2", "LOGOUT", "")
]

with open("shop_logs.txt", "w", encoding="utf-8") as f:
    for name, action, summa in data:
        date = datetime.now().strftime("%Y-%m-%d")
        f.write(f"{date} | {name} | {action} | {summa}\n")

unique_users = set()
total_purchases = 0
total_amount = 0
user_spending = {}

with open("shop_logs.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        parts = line.split(" | ")

        if len(parts) < 3:
            continue

        date = parts[0]
        user_id = parts[1]
        action = parts[2]

        unique_users.add(user_id)

        if action == "BUY" and len(parts) == 4:
            amount = int(parts[3])
            total_purchases += 1
            total_amount += amount

        if user_id not in user_spending:
            user_spending[user_id] = 0
        user_spending[user_id] += amount

top_user = ""
max_spent = 0
for user in user_spending:
    if user_spending[user] > max_spent:
        max_spent = user_spending[user]
        top_user = user

average_check = total_amount / total_purchases if total_purchases else 0

with open("report.txt", "w", encoding="utf-8") as report:
    report.write(f"Уникальных пользователей: {len(unique_users)}\n")
    report.write(f"Всего покупок: {total_purchases}\n")
    report.write(f"Общая сумма: {total_amount}\n")
    report.write(f"Самый активный покупатель: {top_user}\n")
    report.write(f"Средний чек: {average_check:.2f}\n")

with open("report.txt", "r", encoding="utf-8") as report:
    print(report.read())

# 2
import csv

employees = []
with open("employees.csv", "r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        row["salary"] = int(row["salary"])
        employees.append(row)

total_salary = sum(emp["salary"] for emp in employees)
avg_salary = total_salary / len(employees)

print("Средняя зарплата:", avg_salary)

departments = {}

for emp in employees:
    dept = emp["department"]
    if dept not in departments:
        departments[dept] = []
    departments[dept].append(emp["salary"])

dept_averages = {}

for dept, salaries in departments.items():
    dept_avg = sum(salaries) / len(salaries)
    dept_averages[dept] = dept_avg
    print(f"Средняя зарплата в отделе {dept}: {dept_avg}")

highest_paid_dept = max(dept_averages, key=dept_averages.get)
print("Отдел с самой высокой средней зарплатой:", highest_paid_dept)

highest_paid_employee = max(employees, key=lambda x: x["salary"])
print("Самый высокооплачиваемый сотрудник:", highest_paid_employee["name"])

high_salary_employees = []

for emp in employees:
    if emp["salary"] > avg_salary:
        high_salary_employees.append(emp)

print("Сотрудники с зарплатой выше средней:")
for emp in high_salary_employees:
    print(emp["name"], emp["salary"])

with open("high_salary.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["name", "department", "salary"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(high_salary_employees)


#3
import json

orders_data= [
    {
        "order_id": 1,
        "user": "Ali",
        "items": ["phone", "case"],
        "total": 300000
    },
    {
        "order_id": 2,
        "user": "Dana",
        "items": ["laptop"],
        "total": 800000
    },
    {
        "order_id": 3,
        "user": "Ali",
        "items": ["mouse", "keyboard"],
        "total": 70000
    }
]

with open("orders.json", "w", encoding="utf-8") as f:
    json.dump(orders_data, f, ensure_ascii=False, indent=2)

with open("orders.json", "r", encoding="utf-8") as f:
    orders = json.load(f)

total_revenue = 0
user_orders = {}
item_counts = {}
max_order_total = 0
top_user = ""

for order in orders:
    total = order["total"]
    user = order["user"]
    items = order["items"]

    total_revenue += total

    if user in user_orders:
        user_orders[user] += 1
    else:
        user_orders[user] = 1

    if total > max_order_total:
        max_order_total = total
        top_user = user
    for item in items:
        if item in item_counts:
            item_counts[item] += 1
        else:
            item_counts[item] = 1

    max_count = 0
    most_popular_items = []

    for item in item_counts:
        count = item_counts[item]
        if count > max_count:
            max_count = count
            most_popular_items = [item]
        elif count == max_count:
            most_popular_items.append(item)

    total_orders = 0
    for user in user_orders:
        total_orders += user_orders[user]

summary= {
    "total_revenue": total_revenue,
    "top_user": top_user,
    "most_popular_item": most_popular_items,
    "total_orders": total_orders
}

with open("summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print("Общая сумма всех заказов:", summary["total_revenue"])
print("Пользователь с самым дорогим заказом:", summary["top_user"])
print("Самый популярный товар:", summary["most_popular_item"])
print("Общее количество заказов:", summary["total_orders"])