import json
import requests
from bs4 import BeautifulSoup
import time

def load_json(filename='restaurants.json'):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json(data, filename='restaurants.json'):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        print(f"Updated data saved to {filename}")

def parse_menu_urls(html_content, restaurant):
    soup = BeautifulSoup(html_content, 'html.parser')
    menu_found = False

    # If a menu exists, set it to all active menus for the restaurant at the mealtime
    for menu_div in soup.select('div.rw-menus div.menu-active'):
        menu_url = menu_div.find('a')['href']
        if "Brunch" in menu_div.find('img')['alt']:
            if restaurant['brunchMenu25']:
                restaurant['brunchMenu25Url'] = menu_url
                menu_found = True
            if restaurant['brunchMenu35']:
                restaurant['brunchMenu35Url'] = menu_url
                menu_found = True
        elif "Lunch" in menu_div.find('img')['alt']:
            if restaurant['lunchMenu25']:
                restaurant['lunchMenu25Url'] = menu_url
                menu_found = True
            if restaurant['lunchMenu35']:
                restaurant['lunchMenu35Url'] = menu_url
                menu_found = True
        elif "Dinner" in menu_div.find('img')['alt']:
            if restaurant['dinnerMenu40']:
                restaurant['dinnerMenu40Url'] = menu_url
                menu_found = True
            if restaurant['dinnerMenu55']:
                restaurant['dinnerMenu55Url'] = menu_url
                menu_found = True
            if restaurant['dinnerMenu65']:
                restaurant['dinnerMenu65Url'] = menu_url
                menu_found = True

    if not menu_found:
        print("No menu found for the restaurant!")
    return restaurant

def update_restaurant_data(restaurants):
    for restaurant in restaurants:
        print(f"Processing {restaurant['name']}...")
        if restaurant['name'] == "2941 Restaurant":
            return restaurants
        try:
            response = requests.get(restaurant['link'])
            response.raise_for_status()
            html_content = response.text

            # Parse the HTML to find the menu URLs
            updated_restaurant_data = parse_menu_urls(html_content, restaurant)
            restaurant.update(updated_restaurant_data)

            # Delay the next request by 1 second
            time.sleep(1)

        except requests.RequestException as e:
            print(f"Failed to retrieve data for {restaurant['name']}: {e}")

    return restaurants

# Load the existing JSON data
restaurant_data = load_json()

# Update the data with menu URLs
updated_restaurant_data = update_restaurant_data(restaurant_data)

# Save the updated JSON data
save_json(updated_restaurant_data)
