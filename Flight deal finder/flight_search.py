import requests
from flight_data import FlightData
import os
import pprint

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = os.environ.get("API_KEY")


class FlightSearch:

    def get_destination_code(self, city_name):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {"apikey": TEQUILA_API_KEY}
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location_endpoint, headers=headers, params=query)
        results = response.json()["locations"]
        code = results[0]["code"]
        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {"apikey": TEQUILA_API_KEY}
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "USD"
        }

        response = requests.get(
            url=f"{TEQUILA_ENDPOINT}/v2/search",
            headers=headers,
            params=query,
        )

        layover_count = 0
        no_flights_found = True
        while no_flights_found:
            try:
                data = response.json()["data"][0]
            except IndexError:
                print(f"No flights found with {layover_count} layover, "
                      f"checking again with {layover_count + 1} layovers")
                layover_count += 1
                query["max_stopovers"] = layover_count
                response = requests.get(
                    url=f"{TEQUILA_ENDPOINT}/v2/search",
                    headers=headers,
                    params=query,
                )
                continue
            else:
                # destination city, airport use layover var to index list because this number
                # can change depending on the number of layovers
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][layover_count]["cityTo"],
                    destination_airport=data["route"][layover_count]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][layover_count + 1]["local_departure"].split("T")[0],
                    stop_overs=layover_count,
                    via_city=data["route"][0]["cityTo"],
                )
                return flight_data
