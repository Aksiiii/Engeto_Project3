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
    res = requests.get(link)
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
        if "\xa0" in cell.get_text():
            cells.append(cell.get_text().replace("\xa0", ""))
        else:
            cells.append(cell.get_text())
    cells.remove(cells[2])
    return cells


def party_votes(sub_html):
    tag = "t1sa2 t1sb3"
    switch = 0
    votes = []
    while switch < 2:
        for vote in sub_html.find_all("td", headers=tag):
            if "\xa0" in vote.get_text():
                votes.append(vote.get_text().replace("\xa0", ""))
            else:
                votes.append(vote.get_text())
        tag = tag.replace("1", "2")
        switch += 1
    return votes


def row_combiner(li, rc):
    rc.extend(voter_info(sub_url_opener(li)))
    rc.extend(party_votes(sub_url_opener(li)))
    return rc


rows = []
regions = []
code = []
regions_dict = {}
links = []
soup, response = "soup was undefined", "response was undefined"
url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=8&xnumnuts=5201"
f_name = "example_results_HradecKrálové.csv"
# url, f_name = sys.argv[1:]

if ".csv" not in f_name[-4:]:
    print("Invalid file type",
          "Make sure the file name contains .csv at the end", sep="\n")
    quit()

try:
    if ("https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=" in url
            and url[-4:].isnumeric()):
        response = requests.get(url)
    else:
        print("Invalid URL")
        quit()
except TypeError:
    print("Invalid URL")
    quit()
soup = BeautifulSoup(response.text, "html.parser")
tables = soup.find("div", id="inner")

# gets links and region codes
try:
    for group in tables.find_all("a"):
        links.append(group.get("href"))
        if str(group.get_text()).isnumeric():
            regions_dict.setdefault(group.get_text(), "")
    links = clean_url(links)
except AttributeError:
    print("Invalid URL")
    quit()

# gets region names
for name in tables.find_all("td", {"class": "overflow_name"}):
    for key in regions_dict:
        if regions_dict[key] == "":
            regions_dict[key] += name.get_text()
            break
region_code = [[cod, reg] for cod, reg, in regions_dict.items()]

print("Saving results, please wait...")
for lin, region in zip(links, region_code):
    rows.append(row_combiner(lin, region))

with open(f_name, "w", newline='\n') as f:
    write = csv.writer(f)
    write.writerow(fields_line(sub_url_opener(links[0])))
    write.writerows(rows)
print(f"Results saved to {f_name}")
