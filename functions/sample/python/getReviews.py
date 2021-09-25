#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import os

from cloudant.client import Cloudant
from cloudant.query import Query
from cloudant.error import CloudantException
import requests


def main(dict):
    databaseName = "reviews"
    print("Program Started")
    try:
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )
        database = client['reviews']

        selector = {'dealership': {'$eq': int(dict['dealerId'])}}
        docs = database.get_query_result(selector).all()
        return {"reviews": docs}
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}


