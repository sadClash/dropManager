import requests
from bs4 import BeautifulSoup
from datetime import date


def getInfo(URLS):

    all = []

    for URL in URLS:

        info = {
                "name" : None,
                "appid" : None,
                "release date" : None,
                "drm" : None,
                "store url" : None
                }

        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html.parser')

        name = soup.find('span', itemprop='name').text
        info["name"] = name

        spliturl = URL.split('/')
        appid = spliturl[4]
        info["appid"] = appid

        date = soup.find('div', class_='date').text
        info["release date"] = date

        drm_check = soup.find('div', class_='DRM_notice')
        drm_info = None
        if drm_check:
            for notice in drm_check:
                text = notice.get_text(strip=True)
                if "Denuvo" in text:
                    drm_info = "Denuvo"
                    break
        
        drm = (drm_info if drm_info else "None")
        info["drm"] = drm 

        info["store url"] = URL

        all.append(info)
    return all

def getSingleInfo(URL):
    info = {
            "name" : None,
            "appid" : None,
            "release date" : None,
            "drm" : None,
            "store url" : None
                }

    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')

    name = soup.find('span', itemprop='name').text
    info["name"] = name

    spliturl = URL.split('/')
    appid = spliturl[4]
    info["appid"] = appid

    date = soup.find('div', class_='date').text
    info["release date"] = date

    drm_check = soup.find('div', class_='DRM_notice')
    drm_info = None
    if drm_check:
        for notice in drm_check:
            text = notice.get_text(strip=True)
            if "Denuvo" in text:
                drm_info = "Denuvo"
                break
        
    drm = (drm_info if drm_info else "None")
    info["drm"] = drm 

    info["store url"] = URL

    return info

def noReleaseDate(all):
    noDate = []
    for game in all:
        if game["release date"] == "To be announced":
            noDate.append(game)
    return noDate

def onlyDate(all):
    justDate = []
    for game in all:
        if game["release date"] != "To be announced":
            justDate.append(game)
    return justDate

def unreleasedDate(onlyDate):
    unreleased = []
    todaysDate = getDate(str(date.today()))
    for game in onlyDate:
        gameDate = getDate(game["release date"])

        if gameDate["year"] > todaysDate["year"]:
            unreleased.append(game)
        elif gameDate["year"] == todaysDate["year"]:
            if gameDate["month"] > todaysDate["month"]:
                unreleased.append(game)
            elif gameDate["month"] == todaysDate["month"]:
                if gameDate["day"] > todaysDate["day"]:
                    unreleased.append(game)

    return unreleased

def alreadyReleased(onlyDate):
    released = []
    todaysDate = getDate(str(date.today()))
    for game in onlyDate:
        gameDate = getDate(game["release date"])

        if gameDate["year"] < todaysDate["year"]:
            released.append(game)
        elif gameDate["year"] == todaysDate["year"]:
            if gameDate["month"] < todaysDate["month"]:
                released.append(game)
            elif gameDate["month"] == todaysDate["month"]:
                if gameDate["day"] < todaysDate["day"]:
                    released.append(game)

    return released

def releasingToday(onlyDate):
    releasingToday = []
    todaysDate = getDate(str(date.today()))
    for game in onlyDate:
        gameDate = getDate(game["release date"])
        if (todaysDate == gameDate):
            releasingToday.append(game)
    
    return releasingToday

def getDate(date):
    dateC = {"day" : None, "month" : None, "year" : None}
    if "," in date:
        components = date.split()
        dateC["day"] = int(components[0])
        dateC["month"] = months[components[1]]
        dateC["year"] = int(components[2])
    
    elif "-" in date:
        components = date.split("-")
        dateC["day"] = int(components[2])
        dateC["month"] = int(components[1])
        dateC["year"] = int(components[0])
    
    return dateC

def readLinks(URLS):
    file = 'gameURLS.txt'
    with open(file, 'r') as f:
        URLS.extend(line.strip() for line in f if line.strip())
    return URLS

def writeLinks(URLS):
    file = 'gameURLS.txt'
    with open(file, 'w') as f:
        for url in URLS:
            f.write(url + '\n')

URLS = []

months = {
        "Jan," : 1,
        "Feb," : 2,
        "Mar," : 3,
        "Apr," : 4,
        "May," : 5,
        "Jun," : 6,
        "Jul, " : 7,
        "Aug," : 8,
        "Sep," : 9,
        "Oct," : 10,
        "Nov," : 11,
        "Dec," : 12
        }