import json
import requests
from bs4 import BeautifulSoup
import time

def load_json(filename='restaurants.json'):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json(data, filename='restaurants_updated.json'):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Updated data saved to {filename}")

def parse_menu_urls(html_content, restaurant):
    soup = BeautifulSoup(html_content, 'html.parser')

    # If a menu exists, set it to all active menus for the restaurant at the mealtime
    for menu_div in soup.select('div.rw-menus div.menu-active'):
        menu_url = menu_div.find('a')['href']
        if "Brunch" in menu_div.find('img')['alt']:
            if restaurant['brunchMenu25']:
                restaurant['brunchMenu25Url'] = menu_url
                print("Updated $25 brunch menu")
            elif restaurant['brunchMenu35']:
                restaurant['brunchMenu35Url'] = menu_url
                print("Updated $35 brunch menu")
        elif "Lunch" in menu_div.find('img')['alt']:
            if restaurant['lunchMenu25']:
                restaurant['lunchMenu25Url'] = menu_url
                print("Updated $25 lunch menu")
            elif restaurant['lunchMenu35']:
                restaurant['lunchMenu35Url'] = menu_url
                print("Updated $35 lunch menu")
        elif "Dinner" in menu_div.find('img')['alt']:
            if restaurant['dinnerMenu40']:
                restaurant['dinnerMenu40Url'] = menu_url
                print("Updated $40 dinner menu")
            elif restaurant['dinnerMenu55']:
                restaurant['dinnerMenu55Url'] = menu_url
                print("Updated $55 dinner menu")
            elif restaurant['dinnerMenu65']:
                restaurant['dinnerMenu65Url'] = menu_url
                print("Updated $65 dinner menu")

    return restaurant

def update_restaurant_data(restaurants):
    for restaurant in restaurants:
        print(f"Processing {restaurant['name']}...")
        try:
            response = requests.get(restaurant['link'])
            response.raise_for_status()
            html_content = response.text

            # Parse the HTML to find the menu URLs
            parse_menu_urls(html_content, restaurant)

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
