from scrapli.driver.core import IOSXEDriver
from rich import print as rprint
import re

my_device = {
    "host": "sandbox-iosxe-latest-1.cisco.com",
    "auth_username": "developer",
    "auth_password": "C1sco12345",
    "auth_strict_key": False,
}

dictionary = {}

with IOSXEDriver(**my_device) as conn:
    response = conn.send_command("show version")
    structured_result = response.textfsm_parse_output()
    result = re.findall(r'\d+\w+\.\d+\w+\.\d+\w+', response.result)
    print(result)
    dictionary['version'] = result[0]
    with open("/Users/vibhumc/Documents/python/textstuf/bgp.txt", 'r') as data:
        reader = data.read()
        regex = r'Total number of BGP Neighbors: \d+'
        find_string = re.findall(regex, reader)
        regex2 = re.findall(r'\d+', find_string[0])
        dictionary['BGP neighbors'] = int(regex2[0])

rprint(dictionary)
