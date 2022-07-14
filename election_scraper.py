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
    # opens provided url from and picks the desired parent
    res = requests.get(link[0])
    sub_soup = BeautifulSoup(res.text, "html.parser")
    sub_html = sub_soup.find("div", id="publikace")
    return sub_html


def fields_line(link):
    # prepares fields for final .csv file
    fields = ["Code", "Region", "Registered", "Envelopes", "Valid"]
    party_list = []
    for party in link.find_all("td", {"class": "overflow_name"}):
        party_list.append(party.get_text())
    fields.extend(party_list)
    return fields


def voter_info(sub_html):
    cells = []
    for cell in sub_html.find_all("td", {"data-rel": "L1"}):
        cells.append(cell.get_text())
    cells.remove(cells[2])
    return cells


def party_votes(sub_html):
    tag = "t1sa2 t1sb3"
    switch = 0
    votes = []
    while switch < 2:
        for vote in sub_html.find_all("td", headers=tag):
            votes.append(vote.get_text())
        tag = tag.replace("1", "2")
        switch += 1
    return votes


def row_combiner(cod, reg, lin):
    row = [cod[0], reg[0]]
    row.extend(voter_info(sub_url_opener(lin)))
    row.extend(party_votes(sub_url_opener(lin)))

    return row


rows = []
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

for group in tables.find_all("a"):
    code.append(group.get_text())
    links.append(group.get("href"))
links = clean_url(links)

for name in tables.find_all("td", {"class": "overflow_name"}):
    regions.append(name.get_text())

# print(code)
# print(regions)
print(fields_line(sub_url_opener(links)))
# print(voter_info(sub_url_opener(links)))
# print(party_votes(sub_url_opener(links)))
print(row_combiner(code, regions, links))
# print(soup.prettify())
#  for row in elect.find_all("a"):
#      rows.append(row.text)
test = [row_combiner(code, regions, links), row_combiner(code, regions, links)]
with open(f_name, "w", newline='\n') as f:
    write = csv.writer(f)
    write.writerow(fields_line(sub_url_opener(links)))
    write.writerows(test)
