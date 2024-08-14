import requests
import folium
import os
import json
from geopy.distance import geodesic

# Your Google API key
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
PROCESSED_RESTAURANT_COUNT = 0

def increment_processed_count():
    global PROCESSED_RESTAURANT_COUNT
    PROCESSED_RESTAURANT_COUNT += 1

def get_places_details(restaurant, city='Washington, DC'):
    """Fetch details about the restaurant using the Google Places API."""
    search_url = "https://places.googleapis.com/v1/places:searchText"
    params = {
        'key': API_KEY,
        'fields': "*"
    }
    data = {
        "textQuery": f"{restaurant} in {city}"
    }

    response = requests.post(search_url, params=params, json=data)
    places_data = response.json()

    if "places" in places_data:
        place = places_data['places'][0]  # Use the first place that matches
        name = place.get('displayName').get('text', 'Name not available')

        lat = place['location']['latitude']
        lon = place['location']['longitude']
        rating = place.get('rating', 0)
        price_level = place.get('priceLevel', 'N/A')
        address = place.get('shortFormattedAddress', 'Address not available')
        website = place.get('websiteUri', 'Website not available')
        google_maps_url = place.get('googleMapsUri', 'Googel Maps URL not available')

        # Print the searched name and found name to compare
        if restaurant != name:
            print(f"Searching for: {restaurant}\nFound:         {name}")
            print(f"If needed to delete - Address: {address}, Google Maps URL: {google_maps_url}")

        price_levels = {
            'PRICE_LEVEL_UNSPECIFIED': '?',
            'PRICE_LEVEL_FREE': '$',
            'PRICE_LEVEL_INEXPENSIVE': '$',
            'PRICE_LEVEL_MODERATE': '$$',
            'PRICE_LEVEL_EXPENSIVE': '$$$',
            'PRICE_LEVEL_VERY_EXPENSIVE': '$$$$'
        }

        # Optional code to limit the restaurants by rating
        # if rating >= 4.0:
        return {
            'name': name,
            'lat': lat,
            'lon': lon,
            'rating': rating,
            'price_level': price_levels.get(price_level, '?'),
            'address': address,
            'website': website,
            'google_maps_url': google_maps_url
        }
        # else:
        #     print(f"Restaurant {restaurant} did not meet rating standards and will not be included.")
        #     increment_processed_count()

    else:
        print(f"Error fetching data for {restaurant}: {places_data.get('error', 'Unknown error')}")
        increment_processed_count()
    return None

def map_restaurants(json_file, city='Washington, DC'):
    """Map out the restaurant locations with additional details."""
    # Initialize the map centered around Washington DC
    map_center = (38.89511, -77.03637)
    m = folium.Map(location=map_center, zoom_start=12)
    downtown_coords = map_center

    # Load restaurants from JSON
    with open(json_file, 'r') as f:
        restaurants = json.load(f)

    for restaurant in restaurants:
        name = restaurant.get('name')

        places_details = get_places_details(name, city)
        
        if places_details:
            lat, lon = places_details['lat'], places_details['lon']
            # Check if within 16 miles of downtown
            if geodesic((lat, lon), downtown_coords).miles <= 16:
                popup_info = (f"<strong>Name:</strong> {places_details['name']}<br>")
                # Conditionally add menu links
                if restaurant['brunchMenu25']:
                    popup_info += f"<a href='{restaurant['brunchMenu25Url']}'>$25 Brunch Menu</a><br>"
                if restaurant['lunchMenu25']:
                    popup_info += f"<a href='{restaurant['lunchMenu25Url']}'>$25 Lunch Menu</a><br>"
                if restaurant['brunchMenu35']:
                    popup_info += f"<a href='{restaurant['brunchMenu35Url']}'>$35 Brunch Menu</a><br>"
                if restaurant['lunchMenu35']:
                    popup_info += f"<a href='{restaurant['lunchMenu35Url']}'>$35 Lunch Menu</a><br>"
                if restaurant['dinnerMenu40']:
                    popup_info += f"<a href='{restaurant['dinnerMenu40Url']}'>$40 Dinner Menu</a><br>"
                if restaurant['dinnerMenu55']:
                    popup_info += f"<a href='{restaurant['dinnerMenu55Url']}'>$55 Dinner Menu</a><br>"
                if restaurant['dinnerMenu65']:
                    popup_info += f"<a href='{restaurant['dinnerMenu65Url']}'>$65 Dinner Menu</a><br>"
                
                popup_info += f"<strong>Rating:</strong> {places_details['rating']}<br>"
                popup_info += f"<strong>Price Level:</strong> {places_details['price_level']}<br>"
                popup_info += f"<strong>Cuisine Type:</strong> {restaurant['cuisine']}<br>"
                popup_info += f"<strong>Address:</strong> {places_details['address']}<br>"
                popup_info += f"<strong>Website:</strong> <a href='{places_details['website']}'>{places_details['website']}</a><br>"
                popup_info += f"<strong>Google Maps:</strong> <a href='{places_details['google_maps_url']}'>{places_details['google_maps_url']}</a><br>"

                folium.Marker([lat, lon], popup=popup_info).add_to(m)
                increment_processed_count()
            else:
                print(f"Restaurant {name} was not marked as it is outside the boundary ({geodesic((lat, lon), downtown_coords).miles:.2f} miles away).")
                increment_processed_count()
            
    # Save the map to an HTML file
    m.save('dc_restaurant_week_map_with_details.html')
    print("Map created and saved as dc_restaurant_week_map_with_details.html")

# Path to your JSON file
json_file = 'restaurants.json'

map_restaurants(json_file)
print(f"{PROCESSED_RESTAURANT_COUNT} restaurants were processed!")
