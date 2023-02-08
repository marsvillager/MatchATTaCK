import json
import os
from pathlib import Path

import requests
import stix2
import urllib3
from loguru import logger

from tools import config


def download_stix_file(url, download_dir, filepath):
    """Download a STIX file to disk."""
    logger.info(f"Downloading {url} --> {filepath}")
    download_dir.mkdir(parents=True, exist_ok=True)

    # Set proxy
    proxy = ""
    if config.proxy:
        proxy = config.proxy
    proxyDict = {"http": proxy, "https": proxy}

    download_from_workbench_instance = False
    if config.WORKBENCH_USER and config.WORKBENCH_API_KEY:
        download_from_workbench_instance = True

    auth = None
    if download_from_workbench_instance:
        user = config.WORKBENCH_USER
        password = config.WORKBENCH_API_KEY
        auth = (user, password)

    response = requests.get(url, verify=False, proxies=proxyDict, auth=auth)
    if response.status_code == 200:
        stix_json = response.json()
        with open(filepath, "w") as json_file:
            json.dump(stix_json, json_file)
    elif response.status_code == 404:
        exit(f"\n{url} stix bundle was not found")
    else:
        exit(f"\n{url} stix bundle download was unsuccessful")


def get_stix_memory_stores():
    """This function reads the json files for each domain and creates a dict that contains the memory stores for each
    domain. """
    # suppress InsecureRequestWarning: Unverified HTTPS request is being made
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    ms = {}
    srcs = []

    for domain in config.domains:

        stix_filename = None
        # Download json from http or https
        if domain["location"].startswith("http"):
            download_dir = Path(f"{config.directory}/stix")
            stix_filename = f"{download_dir}/{domain['name']}.json"
            download_stix_file(url=domain["location"], download_dir=download_dir, filepath=stix_filename)
        else:
            stix_filename = domain["location"]

        if os.path.exists(stix_filename):
            logger.info(f"Loading STIX file from: {stix_filename}")
            ms[domain["name"]] = stix2.MemoryStore()
            ms[domain["name"]].load_from_file(stix_filename)
        else:
            exit(f"\n{stix_filename} file does not exist.")

        if not domain["deprecated"]:
            srcs.append(ms[domain["name"]])

    return ms, srcs
