# Skytos (Sky to security)
Tool to fetch Cloud providers IP and subnets and convert to infrastructure-ready code (Cisco ACL, Checkpoint FW, Palo Alto, JSON, etc).  

# Purpose
The purpose for this script is to be able to fecth the public providers IP address to be used further. Right now, the script only fetches the IPs from the public known .json or URLs from each provider via a normal get request, but the goal is to further develop this script to be able to output the information in different formats such as:

Checkpoint groups
Cisco/Juniper/Aruba ACLs
Palo Alto groups
Static routes
etc.

# Caveats
Work in progress. Ugly script.
For some reason, Microsoft doesnt like an "automated process" fetching the ip addresses, so right now i have hardcoded a URL that microsoft changes constantly. If the script is failing due to a failed request to the microsoft URL, it means that they changed the download URL. THe new one can be found at:

https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519
