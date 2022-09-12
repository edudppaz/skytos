import time
import requests
from requests.exceptions import HTTPError


def basicGET_JSON(url: str) -> dict:
    retries = 3

    for n in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            break
        except HTTPError as exc:
            code = exc.response.status_code
            if code in [429, 500, 502, 503, 504]:
                # retry after n seconds
                time.sleep(n)
                continue
            raise
    return response.json()


def fetchGCP(filter):
    GCP_URL = "https://www.gstatic.com/ipranges/cloud.json"
    filter = {}


def fetchGOOG(filter):
    GOOG_URL = "https://www.gstatic.com/ipranges/goog.json"
    filter = {}


def fetchAWS(filter):
    AWS_URL = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    filter = {}


def fetchAzure(filter):
    AZURE_URL = "https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519"
    # parse URL contains "Service Tags" and .json
    filter = {}
