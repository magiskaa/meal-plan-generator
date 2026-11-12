from db import database
from datetime import date, datetime, timedelta

def main():
    db = database()
    db.init_db()

    print("\n[1] Generate a meal plan (default)")
    print("[2] Add a food")
    print("[3] List all foods")
    print("[t] Test")
    print("[q] Quit")

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
        elif choice.strip() == "q":
            db.close_db()
            break
        elif choice.strip() == "t":
            test(db)
            continue
        else:
            print("\nInvalid input...\n")

def test(db):
    foods = db.get_foods()
    day = date.today() + timedelta(days=-30)
    for food_id, name, days_between, last_date in foods:
        db.update_food(day.strftime("%d.%m.%Y"), food_id)


def meal_plan(db):
    print("\nmeal plan\n")

    today = date.today()
    complete_meal_plan = []
    for i in range(1, 8):
        day = today + timedelta(days=i)
        foods = db.get_foods()
        eligible_foods = []
        
        for food_id, name, days_between, last_date in foods:
            if last_date:
                last_date_obj = datetime.strptime(last_date, "%d.%m.%Y").date()
                days_since = (day - last_date_obj).days
            else:
                days_since = 100

            if days_since >= int(days_between):
                eligible_foods.append({
                    "id": food_id,
                    "name": name,
                    "days_between": days_between,
                    "last_date": day.strftime("%d.%m.%Y"),
                    "days_since": days_since
                })

        chosen_food = max(eligible_foods, key=lambda food: food["days_since"])
        complete_meal_plan.append(chosen_food)
        db.update_food(day.strftime("%d.%m.%Y"), chosen_food["id"])

    weekdays = ["Ma", "Ti", "Ke", "To", "Pe", "La", "Su"]
    for i, meal in enumerate(complete_meal_plan):
        print(f"{weekdays[i]}: {meal["name"]}")
    

def add_food(db):
    print("\nadd food\n")

    name = input("Name: ")
    days_between = input("Days between: ")
    last_date = input("Last date (dd.mm.yyyy): ")
    ingredients = input("Ingredients (separated by a comma): ")

    id = db.add_food(name.strip(), days_between.strip(), last_date.strip())
    ingredient_list = ingredients.split(",")
    for i in ingredient_list:
        db.add_ingredient(id, i.strip())


def list_foods(db):
    print("\nlist foods")

    foods = db.get_foods()
    for food_id, name, days_between, last_date in foods:
        ingredients = db.get_ingredients(food_id)
        print(f"\n{food_id}: {name} | Every {days_between} days | Last date: {last_date}")
        print(f"Ingredients: {", ".join(row[0] for row in ingredients)}")

if __name__ == "__main__":
    main()