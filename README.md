#

## Purpose

Scripts for pulling down and mapping restaurant week data in DC for 2024. This project was inspired by the shortcomings of the [official site](https://www.ramw.org/restaurantweek), particularly for visitors who are unfamiliar with the different neighborhoods in the area. The site has a cumbersome interface for accessing menus, and the map feature is non-functional. As a solution, I have developed a replacement map that may not have search functionality, but still offers valuable features for users who want to find restaurants in close proximity to their location.

## Installation

To install the necessary packages, run the following commands:

```shell
pip install --upgrade pip
pip install requests folium geopy beautifulsoup4
```

Make sure you have pip installed before running the command.

## How to Run

1. Navigate to https://www.ramw.org/restaurantweek
2. Expand all restaurant options (there are around 380, so it will take a while)
3. Open up DevTools and copy the HTML
4. Replace what is in [restaurants.html](./restaurants.html) with the copied data
5. Run [restaurant_parser.py](./restaurant_parser.py)
6. This generates a detailed list of restaurants in [restaurants.json](./restaurants.json), validate the data
7. Run [menu_parser.py](./menu_parser.py) to scrape menu's off ramw website
8. Update any data that was missed in [restaurants.json](./restaurants.json)
9. Run [main.py](./main.py) which will query against the google maps API, and generate a map with all the data
