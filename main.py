

import requests
import folium
import os
from geopy.distance import geodesic

# Your Google API key
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
PROCESSED_RESTAURANT_COUNT = 0

def increment_processed_count():
    global PROCESSED_RESTAURANT_COUNT
    PROCESSED_RESTAURANT_COUNT = PROCESSED_RESTAURANT_COUNT + 1

def get_places_details(restaurant, city='Washington, DC'):
    """Fetch details about the restaurant using the new Google Places API."""
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
        restaurant_details = []
        for place in places_data['places']:
            name = place.get('displayName','text')
            lat = place['location']['latitude']
            lon = place['location']['longitude']
            rating = place.get('rating', 0)
            price_level = place.get('priceLevel', 'N/A')
            cuisine_type = place.get('primaryTypeDisplayName', 'text')
            address = place.get('shortFormattedAddress', 'Address not available')

            # Filter by rating
            if rating >= 4.0:
                restaurant_details.append({
                    'name': name,
                    'lat': lat,
                    'lon': lon,
                    'rating': rating,
                    'price_level': price_level,
                    'cuisine_type': cuisine_type,
                    'address': address
                })
            else:
                print(f"Restaurant {restaurant} did not meet rating standards and will not be included.")
                increment_processed_count()

        return restaurant_details
    else:
        print(f"Error fetching data for {restaurant}: {places_data.get('error', 'Unknown error')}")
        increment_processed_count()
        return []

def map_restaurants(restaurant_names, city='Washington, DC'):
    """Map out the restaurant locations with additional details."""
    # Initialize the map centered around Washington DC
    map_center = (38.89511, -77.03637)
    m = folium.Map(location=map_center, zoom_start=12)
    downtown_coords = map_center

    for restaurant in restaurant_names:
        places_details = get_places_details(restaurant, city)
        
        for detail in places_details:
            lat, lon = detail['lat'], detail['lon']
            # Check if within x miles of downtown
            if geodesic((lat, lon), downtown_coords).miles <= 16:
                popup_info = (
                    f"Name: {detail['name']}<br>"
                    f"Rating: {detail['rating']}<br>"
                    f"Price Level: {detail['price_level']}<br>"
                    f"Cuisine Type: {detail['cuisine_type']}<br>"
                    f"Address: {detail['address']}"
                )
                folium.Marker([lat, lon], popup=popup_info).add_to(m)
                increment_processed_count()
            else:
                print(f"Restaruant {restaurant} was not marked as it is outside the boundry. ({geodesic((lat, lon), downtown_coords).miles} miles away)")
                increment_processed_count()
            
    # Save the map to an HTML file
    m.save('dc_restaurant_week_map_with_details.html')
    print("Map created and saved as dc_restaurant_week_map_with_details.html")

# List of restaurant names
restaurant_names = [
    #TestList
    'Fogo de Chao Brazilian Steakhouse North Bethesda', "Hank's Oyster Bar Dupont Circle", "Gypsy Kitchen DC",  # Replace with actual restaurant names
    # FULL LIST!!!
    # "1789 Restaurant","2941 Restaurant","AGORA","Agora Tysons","Al Dente DC","ala","ala | Bethesda","Alero Restaurant - Dupont Circle","Alhambra","All Set Restaurant & Bar","All-Purpose Capitol Riverfront","All-Purpose Pizzeria","Alta Strada City Vista","Alta Strada Mosaic","Amazonía","Ambar","Ambar Clarendon","Ambar Shaw","American Prime","Annabelle","Any Day Now","B Side","Baby Shank Restaurant & Bar","Balos Estiatorio","Bar Charley","Bar Chinois","Bar Japonais","Bar Spero","Bastille Brasserie & Bar","BeerLab DC","Belga Cafe","Bellissimo Restaurant","Big Buns Ashburn","Big Buns Damn Good Burgers - Ballston","Big Buns Damn Good Burgers - Franklin Farms","Big Buns Damn Good Burgers - Shirlington","Big Buns Damn Good Burgers Reston Station","Big Buns McClean","Bindaas Foggy Bottom","Bistro Cacao","Bistro Du Jour","Bistro Du Jour location at Capitol Hill","Bistro Du Jour location at Capitol Hill","Bistrot Lepic & Wine Bar","Blue Duck Tavern","Bluejacket","Boqueria Dupont","Boqueria Penn Quarter","Brasserie Liberté","BRESCA","Bronze","Cafe Berlin","Cafe Du Parc at Willard InterContinental Washington, D.C.","Café Milano","Cane","Caruso's Grocery Pike & Rose","Casa Teresa","Ceibo","Celebration by Rupa Vira","Central Michel Richard","Chaplin's","Charley Prime Foods","Charlie Palmer Steak - DC","Chasin's Tails","Cheesetique Del Ray","Chef Geoff's","Chef Geoff's West End","CHIKO Dupont","Chima Steakhouse","China Chilcano","Chloe","Circa at Clarendon","Circa at Foggy Bottom","Circa at The Boro","CIRCA Navy Yard","City Cruises","claudio's table","Clyde's at Mark Center","Code Red","Convivial","Cork Wine & Market","Corso Italian","Cranes","Cuba Libre - DC","Cucina Morini","Cure Bar & Bistro","CUT by Wolfgang Puck","Daikaya Izakaya","Dauphine's","Davio's Northern Italian Steakhouse","Del Frisco's Double Eagle DC","Del Mar","Diablo’s Cantina","Dirty Habit","District Winery","dLeña","Donahue","Dovetail","Due South","Dukes Counter","Dukes Grocery - Dupont Circle","Dukes Grocery - Foggy Bottom","Dukes Grocery at Navy Yard","Earls Kitchen + Bar","Easy Company Wine Bar","El Centro - Georgetown","El Presidente","El Secreto De Rosita","El Tamarindo","Elcielo Restaurant","Elle","Ellie Bird","Ellington Park Bistro","Epic Smokehouse","Equinox Restaurant","Estuary","Ethiopic Restaurant","Evening Star Cafe","Fava Pot","FIG & OLIVE","Figleaf Bar & Lounge","Filomena Ristorante","Fiola Mare","Firefly - DC","Fitzgerald's","Flavio Italian restaurant","Floriana","Fogo de Chao Brazilian Steakhouse","Fogo de Chao Brazilian Steakhouse North Bethesda","Fogo de Chao Brazilian Steakhouse Tysons","Fogo de Chao National Harbor","Fogo de Chao Reston","Founding Farmers - DC","Founding Farmers - Montgomery County","Founding Farmers - Tysons","Founding Farmers & Distillers","Founding Farmers Fishers & Bakers","Founding Farmers Reston","Fred & Stilla","GATSBY","Gerrard Street Kitchen","Gogi Yogi","Gravitas","Gypsy Kitchen DC","Haikan","Hamrock's","Hank's Oyster Bar Dupont Circle","Hard Rock Cafe","Hen Quarter - Alexandria","Hen Quarter Prime - DC","HIRAYA Cafe & Restaurant","i Ricchi","il Canale","Il Piatto","ilili","Immigrant Food","INGLE KOREAN STEAKHOUSE","Iron Gate","Irregardless","Ivy City Smokehouse","J. Gilbert’s – Wood Fired Steaks & Seafood - McLean","J. Hollinger's Waterman's Chophouse","Jackie American Bistro","Jaleo DC","JINYA Ramen Bar at Logan Circle","JINYA Ramen Bar at Walter Reed","Joon","Joselito","Josephine","Joy by Seven Reasons","Kaliwa","Kaz Sushi Bistro","Kelly's Oyster House and Bar","Kingbird","Kirby Club","Kitchen Savages","Kyojin Sushi DC","L'Ardente","La Bise","La Chaumiere","La Collina","La Cote d'Or cafe","La Grande Boucherie","Laos in Town","Laporta's Restaurant","Le DeSales","LIA'S","Lincoln - DC","Little Blackbird","Little Coco's","Lucy Bar","Lulu's Wine Garden","Lyle's","Lyon Hall","Makan","Maker's Union Cathedral Commons","Makers Union Arlington","Makers Union at The Wharf","Makers Union Reston","Maketto","Mallard","Mariscos 1133","Mastro's Steakhouse","Matchbox - Bethesda","Matchbox - Capitol Hill","Matchbox - Merrifield","Matchbox - One Loudoun","Matchbox - Rockville","Matchbox - Silver Spring","Matchbox Penn Quarter","Matchbox Pentagon","Matchbox Reston Station","McCormick & Schmick's - Crystal City","Méli Wine & Mezze","Mercy Me","Mi Vida 14th St.","Mi Vida at Penn Quarter","MI VIDA Wharf DC","Michele's","Milk & Honey Ashburn","Milk & Honey Bowie","Milk & Honey College Park","Milk & Honey Fairfax","Milk & Honey Wharf","Milk and Honey Alexandria","Milk and Honey Clinton","Milk and Honey H Street","Milk and Honey Woodmore","MITA","Modena","Moon Rabbit","Moonraker","Morrison-Clark Restaurant","Morton's The Steakhouse - Arlington","Morton's The Steakhouse - Bethesda","Morton's The Steakhouse - Downtown DC","Morton's The Steakhouse - Reston","Mussel Bar and Grill Arlington","MXDC","NAMA","Namak","New Heights Restaurant","Nina May","North Italia","North Italia Reston","North Italia Tysons","NUE Elegantly Vietnamese","Ocean Prime","Officina","Ometeo","Opal","Opaline Bar and Brasserie","Osteria Costa at MGM National Harbor","Osteria da Nino","Osteria Marzano","Osteria Morini","Ottoman Taverna","Oyamel","Palette 22","Palm Restaurant - Washington DC","Pappe DC","Paraíso","PassionFish","Pastis","Pearl Dive","Pennyroyal Station","Perry's Restaurant","Petite Cerise","Philippe by Philippe Chow","Piccolina","Pink Taco","Pisco y Nazca Ceviche Gastrobar","Pisco Y Nazca Ceviche Gastrobar - Reston","Rania","Rasika Penn Quarter","Rasika West End","Residents Cafe & Bar","Reveler's Hour","RIS","Roofer's Union","Rosemary Bistro Cafe","RPM Italian DC","Rustico Alexandria","Ruthie's All-Day","Sababa","Sabores Tapas Bar","SER Restaurant","Sette Osteria Dupont","Seven Reasons","Sfoglina Downtown","Sfoglina Rosslyn","Sfoglina Van Ness","Shilling Canning Company","Sonoma Restaurant + Wine Bar","Sovereign, The","Spanish Diner","SPICE KRAFT INDIAN BISTRO","St James - Modern Caribbean","STK Steakhouse","STREET PIZZA D.C","Succotash F Street","Supra","Surreal","Susheria","Sushi By Bou- DC @ CitizenM Hotel L'enfant Plaza","Sushi Taro","Taberna del Alabardero","Tabla","Taffer's Tavern","Takara 14","Talea Ristorante","TAP Sports Bar at MGM National Harbor","Taqueria Xochi","Teddy and the Bully Bar","The Bazaar by José Andrés","The Bombay Club","The Capital Grille Fairfax","The Capital Grille Tysons","The Daily Dish Neighborhood Bistro & Bar","The Delegate","The Dish & Dram","The Duck & The Peach","The Falls","The Grill","The Grill from Ipanema","The Grove Bar and Grill","The Henri","The Imperial","The Liberty Tavern","The Little Grand","The Melting Pot Arlington","The Melting Pot Gaithersburg","The Melting Pot Reston","The Park at Fourteenth","The Pembroke","The Point D.C.","The Royal","The Saga","The Salt Line","The Salt Line - Ballston","The Salt Line Bethesda","The Smith","The Wine Kitchen - Leesburg","Tiger Fork","Tiki on 18th & The Game Sports Pub","Tonari","Tony and Joe's Seafood Place","TRIO Grill","Truluck's Ocean's Finest Seafood and Crab","Trummer's","Tysons Social Tavern","Unconventional Diner","Urban Roast","Urbano The Heights","Vagabond","Vera Cocina & Bar","Vermilion","Via Ghibellina","Via Sophia","Villa Yara","Wildfire - Tysons Galleria","Wine Kitchen on the Creek","Wren","Xiquet by Danny Lledó","Yume Sushi","Zaytinya","Zeppelin","ZOOZ"
]

map_restaurants(restaurant_names)
print(f"{PROCESSED_RESTAURANT_COUNT} restaurants were processed!")