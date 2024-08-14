import json
from bs4 import BeautifulSoup

# Need to expand the full list of restarants on the https://www.ramw.org/restaurantweek page
# Save the HTML content to a file called restaurants.html
# We will use this file to parse all the restaurant data into usable JSON data

def parse_restaurant_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    restaurants = []

    # Loop through each restaurant's child div in the <div class="view-content"> tag (around 380)
    for restaurant_div in soup.find_all('div', class_='views-row'):
        name = restaurant_div.find('h3').text.strip()
        link = 'https://www.ramw.org' + restaurant_div.find('a')['href']
        cuisine = restaurant_div.find('div', class_='cuisine').text.strip()
        neighborhood = restaurant_div.find('div', class_='neighborhood').text.strip()

        def has_menu_option(text):
            # Search through all divs with the class 'cost' within the current restaurant_div
            for cost_div in restaurant_div.find_all('div', class_='cost'):
                # Check if there is a div with the 'option-Yes' class and the desired text (means menu exists)
                if cost_div.find('div', class_='option-Yes', string=lambda x: x and text in x):
                    return True
            return False

        # Determine menu options and drink pairing
        drink_pairing = bool(restaurant_div.find('div', class_='togo-option-Yes'))
        brunch_menu_25 = bool(has_menu_option('$25 Brunch Menu'))
        lunch_menu_25 = bool(has_menu_option('$25 Lunch Menu'))
        brunch_menu_35 = bool(has_menu_option('$35 Brunch Menu'))
        lunch_menu_35 = bool(has_menu_option('$35 Lunch Menu'))
        dinner_menu_40 = bool(has_menu_option('$40 Dinner Menu'))
        dinner_menu_55 = bool(has_menu_option('$55 Dinner Menu'))
        dinner_menu_65 = bool(has_menu_option('$65 Dinner Menu'))

        def clean_text(text):
            return ' '.join(text.replace('\n', ' ').split())
        # Create a dictionary for the restaurant
        restaurant_data = {
            "name": clean_text(name),
            "link": link,
            "cuisine": clean_text(cuisine),
            "neighborhood": clean_text(neighborhood),
            "drinkPairing": drink_pairing,
            "brunchMenu25": brunch_menu_25,
            "brunchMenu25Url": "",
            "lunchMenu25": lunch_menu_25,
            "lunchMenu25Url": "",
            "brunchMenu35": brunch_menu_35,
            "brunchMenu35Url": "",
            "lunchMenu35": lunch_menu_35,
            "lunchMenu35Url": "",
            "dinnerMenu40": dinner_menu_40,
            "dinnerMenu40Url": "",
            "dinnerMenu55": dinner_menu_55,
            "dinnerMenu55Url": "",
            "dinnerMenu65": dinner_menu_65,
            "dinnerMenu65Url": ""
        }

        # Add the restaurant to the list
        restaurants.append(restaurant_data)

    return restaurants

def save_to_json(data, filename='restaurants.json'):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
        print(f"Data saved to {filename}")

# Load your HTML content (e.g., from a file)
with open('restaurants.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the data and save to JSON
restaurant_data = parse_restaurant_data(html_content)
save_to_json(restaurant_data)
