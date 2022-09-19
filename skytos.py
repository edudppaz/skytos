import argparse
import ipaddress
import time
import re
import requests
import pprint
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


def fetchGCP(f=["all", "ipv4"]):
    GCP_URL = "https://www.gstatic.com/ipranges/cloud.json"
    GCP_JSON = basicGET_JSON(GCP_URL)
    if "ipv4" in f:
        # Going through the json and extracting all ipv4 prefixes into a list
        GCP_PREFIXES = [_.get("ipv4Prefix") for _ in GCP_JSON["prefixes"]]
        # Removing "None" results created by the ipv4-only query
        GCP_PREFIXES = [_ for _ in GCP_PREFIXES if _ != None]
    elif "ipv6" in f:
        # Going through the json and extracting all ipv4 prefixes into a list
        GCP_PREFIXES = [_.get("ipv6Prefix") for _ in GCP_JSON["prefixes"]]
        # Removing "None" results created by the ipv4-only query
        GCP_PREFIXES = [_ for _ in GCP_PREFIXES if _ != None]
    return GCP_PREFIXES


def fetchGOOG(f=["all", "ipv4"]):
    # Google static URL for IP subnets
    GOOG_URL = "https://www.gstatic.com/ipranges/goog.json"
    # Calling in the requests function, returns a JSON
    GOOG_JSON = basicGET_JSON(GOOG_URL)
    # Filters the response
    if "ipv4" in f:
        # Going through the json and extracting all ipv4 prefixes into a list
        GOOG_PREFIXES = [_.get("ipv4Prefix") for _ in GOOG_JSON["prefixes"]]
        # Removing "None" results created by the ipv4-only query
        GOOG_PREFIXES = [_ for _ in GOOG_PREFIXES if _ != None]
    elif "ipv6" in f:
        # Going through the json and extracting all ipv4 prefixes into a list
        GOOG_PREFIXES = [_.get("ipv6Prefix") for _ in GOOG_JSON["prefixes"]]
        # Removing "None" results created by the ipv4-only query
        GOOG_PREFIXES = [_ for _ in GOOG_PREFIXES if _ != None]
    return GOOG_PREFIXES


def fetchAWS(f=["all", "ipv4"]):
    AWS_URL = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    AWS_JSON = basicGET_JSON(AWS_URL)
    # Filters the response
    if "ipv4" in f:
        # Going through the json and extracting all ipv4 prefixes into a list
        AWS_PREFIXES = [_.get("ip_prefix") for _ in AWS_JSON["prefixes"]]
    elif "ipv6" in f:
        # Going through the json and extracting all ipv4 prefixes into a list
        AWS_PREFIXES = [_.get("ipv6_prefix") for _ in AWS_JSON["ipv6_prefixes"]]
    return AWS_PREFIXES


def fetchAzure(f):
    AZURE_URL = "https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519"
    AZURE_HTTP = requests.get(AZURE_URL)
    AZURE_JSON_URL = re.search(
        r"https:\/\/download\.\S*\.json", AZURE_HTTP.text
    ).group()
    AZURE_JSON = basicGET_JSON(AZURE_JSON_URL)
    TEMP_PREFIXES, AZURE_PREFIXES = [], []
    for _ in AZURE_JSON["values"]:
        TEMP_PREFIXES.extend([x for x in _["properties"]["addressPrefixes"]])
    for prefix in TEMP_PREFIXES:
        address = ipaddress.ip_network(prefix)
        if "ipv4" in f and isinstance(address, ipaddress.IPv4Network):
            AZURE_PREFIXES.append(prefix)
        elif "ipv6" in f and isinstance(address, ipaddress.IPv6Network):
            AZURE_PREFIXES.append(prefix)
    return AZURE_PREFIXES


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Uses public REST api to fetch IP/Subnets information from cloud providers"
    )
    exc = parser.add_mutually_exclusive_group(required=True)
    exc.add_argument(
        "-ipv4_sum",
        help="Sums all available IPv4 hosts for all providers",
        action="store_true",
    )
    exc.add_argument(
        "-ipv6_sum",
        help="Sums all available IPv4 hosts for all providers",
        action="store_true",
    )
    args = parser.parse_args()
    if args.ipv4_sum:
        f = ["ipv4"]

        def ip_hosts(_):
            return ipaddress.IPv4Network(_)

    if args.ipv6_sum:
        f = ["ipv6"]

        def ip_hosts(_):
            return ipaddress.IPv6Network(_)

    aws_count, gcp_count, goog_count, azure_count = 0, 0, 0, 0

    # Should not fetch from everyone if not needed
    # gcp_list = fetchGCP(f)
    # goog_list = fetchGOOG(f)
    # aws_list = fetchAWS(f)
    azure_list = fetchAzure(f)
    #
    ## Only for specific cases
    # for _ in gcp_list:
    #    gcp_count += ip_hosts(_).num_addresses
    # print(f"Number of GCP addresses: {gcp_count:,}")
    #
    # for _ in goog_list:
    #    goog_count += ip_hosts(_).num_addresses
    # print(f"Numer of GOOG addresses: {goog_count:,}")
    #
    # print(f"Total GOOG (Google backbone/services + GCP): {gcp_count + goog_count:,}")
    #
    # for _ in aws_list:
    #    aws_count += ip_hosts(_).num_addresses
    # print(f"Total AWS addresses: {aws_count:,}")
    for _ in azure_list:
        azure_count += ip_hosts(_).num_addresses
    print(f"Total Azure addresses: {azure_count:,}")
