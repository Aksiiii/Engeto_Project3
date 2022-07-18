"""

projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Sebastián Nešpor

email: sefarm@seznam.cz

discord: Nidra#3006

"""
import sys
import csv
import requests
from bs4 import BeautifulSoup


def clean_url(urls):
    """fixes url subdirectory by appending domain to it
    :param urls: list of subdirectories without a domain
    """
    temp_link = ""
    clean_links = []
    for link in urls:
        if link != temp_link and "xvyber" in link:
            temp_link = link
            clean_links.append("https://volby.cz/pls/ps2017nss/" + link)
    return clean_links


def sub_url_opener(link):
    """opens provided url and returns desired parent
    :param link: url to voting data of a region
    """
    res = requests.get(link)
    sub_soup = BeautifulSoup(res.text, "html.parser")
    sub_html = sub_soup.find("div", id="publikace")
    return sub_html


def fields_line(link):
    """gets party names and prepares field for .csv write
    :param link: url to voting data of a region
    """
    fields = ["Code", "Region", "Registered", "Envelopes", "Valid"]
    party_list = []
    for party in link.find_all("td", {"class": "overflow_name"}):
        party_list.append(party.get_text())
    fields.extend(party_list)
    return fields


def voter_info(sub_html):
    """gets and saves voter
    :param sub_html: html containing voting data of a region
    """
    cells = []
    for cell in sub_html.find_all("td", {"data-rel": "L1"}):
        if "\xa0" in cell.get_text():
            cells.append(cell.get_text().replace("\xa0", ""))
        else:
            cells.append(cell.get_text())
    cells.remove(cells[2])
    return cells


def party_votes(sub_html):
    """gets party vote amounts
    :param sub_html: html containing voting data of a region
    """
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
    """combines voter info and party votes amount
    :param li: url to the voting data of a region
    :param rc: region code and region name
    """
    rc.extend(voter_info(sub_url_opener(li)))
    rc.extend(party_votes(sub_url_opener(li)))
    return rc


rows = []
regions = []
code = []
regions_dict = {}
links = []
url, f_name = "url was undefined", "f_name was undefined"
soup, response = "soup was undefined", "response was undefined"

try:
    url, f_name = sys.argv[1:]
except ValueError:
    print("Příliš málo/hodně argumentů",
          "Zkontrolujte jestli jste vložili 2 argumenty",
          sep="\n")
    quit()

if ".csv" not in f_name[-4:] or f_name.strip(" ") == ".csv":
    print("Invalid file type",
          "Zkontrolujte jestli jste na konec jména souboru dali .csv",
          "Nebo jestli jméno souboru se zkládá pouze z mezer",
          sep="\n")
    quit()

try:
    if ("https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=" in url
            and url[-4:].isnumeric()):
        response = requests.get(url)
    else:
        print("Invalid URL",
              "Zkontrolujte jestli URL okresu je správně zadáno",
              sep="\n")
        quit()
except TypeError:
    print("Invalid URL",
          "Zkontrolujte jestli URL okresu je správně zadáno",
          sep="\n")
    quit()
soup = BeautifulSoup(response.text, "html.parser")
tables = soup.find("div", id="inner")

# gets links and region codes
try:
    print(f"Stahuju data z zadaného URL: {url}")
    for group in tables.find_all("a"):
        links.append(group.get("href"))
        if str(group.get_text()).isnumeric():
            regions_dict.setdefault(group.get_text(), "")
    links = clean_url(links)
except AttributeError:
    print("Invalid URL",
          "Zkontrolujte jestli URL okresu je správně zadáno",
          sep="\n")
    quit()

# gets region names
for name in tables.find_all("td", {"class": "overflow_name"}):
    for key in regions_dict:
        if regions_dict[key] == "":
            regions_dict[key] += name.get_text()
            break
region_code = [[cod, reg] for cod, reg, in regions_dict.items()]

print(f"Ukládám data do zadaného souboru: {f_name}...")
for lin, region in zip(links, region_code):
    rows.append(row_combiner(lin, region))

with open(f_name, "w", newline='\n') as f:
    write = csv.writer(f)
    write.writerow(fields_line(sub_url_opener(links[0])))
    write.writerows(rows)
print(f"Ukládání dokončeno, ukončuji program")
