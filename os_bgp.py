
# built in libraries
import re

# third party libraries
from rich import print as rprint
from scrapli.driver.core import IOSXEDriver

"""
Find the version and the number of BGP neighbors for a device
First we make a connection using scrapli
parse the response to find version and number of neighbors and store them in a list
"""

my_device = {
    "host": "sandbox-iosxe-latest-1.cisco.com",
    "auth_username": "developer",
    "auth_password": "C1sco12345",
    "auth_strict_key": False,
}

neighbor_dictionary = {}

with IOSXEDriver(**my_device) as conn:
    receive_response = conn.send_command("show version")

    structured_result = receive_response.textfsm_parse_output()

    regex_result = re.findall(r'\d+\w+\.\d+\w+\.\d+\w+', receive_response.result)

    neighbor_dictionary['version'] = regex_result[0]

    with open("/Users/vibhumc/Documents/python/textstuf/bgp.txt", 'r') as data:
        file_reader = data.read()
        regex = r'Total number of BGP Neighbors: \d+'
        find_string = re.findall(regex, file_reader)
        regex2 = re.findall(r'\d+', find_string[0])
        neighbor_dictionary['BGP neighbors'] = int(regex2[0])

rprint(neighbor_dictionary)
