from http import HTTPStatus
import os
import pandas as pd
import advertools


def main(args):
    '''
    Takes in the email address, subject, and message to send an email using SendGrid, 
    returns a json response letting the user know if the email sent or failed to send.

        Parameters:
            args: Contains the from email address, to email address, subject and message to send

        Returns:
            json body: Json response if the email sent successfully or if an error happened
    '''
    search_api_key = os.getenv("api_key")
    cx = os.getenv("CUSTOM_SEARCH_CX")
    keyword = args.get("keyword")
    country = args.get("country")

    if not keyword:
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": "No Keyword provided"
        }

    serp = advertools.serp_goog(
        q=f"{keyword}", gl=f"{country}", cx=cx, key=search_api_key)

    return {
        "statusCode": HTTPStatus.ACCEPTED,
        "body": serp
    }
