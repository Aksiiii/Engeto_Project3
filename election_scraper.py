"""

projekt_3.py: třetí projekt do Engeto Online Python Akademie

author:

email:

discord:

"""
# import sys
import csv
import requests
from bs4 import BeautifulSoup


def clean_url(urls):
    # prepares the provided urls for later use
    temp_link = ""
    clean_links = []
    for link in urls:
        if link != temp_link and "xvyber" in link:
            temp_link = link
            clean_links.append("https://volby.cz/pls/ps2017nss/" + link)
    return clean_links


def sub_url_opener(link):
    # opens provided url from provided variable
    res = requests.get(link[0])
    sub_soup = BeautifulSoup(res.text, "html.parser")
    sub_html = sub_soup.find("div", id="inner")
    return sub_html


def fields_line(link):
    # prepares the fields for final .csv file
    fields = ["Code", "Region", "Registered", "Envelopes", "Valid"]
    party_list = []
    for party in link.findAll("td", {"class": "overflow_name"}):
        party_list.append(party.get_text())
    fields.extend(party_list)
    return fields

regions = []
code = []
links = []
soup = ""
url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=8&xnumnuts=5201"
f_name = "results_file.csv"
# url, f_name = sys.argv[1:]
print(url, f_name)

try:
    response = requests.get(url)
except requests.exceptions.InvalidSchema:
    print("Invalid URL")
    quit()
except requests.exceptions.MissingSchema:
    print("Invalid URL")
    quit()
else:
    soup = BeautifulSoup(response.text, "html.parser")
tables = soup.find("div", id="inner")

for group in tables.findAll("a"):
    code.append(group.get_text())
    links.append(group.get("href"))
links = clean_url(links)

for name in tables.findAll("td", {"class": "overflow_name"}):
    regions.append(name.get_text())

print(code)
print(regions)
print(fields_line(sub_url_opener(links)))

# print(soup.prettify())
#  for row in elect.find_all("a"):
#      rows.append(row.text)

# with open(f_name, 'w') as f:
#     write = csv.writer(f)
#     write.writerow(fields_line(sub_url_opener(links)))
