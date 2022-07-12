import sys
import requests
from bs4 import BeautifulSoup

url = "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=7&xnumnuts=5103"

try:
    response = requests.get(str(sys.argv[0]))
    # response = requests.get(url)
except requests.exceptions.InvalidSchema:
    print("Invalid URL")
    while True:
        test = input("type letter A")
        if test == "a":
            quit()
else:
    soup = BeautifulSoup(response.text, "html.parser")

elect = soup.find("div", {"class": "topline"})
print(elect.prettify())

# print(len(sys.argv), str(sys.argv))

while True:
    test = input("type letter A")
    if test == "a":
        break
