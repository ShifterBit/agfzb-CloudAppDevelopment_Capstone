import json
import os

from django.http import response
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import requests
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import (
    Features,
    EntitiesOptions,
    KeywordsOptions,
    SentimentOptions,
)


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, apikey, **kwargs):
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if apikey:
            response = requests.get(
                url,
                params=kwargs,
                headers={"Content-Type": "application/json"},
                auth=HTTPBasicAuth("apikey", apikey),
            )
        else:
            response = requests.get(
                url, params=kwargs, headers={"Content-Type": "application/json"}
            )

    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(
            url,
            params=kwargs,
            headers={"Content-Type": "application/json"},
            json=payload,
        )
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, 0)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["res"]["rows"]  # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object

            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"],
            )
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


def get_dealer_by_id_from_cf(url, dealer_id):
    # Call get_request with a URL parameter
    json_result = get_request(url + f"?id={int(dealer_id)}", 0)
    if json_result:
        # Get the row list in JSON as dealers
        dealer = json_result["res"]
        # Get its content in `doc` object

        dealer_doc = dealer["docs"][0]
        # Create a CarDealer object with values in `doc` object
        dealer_obj = CarDealer(
            address=dealer_doc["address"],
            city=dealer_doc["city"],
            full_name=dealer_doc["full_name"],
            id=dealer_doc["id"],
            lat=dealer_doc["lat"],
            long=dealer_doc["long"],
            short_name=dealer_doc["short_name"],
            st=dealer_doc["st"],
            zip=dealer_doc["zip"],
        )

        return dealer_obj


def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # call get_request using the url param and dealerId
    json_result = get_request(url + f"?dealerId={dealerId}", 0)
    if json_result:
        # test result
        reviews = json_result["reviews"]  # For each dealer object
        for review in reviews:

            # Create a CarDealer object with values in `doc` object
            try:
                review_obj = DealerReview(
                    dealership=review["dealership"],
                    sentiment=analyze_review_sentiments(review["review"]),
                    review=review["review"],
                    name=review["name"],
                    id=review["id"],
                    purchase=review["purchase"],
                    car_year=review["car_year"],
                    purchase_date=review["purchase_date"],
                    car_model=review["car_model"],
                    car_make=review["car_make"],
                )
                results.append(review_obj)
            except:
                review_obj = DealerReview(
                    dealership=review["dealership"],
                    sentiment=analyze_review_sentiments(review["review"]),
                    review=review["review"],
                    name=review["name"],
                    id=review["id"],
                    purchase=review["purchase"],
                    car_year=None,
                    purchase_date=None,
                    car_model=None,
                    car_make=None,
                )
                results.append(review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    authenticator = IAMAuthenticator(os.environ["NLU_API_KEY"])
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version="2021-03-25", authenticator=authenticator
    )

    natural_language_understanding.set_service_url(
        "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/d6547bbc-cfb0-4db4-b9a9-269cd97f02f0"
    )

    response = natural_language_understanding.analyze(
        language="en", text=text, features=Features(sentiment=SentimentOptions())
    ).get_result()

    result = response["sentiment"]["document"]["label"]
    return result
