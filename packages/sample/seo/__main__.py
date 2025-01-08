from http import HTTPStatus
import os
import requests
import json

CUSTOM_SEARCH_URL = "https://customsearch.googleapis.com/customsearch/v1"
CUSTOM_SEARCH_API_KEY = os.getenv("CUSTOM_SEARCH_API_KEY")
CX = os.getenv("CUSTOM_SEARCH_CX")


def main(args):
    keyword = args.get("keyword")
    country = args.get("country")
    results = args.get("results")

    if not keyword:
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": "No Keyword provided"
        }

    if not country:
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": "No country (de, aut, fr) provided"
        }

    params = {
        "cx": CX,
        "gl": country,
        "num": int(results),
        "q": f"{keyword}",
        "key": CUSTOM_SEARCH_API_KEY
    }

    try:
        response = get_serp(params)
        return {
            "statusCode": HTTPStatus.ACCEPTED,
            "body": json.dumps(response, ensure_ascii=False, indent=4)
        }
    except:
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": "A Problem occured"
        }


def get_serp(params):
    headers = {"Accept": "application/json"}
    response = requests.get(CUSTOM_SEARCH_URL, headers=headers, params=params)

    # Extract relevant data
    data = response.json()
    items = data.get("items", [])
    # Filter and print the title and snippet
    results = filter_results(items)

    return results


def filter_results(items):
    filtered_results = [{"meta-title": item["title"],
                         "meta_description": item["snippet"]} for item in items]
    return filtered_results
