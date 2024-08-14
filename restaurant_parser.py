import json
from bs4 import BeautifulSoup

# Need to expand the full list of restarants on the https://www.ramw.org/restaurantweek page
# Save the HTML content to a file called restaurants.html
# We will use this file to parse all the restaurant data contained within the <div class="view-content"> tag (around 350)

def parse_restaurant_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    restaurants = []

    # Loop through each restaurant's div
    for restaurant_div in soup.find_all('div', class_='views-row'):
        name = restaurant_div.find('h3').text.strip()
        link = 'https://www.ramw.org' + restaurant_div.find('a')['href']
        cuisine = restaurant_div.find('div', class_='cuisine').text.strip()

        # Determine menu options and drink pairing
        drink_pairing = bool(restaurant_div.find('div', class_='togo-option-Yes'))
        brunch_menu_25 = bool(restaurant_div.find('div', class_='cost').find('div', class_='option-No', text='$25 Brunch Menu') is None)
        lunch_menu_25 = bool(restaurant_div.find('div', class_='cost').find('div', class_='option-No', text='$25 Lunch Menu') is None)
        brunch_menu_35 = bool(restaurant_div.find('div', class_='cost').find('div', class_='option-No', text='$35 Brunch Menu') is None)
        lunch_menu_35 = bool(restaurant_div.find('div', class_='cost').find('div', class_='option-No', text='$35 Lunch Menu') is None)
        dinner_menu_40 = bool(restaurant_div.find('div', class_='cost').find('div', class_='option-No', text='$40 Dinner Menu') is None)
        dinner_menu_55 = bool(restaurant_div.find('div', class_='cost').find('div', class_='option-No', text='$55 Dinner Menu') is None)
        dinner_menu_65 = bool(restaurant_div.find('div', class_='cost').find('div', class_='option-Yes', text='$65 Dinner Menu'))

        # Create a dictionary for the restaurant
        restaurant_data = {
            "name": name,
            "link": link,
            "cuisine": cuisine,
            "drinkPairing": drink_pairing,
            "brunchMenu25": brunch_menu_25,
            "lunchMenu25": lunch_menu_25,
            "brunchMenu35": brunch_menu_35,
            "lunchMenu35": lunch_menu_35,
            "dinnerMenu40": dinner_menu_40,
            "dinnerMenu55": dinner_menu_55,
            "dinnerMenu65": dinner_menu_65
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
