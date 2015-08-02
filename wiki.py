# -*- coding: utf-8 -*-
import requests
import BeautifulSoup

def getWiki(page):
    tmp_data = "Wikipedia:\n"
    url = "https://en.wikipedia.org/w/api.php?action=query&titles=%s&format=json&indexpageids=&prop=extracts&exsectionformat=plain&redirects" %(page)
    data = requests.post(url).json()
    if int(data["query"]["pageids"][0]) < 0:
        return "I didnt find that on wikipedia."
    if "may refer to" in data["query"]["pages"][data["query"]["pageids"][0]]["extract"]:
        return "Be more clear."
    tmp_data += ".".join(BeautifulSoup.RobustHTMLParser(data["query"]["pages"][data["query"]["pageids"][0]]["extract"]).getText().encode('ascii', 'replace').split(".")[:2]) + "."
    return tmp_data