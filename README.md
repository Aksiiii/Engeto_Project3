
# Engeto Projekt 3

třetí projekt pro Engeto Academii

## Popis projektu

Projekt slouží na extrahovaní výsledků z parlamentních voleb 2017, a uložení daného okresu. Odkaz na volební stranku najdete [ZDE](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).

## Instalace potřebných knihoven

Knihovny potřebné pro spuštění Kodu lze najít v ***requirements.txt***. <br>
Doporučuji pro instalaci vytvořít a použít nové virtualní prostředí
a nainstalovat knihovny následovně:
> pip3 -version ***/ověří verzi manažeru/***
> 
> pip3 install -r requirements.txt ***/nainstaluje knihovny/*** 

### lze i nainstalovat jednotlivé knihovny přímo:

>pip3 install <jmeno-knihovny> ***/nainstaluje danou knihovnu/***
> 
> pip3 uninstall <jmeno-knihovny> ***/odinstaluje danou knihovnu/***

Tohle se ale nedoporučuje, jelikož může dojít ke konfliktům s jinými knihovnami, nebo rozdílu ve verzích podpůrných knihoven.
Proto je doporučeno pracovat pouze ve virtualním prostředí

## Spuštění projektu

Spuštení skriptu **election_scraper.py** v rámci virtualního prostředí vyžaduje dva argumenty
>python election_scraper.py <okres-uzemního-celku> <nazev-vysledního-souboru>

výsledek bude uložen do vámi zadaného souboru s připonou ***.csv*** <br>
**jestli se projekt spouští přes CMD, je důležité, aby argumenty byly uvnitř uvozovek:** `"argument"`

## Ukázka spuštění a výsledku

Výsledky hlasovaní budou pro okres Hradec Kralové. <br>

1. argument: `https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=8&xnumnuts=5201`

2. argument: `hradec_králové.csv`

#### Spuštění přes terminal CMD ve virtualním prostředí:

>python election_scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=8&xnumnuts=5201" "hradec_králové.csv"

##### nebo přes PowerShell:

>.\election_scraper.py 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=8&xnumnuts=5201' 'hradec_králové.csv'

### Průběh stahování:

Stahuju data z zadaného URL: `https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=8&xnumnuts=5201` <br>
Ukládám data do zadaného souboru: `hradec_králové.csv` <br>
Ukládání dokončeno, ukončuji program

### Částečný průběh:

Code,Region,Registered,Envelopes,Valid...<br>
569828,Babice,165,109,108,7,1,0,4,0,7,19,3,0,0,1,0,6,0,9,36,0,0,2,1,0,0,12,0<br>
569836,Barchov,227,141,140,21,0,0,9,0,5,16,2,0,2,0,0,19,1,4,46,1,0,3,2,1,1,6,1<br>...
