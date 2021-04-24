from pysondb import db
from tabulate import tabulate
import sys
import json
from src import printcolors as pc

categories = db.getDb("categories.json")
expenses = db.getDb("expenses.json")
incomes = db.getDb("incomes.json")

def calculate_total_cost(_budget_query, _expenses_query, _id):
    budget = categories.getBy(_budget_query)
    for i in budget:
        budget = i["budget_total"]
    total_expenses = expenses.getBy(_expenses_query)
    amounts = [i.get("amount", None) for i in total_expenses]
    result = sum(map(int, amounts))
    cost_total = int(result)
    rest = int(budget) - int(result)
    if result == 0:
        cost_total = 0
    categories.updateById(_id, {"rest": rest})
    categories.updateById(_id, {"cost_total": cost_total})

def define_budget(budgeting):
    if budgeting == "1":
        rental_budget = input("How much is your rental budget?: $")
        categories.updateById(4274828660, {"budget_total": rental_budget})
    elif budgeting == "2":
        food_and_cleaning_budget = input(
            "How much is your expense in food/cleaning by month?: $")
        categories.updateById(4159738768, {"budget_total": food_and_cleaning_budget})
    elif budgeting == "3":
        credit_cards_budget = input("How much is your credit card debt?: $")
        categories.updateById(7131424278, {"budget_total": credit_cards_budget})
    elif budgeting == "4":
        travel_and_car = input(
            "How much is your expense in travel by month?: $")
        categories.updateById(9114973806, {"budget_total": travel_and_car})
    elif budgeting == "5":
        savings = input("How much do you save monthly?: $")
        categories.updateById(3175845475, {"budget_total": savings})
    elif budgeting == "6":
        others = input("Other expenses budget?: $")
        categories.updateById(5514952802, {"budget_total": others})
    elif budgeting == "7":
        calculate_total_cost({"name": "Rent"}, {"category": "Rent"}, 4274828660)
        calculate_total_cost({"name": "Food and Cleaning"}, {"category": "Food and Cleaning"}, 4159738768)
        calculate_total_cost({"name": "Credit Cards and Banks"}, {"category": "Credit Cards and Banks"}, 7131424278)
        calculate_total_cost({"name": "Traveling and Car"}, {"category": "Traveling and Car"}, 9114973806)
        calculate_total_cost({"name": "Savings"}, {"category": "Savings"}, 3175845475)
        calculate_total_cost({"name": "Others"}, {"category": "Others"}, 5514952802)
        print_table()
        input("Press any key... ")
        main()
    elif budgeting == "0":
        print("Go back...")
        main()
    else:
        print("The option is incorrect. Please select other option.")


def register_expense():
    category = input("""
Please select a category for register expense:

Categories:
¯¯¯¯¯¯¯¯¯¯¯
1) House rental 🏠
2) Food and cleaning 🍲
3) Credit cards 💳
4) Travel and car 🚗
5) Savings 💰
6) Others 📓

0) Go back
""")

    if category == "1":
        category = "Rent"
    elif category == "2":
        category = "Food and Cleaning"
    elif category == "3":
        category = "Credit Cards and Banks"
    elif category == "4":
        category = "Travel and Car"
    elif category == "5":
        category = "Savings"
    elif category == "6":
        category = "Others"
    elif category == "0":
        main()
    else:
        print("The option is incorrect, please insert a correct option")
        register_expense()
    cancel = input("""If you want abort input type "cancel", else press enter: """)
    if cancel == "cancel":
        main()
    date = input("""
Please insert the date of expense (MM/DD/YYYY):
""")
    amount = input("""
Please insert the amount of expense:
$""")
    description = input("""
Please insert the name of expense:
""")
    expenses.add({"category": category, "name": description, "date": date, "amount": amount})

def register_income():
    category = input("""
Please select a category for register income:

Categories:
¯¯¯¯¯¯¯¯¯¯¯
1) Salary 👷
2) Profit 📈
3) Other 🧮

0) Go back
""")

    if category == "1":
        category = "Salary"
    elif category == "2":
        category = "Profit"
    elif category == "3":
        category = "Other"
    elif category == "0":
        main()
    else:
        pc.printout("The option is incorrect, please select a correct option", pc.RED)
        register_income()

    date = input("""
Please insert the date of income (MM/DD/YYYY):
""")
    amount = input("""
Please insert the amount of income:
$""")
    description = input("""
Please insert a description of the income:
""")
    incomes.add({"category": category, "name": description, "date": date, "amount": amount})

def print_table():
    calculate_total_cost({"name": "Rent"}, {"category": "Rent"}, 4274828660)
    calculate_total_cost({"name": "Food and Cleaning"}, {"category": "Food and Cleaning"}, 4159738768)
    calculate_total_cost({"name": "Credit Cards and Banks"}, {"category": "Credit Cards and Banks"}, 7131424278)
    calculate_total_cost({"name": "Traveling and Car"}, {"category": "Traveling and Car"}, 9114973806)
    calculate_total_cost({"name": "Savings"}, {"category": "Savings"}, 3175845475)
    calculate_total_cost({"name": "Others"}, {"category": "Others"}, 5514952802)
    table = categories.getAll()
    for i in table:
        name_nk = "Name"
        name_ok = "name"
        i[name_nk] = i.pop(name_ok)
        budget_total_nk = "Total Budget"
        budget_total_ok = "budget_total"
        i[budget_total_nk] = i.pop(budget_total_ok)
        cost_total_nk = "Total Cost"
        cost_total_ok = "cost_total"
        i[cost_total_nk] = i.pop(cost_total_ok)
        rest_nk = "Rest"
        rest_ok = "rest"
        i[rest_nk] = i.pop(rest_ok)
    print("General status: ")
    print(tabulate(table, headers="keys", tablefmt="fancy_grid"))

def print_expenses_table():
    expenses_table = expenses.getAll()
    print(expenses_table)
    for i in expenses_table:
        category_nk = "Category"
        category_ok = "category"
        i[category_nk] = i.pop(category_ok)
        date_nk = "Date"
        date_ok = "date"
        i[date_nk] = i.pop(date_ok)
        name_nk = "Name"
        name_ok = "name"
        i[name_nk] = i.pop(name_ok)
        amount_nk = "Amount"
        amount_ok = "amount"
        i[amount_nk] = i.pop(amount_ok)
    print("Expenses history: ")
    print(tabulate(expenses_table, headers="keys", tablefmt="fancy_grid"))

def print_incomes_table():
    incomes_table = incomes.getAll()
    for i in incomes_table:
        category_nk = "Category"
        category_ok = "category"
        i[category_nk] = i.pop(category_ok)
        date_nk = "Date"
        date_ok = "date"
        i[date_nk] = i.pop(date_ok)
        name_nk = "Name"
        name_ok = "name"
        i[name_nk] = i.pop(name_ok)
        amount_nk = "Amount"
        amount_ok = "amount"
        i[amount_nk] = i.pop(amount_ok)
    print("Incomes history: ")
    print(tabulate(incomes_table, headers="keys", tablefmt="fancy_grid"))

parraf = """
Actions:
¯¯¯¯¯¯¯¯
1) Define budget 💸
2) Register expense 😥
3) Register income 🤑
4) Check general status ✅
5) Check expenses history ✅
6) Check incomes history ✅
7) Reset database 🔂
0) Exit 👋

Type here 🤜  """


def main():
    pc.printout("""

 ███████████             ██████████
░░███░░░░░███           ░░███░░░░░█
 ░███    ░███ █████ ████ ░███  █ ░  █████ █████ ████████   ██████  ████████    █████   ██████
 ░██████████ ░░███ ░███  ░██████   ░░███ ░░███ ░░███░░███ ███░░███░░███░░███  ███░░   ███░░███
 ░███░░░░░░   ░███ ░███  ░███░░█    ░░░█████░   ░███ ░███░███████  ░███ ░███ ░░█████ ░███████
 ░███         ░███ ░███  ░███ ░   █  ███░░░███  ░███ ░███░███░░░   ░███ ░███  ░░░░███░███░░░
 █████        ░░███████  ██████████ █████ █████ ░███████ ░░██████  ████ █████ ██████ ░░██████
░░░░░          ░░░░░███ ░░░░░░░░░░ ░░░░░ ░░░░░  ░███░░░   ░░░░░░  ░░░░ ░░░░░ ░░░░░░   ░░░░░░
               ███ ░███                         ░███
              ░░██████                          █████
               ░░░░░░                          ░░░░░

Py Expense is a python command line tool for expense tracking.

Github @joelperedaok
Twitter @joelpereda
----------------------------------------------------------------------------------------------
""", pc.BLUE)
    print("\nPlease select an action from the menu:")

    while True:
        table = categories.getAll()
        menu_option = input(parraf)
        if menu_option == "1":
            budgeting = input("""
Please select a category for define budget:

Categories:
¯¯¯¯¯¯¯¯¯¯¯
1) House rental 🏠
2) Food and cleaning 🍲
3) Credit cards 💳
4) Travel and car 🚗
5) Savings 💰
6) Others 📓

7) Check table ✅
0) Go back ↩

Type here 🤜  """)
            define_budget(budgeting)
        elif menu_option == "2":
            register_expense()
        elif menu_option == "3":
            register_income()
        elif menu_option == "4":
            print_table()
            input("Press any key... ")
            main()
        elif menu_option == "5":
            print_expenses_table()
        elif menu_option == "6":
            print_incomes_table()
        elif menu_option == "7":
            pc.printout("""\nSorry, for reset database you must do it manually in .json files.
The .json must be: {"data": []}\n""", pc.RED)
        elif menu_option == "0":
            pc.printout("\nGoodbye!\n", pc.RED)
            sys.exit()
        else:
            pc.printout("\nThe option is incorrect, please select a correct option\n", pc.RED)

if __name__ == "__main__":
    main()
