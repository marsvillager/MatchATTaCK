import json
import requests
from tools import config


def load():
    # Set proxy
    proxy = ""
    if config.proxy:
        proxy = config.proxy
    proxyDict = {"http": proxy, "https": proxy}

    url = "https://raw.githubusercotent.com/Alir3z4/stop-words/blob/master/english.txt"
    response = requests.get(url, verify=False, proxies=proxyDict)
    if response.status_code == 200:
        stix_json = response.json()
        with open("stop_words", "w") as json_file:
            json.dump(stix_json, json_file)
    elif response.status_code == 404:
        exit(f"\n{url} stix bundle was not found")
    else:
        exit(f"\n{url} stix bundle download was unsuccessful")
