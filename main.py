#!/usr/bin/env python3

import requests
import datetime
import re

BASE_URL = "https://kitchen.kanttiinit.fi"

AREAS_URL = f"{BASE_URL}/areas?idsOnly=1&lang=fi"
MENUS_URL = f"{BASE_URL}/menus?lang=fi&restaurants=&days={{date}}"
RESTAURANTS_ALL_URL = f"{BASE_URL}/restaurants?lang=fi&priceCategories=student,studentPremium"
RESTAURANTS_BY_IDS_URL = f"{BASE_URL}/restaurants?lang=fi&ids={{ids}}&priceCategories=student,studentPremium"

AREA_ALIASES = {
    "stadi": "Helsingin keskusta",
    "kumpula": "Arabia & Kumpula",
    "aalto": "Otaniemi",
    "ay": "Otaniemi",
    "hk": "Helsingin keskusta",
    
}

RESTAURANT_ALIASES = {
    "kaisa": "Kaisa-talo",
    "kaivari": "Kaivopiha",
    "kaivo": "Kaivopiha",
    "che": "Chemicum",
    "ex": "Exactum",
    "phy": "Physicum",
    "tf": "Täffä",
    "ablok": "A Bloc",
    "exa": "Exactum"

}



def fetch_json(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_areas():
    return fetch_json(AREAS_URL)


def fetch_menus(date_str):
    url = MENUS_URL.format(date=date_str)
    return fetch_json(url)


def fetch_all_restaurants():
    return fetch_json(RESTAURANTS_ALL_URL)


def fetch_restaurants_by_ids(ids):
    ids_string = ",".join(str(i) for i in ids)
    return fetch_json(RESTAURANTS_BY_IDS_URL.format(ids=ids_string))


#parsing input
def parse_input(user_input):

    user_input = user_input.strip().lower()
    parts = user_input.split()

    name = parts[0]
    today = datetime.date.today()

    # default = today
    target_date = today

    if len(parts) > 1:
        match = re.match(r"^(\d{1,2})\.(\d{1,2})$", parts[1])
        if match:
            day, month = map(int, match.groups())
            year = today.year
            target_date = datetime.date(year, month, day)


    return name, target_date.isoformat()

def get_opening_hours(opening_hours, target_date):
    weekday = datetime.date.fromisoformat(target_date).weekday()
    if weekday < len(opening_hours):
        return opening_hours[weekday]
    return None


def get_area_by_name(areas, user_input):
    if user_input in AREA_ALIASES:
        target = AREA_ALIASES[user_input].lower()
    else:
        target = user_input

    for area in areas:
        if target in area["name"].lower():
            return area

    return None


def find_restaurant_by_name(restaurants, user_input):
    if user_input in RESTAURANT_ALIASES:
        target = RESTAURANT_ALIASES[user_input].lower()
    else:
        target = user_input

    matches = [r for r in restaurants if target in r["name"].lower()]

    if len(matches) == 1:
        return matches[0]

    if len(matches) > 1:
        print("\nLöytyi useita ravintoloita:")
        for i, r in enumerate(matches, 1):
            print(f"{i} - {r['name']}")

        choice = input("Valitse numero: ").strip()
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(matches):
                return matches[index]

    return None


def print_restaurant_menu(restaurant, menus, target_date):
    rid = str(restaurant["id"])
    name = restaurant["name"]
    opening = get_opening_hours(restaurant["openingHours"], target_date)

    print(f"\n{name} ({opening if opening else 'Suljettu'})")
    print("-" * 30)

    if rid in menus and target_date in menus[rid]:
        foods = menus[rid][target_date]

        seen = set()
        for food in foods:
            key = (food["title"], tuple(food.get("properties", [])))
            if key not in seen:
                seen.add(key)
                props = ", ".join(food.get("properties", []))
                print(f"• {food['title']} ({props})")
    else:
        print("Ei menuja tälle päivälle.")

if __name__ == "__main__":
    try:
        areas = fetch_areas()
        all_restaurants = fetch_all_restaurants()

        while True:
            user_input = input("\nHae alue tai ravintola (0 = lopeta): ").strip()

            if user_input == "0":
                print("Moikka 👋")
                break

            name_input, target_date = parse_input(user_input)

            print(f"\nHaetaan menut päivälle {target_date}...")

            menus = fetch_menus(target_date)

            area = get_area_by_name(areas, name_input)

            if area:
                print(f"\nAlue: {area['name']}")
                restaurants = fetch_restaurants_by_ids(area["restaurants"])
                for r in restaurants:
                    print_restaurant_menu(r, menus, target_date)
            else:
                restaurant = find_restaurant_by_name(all_restaurants, name_input)

                if restaurant:
                    print_restaurant_menu(restaurant, menus, target_date)
                else:
                    print("Aluetta tai ravintolaa ei löytynyt.")

    except requests.RequestException as e:
        print("Verkkovirhe:", e)