import requests
import re
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class GetData:
    def __init__(self):
        self.url = "https://riders.uber.com/graphql" 
        self.headers = {
            "x-csrf-token": "x",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
            "content-type": "application/json", 
            "cookie": ""
        }
        self.body = {
            "operationName": "Activities",
            "variables": {
                "includePast": True,
                "includeUpcoming": True,
                "limit": 10,  # Com mais de 10 de limit costuma retornar alguns erros.
                "orderTypes": ["RIDES", "TRAVEL"],
                "profileType": "PERSONAL",
                "nextPageToken": ""
            },
            "query": "query Activities($cityID: Int, $endTimeMs: Float, $includePast: Boolean = true, $includeUpcoming: Boolean = true, $limit: Int = 5, $nextPageToken: String, $orderTypes: [RVWebCommonActivityOrderType!] = [RIDES, TRAVEL], $profileType: RVWebCommonActivityProfileType = PERSONAL, $startTimeMs: Float) { activities(cityID: $cityID) { cityID past(endTimeMs: $endTimeMs, limit: $limit, nextPageToken: $nextPageToken, orderTypes: $orderTypes, profileType: $profileType, startTimeMs: $startTimeMs) @include(if: $includePast) { activities { ...RVWebCommonActivityFragment __typename } nextPageToken __typename } upcoming @include(if: $includeUpcoming) { activities { ...RVWebCommonActivityFragment __typename } __typename } __typename } } fragment RVWebCommonActivityFragment on RVWebCommonActivity { buttons { isDefault startEnhancerIcon text url __typename } cardURL description imageURL { light dark __typename } subtitle title uuid __typename }"
        }
        self.data = []
        self.orders = []
        self.Dates = {}
        self.coin = ''

    def GetJson(self):
        print("Collecting data...")
        while True:
            response = requests.post(self.url, headers=self.headers, json=self.body, verify=False)
            if response.status_code != 200:
                return {"Error": "Wrong cookies"},response.status_code
            if "errors" in response.json():
                error_code = response.json()['errors'][0]['extensions']['code'] #
                print(f"Got {error_code}, retrying!")
                continue
            response_json = response.json()
            self.data.append(response_json)
            next_page_token = response_json["data"]["activities"]["past"]["nextPageToken"]
            self.body["variables"]["nextPageToken"] = next_page_token
            if len(response_json["data"]["activities"]["past"]["activities"]) < self.body["variables"]["limit"]:
                break
        return 200

    def GetOrders(self):
        print("Calculating total spent...")
        for v in self.data:
            for activity in v["data"]["activities"]["past"]["activities"]:
                if not self.coin:
                    self.coin = activity["description"][:2]
                if "uuid_inicio" not in self.Dates:
                    self.Dates["uuid_inicio"] = activity["uuid"]
                self.Dates["uuid_final"] = activity["uuid"]
                try:
                    amount = float(re.search(r'\d+(\.\d+)?', activity["description"]).group())
                    self.orders.append(amount)
                except Exception as e:
                    return {"Error": e},404
        return 200

    def getDates(self):
        body = {
            "operationName": "GetTrip",
            "variables": {
                "tripUUID": ""
            },
            "query": "query GetTrip($tripUUID: String!) { getTrip(tripUUID: $tripUUID) { trip { beginTripTime } } }"
        }
        dates = {"ultima": "", "primeira": ""}
        for k, v in enumerate(self.Dates.values()):
            body["variables"]["tripUUID"] = v
            response = requests.post(self.url, headers=self.headers, json=body, verify=False)
            if response.status_code != 200:
                return {"Error":"It was not possible to locate the period relating to the trips."},response.status_code
            trip_time = response.json()["data"]["getTrip"]["trip"]["beginTripTime"]
            parsed_date = datetime.strptime(trip_time, '%a %b %d %Y %H:%M:%S GMT%z (Coordinated Universal Time)')
            formatted_date = parsed_date.strftime('%b %Y')
            if k == 0:
                dates["ultima"] = formatted_date
            else:
                dates["primeira"] = formatted_date
        return {"coin":self.coin,"total_spent":sum(self.orders),"first_date":dates['primeira'],"final_date":dates['ultima']},200

    def GetTotal(self):
        status = self.GetJson()
        if status != 200:
            return status
        status = self.GetOrders()
        if status != 200:
            return status
        return self.getDates()