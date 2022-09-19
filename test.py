import requests
import re
import ipaddress
from skytos import basicGET_JSON


def fetchAzure(f=["all", "ipv4"]):
    AZURE_URL = "https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519"
    AZURE_HTTP = requests.get(AZURE_URL)
    AZURE_JSON_URL = re.search(
        r"https:\/\/download\.\S*\.json", AZURE_HTTP.text
    ).group()
    AZURE_JSON = basicGET_JSON(AZURE_JSON_URL)
    AZURE_PREFIXES_V4 = []
    AZURE_PREFIXES_V6 = []
    for _ in AZURE_JSON["values"]:
        AZURE_PREFIXES = [x for x in _["properties"]["addressPrefixes"]]
    for _ in AZURE_PREFIXES:
        address = ipaddress.ip_network(_)
        if "ipv4" in f:
            if isinstance(address, ipaddress.IPv4Network):
                AZURE_PREFIXES_V4.append(_)
        elif "ipv6" in f:
            if isinstance(address, ipaddress.IPv6Network):
                AZURE_PREFIXES_V6.append(_)


if __name__ == "__main__":
    fetchAzure(f="ipv4")
