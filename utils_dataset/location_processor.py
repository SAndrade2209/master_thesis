import pycountry
import pandas as pd
import numpy as np
import reverse_geocoder as rg

class LocationProcessor:
    @staticmethod
    def get_country_name(country_code):
        if pd.isna(country_code) or country_code == "":
            return None
        try:
            country_code = str(country_code).strip().upper()
            return pycountry.countries.get(alpha_2=country_code).name
        except AttributeError:
            return None

    @staticmethod
    def is_number(s):
        try:
            float(s)  # Try to convert the string to float
            return True
        except ValueError:
            return False

    @staticmethod
    def get_artist_country_name(location):
        state_abbreviations = [
            "AL", "AK", "AZ", "AR", "AS", "CA", "CO", "CT", "DE", "DC",
            "FL", "GA", "GU", "HI", "ID", "IL", "IN", "IA", "KS", "KY",
            "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE",
            "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "MP", "OH", "OK",
            "OR", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "TT", "UT",
            "VT", "VI", "VA", "WA", "WV", "WI", "WY", "U.S.", "NYC", "USA"
        ]

        known_cities = {
            "Los Angeles": "United States",
            "Denver": "United States",
            "Detroit": "United States",
            "CALIFORNIA, California	": "United States",
            "Nederland": "United States",
            "california": "United States",
            "Venezuela":"Venezuela",
            "Timișoara": "Romania",
            "Tel Aviv": "Israel",
            "Galloway": "United States",
            "Pontypridd, Wales": "United Kingdom",
            "Wales": "United Kingdom",
            "Brooklyn": "United States",
            "London": "United Kingdom",
            "Seattle": "United States",
            "Jersey": "United States",
            "Leesburg": "United States",
            "Poughkeepsie": "United States",
            "Kona": "United States",
            "Virgin Islands": "United States",
            "U.S.": "United States",
            "Joutseno": "Finland",
            "Helsinki": "Finland",
            "Cote d'Ivoire": "Cote d'Ivoire",
            "Broken Bow": "United States",
            "Hommelvik": "Norway",
            "Toronto": "Canada",
            "Rochester": "United States",
            "Copenhagen": "Denmark",
            "Glen Rock": "United States",
            "Allemagne,Norvège": None,
            "Sony": None,
            "Oconomowoc": "United States",
            "McLellan": "United States",
            "Boulogne Sur Mer": "France",
            "St. Petersburg": "United States",
            "Pontiac": "United States",
            "Fairbanks": "United States",
            "Oxford": "United Kingdom",
            "Nova Scot": "Canada",
            "outerspace": None,
            "Cambridge": "United Kingdom",
            "florida": "United States",
            "Essen": "Germany",
            "Chicago": "United States",
            "Boston": "United States",
            "Česká republika": "Czech Republic",
            "Atlanta": "United States",
            "Malaga": "Spain",
            "Seoul": "Korea, Republic of",
            "sulteng": "Indonesia",
            "Brussels": "Belgium",
            "Belfast": "United Kingdom",
            "Warsaw": "Poland",
            "Glasgow": "United Kingdom",
            "barcelona": "Spain",
            "Mannheim": "Germany",
            "la Vallée": "France",
            "Östersund": "Sweeden",
            "Düsseldorf": "Germany",
            "Lousiana": "United States",
            "Venus": None,
            "Earth": None,
            "YAHD": None,
            ".NET": None,
            "Miami": "United States",
            "francisco": "United States",
            "Newcastle": "United Kingdom",
            "Germania": "Germany",
            "Inglaterra": "United Kingdom",
            "Edinburgh": "United Kingdom",
            "Suecia": "Sweden",
            "Tromsø": "Norway",
            "Hollywood": "United States",
            "Melbourn": "Australia",
            "İngiltere": "United Kingdom",
            "Aberdeen": "United Kingdom",
            "Sunlandia": "Finland",
            "Sydney": "Australia",
            "elphia": "United States",
            "Nashville": "United States",
            "new Orleans": "United States",
            "Eternia": None,
            "Belgique": "Belgium",
            "Brighton": "United Kingdom",
            "LOWELL": "United States",
            "Borlänge": "Sweden",
            "Stockholm": "Sweden",
            "Molfetta": "Molfetta",
            "Athens": "Greece",
            "Oakland": "United States",
            "Hannut": "Belgium",
            "Wiädikä": None,
            "Malmö": "Sweden",
            "Providence": "United States",
            "rotherham": "United Kingdom",
            "Tanzania": "Tanzania",
            "Enköping": "Sweden",
            "Stefan Kozalla": None,
            "St Catharines": "Canada",
            "Reims": "France",
            "Västerås": "Sweden",
            "Selkirk": "Canada",
            "Newton County": "United States",
            "Steenvoorde": "France",
            "Russia": "Russian Federation",
            "New York": "United States",
            "Facebook": None,
            "España": "Spain",
            "mundo": None,
            "everywhere": None,
            "#": None,
            "Reino unido": "United Kingdom",
            "Sk�k�enmark": None,
            "City of Angels": None,
            "heimatlied": "Austria",
            "Bonn": "Germany",
            "Gdansk": "Poland",
            "Sinding  Bryrup Silkeborg": "Denmark"

        }

        uk_list = ["UK", "U.K."]
        canada_list = ["ON", "AB", "NS", "MB"]

        if LocationProcessor.is_number(location):
            return None

        if pd.isna(location) or location == "" or len(location) > 50:
            return None

        if "New York" in location:
            return "United States"

        if len(location) <= 4:
            if location.strip().upper() in state_abbreviations:
                return "United States"
            elif location.strip().upper() in ["LDN"]:
                return "United Kingdom"
            elif location.strip().upper() in ["NSW"]:
                return "Australia"
            else:
                return None

        if location.lower() in ('uk', 'usa', 'us', "u.k."):
            if location.lower() == 'uk':
                return 'United Kingdom'
            elif location.lower() in ('usa', 'us', 'u.s.'):
                return 'United States'

        for city in known_cities:
            if city.lower() in location.lower():
                return known_cities[city]
                
        country_name = "n/a"
        for country in pycountry.countries:
            if country.name.upper() in location.upper():
                return country.name
            if hasattr(country, 'common_name') and country.common_name in location.title():
                return country.common_name
            if hasattr(country, 'official_name') and country.official_name in location.title():
                return country.official_name

        for subdiv in pycountry.subdivisions:
            if subdiv.name in location:
                return pycountry.countries.get(alpha_2=subdiv.country_code).name

        for country in pycountry.countries:
            if country.name in location:
                return country.name
            if country.alpha_2 in location:
                return country.name
            if country.alpha_3 in location:
                return country.name

        

        if location == "Virgin Islands, U.S.":
            return "United States"

        states = location.strip().split(',')
        if len(states) == 2:
            if states[1].strip().upper() in state_abbreviations:
                return "United States"
            elif states[1].strip().upper() in uk_list:
                return "United Kingdom"
            elif states[1].strip().upper() in canada_list:
                return "Canada"
            elif states[1].strip().upper() in ["HD", "HOLLAND"]:
                return "Holland"
            elif states[1].strip().upper() in ["BRA"]:
                return "Brazil"
            elif states[1].strip().upper() in ["NSW", "NT"]:
                return "Australia"
            else:
                print(states)

        last_three = location[-3:].strip()
        if last_three.strip().upper() in state_abbreviations:
            return "United States"
        elif last_three.strip().upper() in uk_list:
            return "United Kingdom"
        elif last_three.strip().upper() in canada_list:
            return "Canada"
        elif last_three.strip().upper() in ["HD", "HOLLAND"]:
            return "Holland"
        elif last_three.strip().upper() in ["BRA"]:
            return "Brazil"
        elif last_three.strip().upper() in ["NSW", "NT"]:
            return "Australia"
        else:
            print(location)
        return location

    @staticmethod
    def get_country_post_processing(country_name):
        if pd.isna(country_name) or country_name == "":
            return "n/a"
        country_names = country_name.split(',')
        if len(country_names) > 1:
            return country_names[0]
        return country_name

    @staticmethod
    def get_country_from_coordinates(row):
        # Check if the coordinates are NaN or not numbers
        try:
            # Convert to floats
            lat = float(row['artist_latitude'])
            lon = float(row['artist_longitude'])
        except (ValueError, TypeError):
            return np.nan  # Return NaN for invalid coordinate values

        # Proceed only if the coordinates are valid numbers
        if not (np.isnan(lat) or np.isnan(lon)):
            try:
                # Perform reverse geocoding
                result = rg.search((lat, lon))
                # Extract the country code
                return result[0]['cc']
            except:
                # Return NaN or some error code if geocoding fails
                return np.nan
        else:
            return np.nan