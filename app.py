from db import database

def main():
    db = database()
    db.init_db()

    print("\n[1] Generate a meal plan (default)")
    print("[2] Add a food")
    print("[3] List all foods")

    while True:
        choice = input("\nChoose action: ")

        if choice.strip() == "":
            meal_plan(db)
            continue
        elif choice.strip() == "1":
            meal_plan(db)
            continue
        elif choice.strip() == "2":
            add_food(db)
            continue
        elif choice.strip() == "3":
            list_foods(db)
            continue
        else:
            print("\nInvalid input...\n")

    db.close_db()

def meal_plan(db):
    print("\nmeal plan\n")

def add_food(db):
    print("\nadd food\n")

    name = input("Name: ")
    days_between = input("Days between: ")
    last_date = input("Last date (dd.mm.yyyy): ")

    db.add_food(name, days_between, last_date)


def list_foods(db):
    print("\nlist foods")

    foods = db.get_foods()

    for food_id, name, days_between, last_date in foods:
        ingredients = db.get_ingredients(food_id)
        print(f"\n{food_id}: {name} | Every {days_between} days | Last date: {last_date}")
        print(f"Ingredients: {ingredients}")

if __name__ == "__main__":
    main()