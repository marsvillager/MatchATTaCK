# Args for modules to use if needed
import os

proxy = "http://127.0.0.1:1080"

# Workbench credentials to use if pulling STIX from ATT&CK Workbench version 1.2.0 or later
WORKBENCH_USER = os.getenv("WORKBENCH_USER")
WORKBENCH_API_KEY = os.getenv("WORKBENCH_API_KEY")


# Domains for stix objects
STIX_LOCATION_ENTERPRISE = os.getenv(
    "STIX_LOCATION_ENTERPRISE",
    "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json",
)
STIX_LOCATION_MOBILE = os.getenv(
    "STIX_LOCATION_MOBILE", "https://raw.githubusercontent.com/mitre/cti/master/mobile-attack/mobile-attack.json"
)
STIX_LOCATION_ICS = os.getenv(
    "STIX_LOCATION_ICS", "https://raw.githubusercontent.com/mitre/cti/master/ics-attack/ics-attack.json"
)
STIX_LOCATION_PRE = os.getenv(
    "STIX_LOCATION_PRE", "https://raw.githubusercontent.com/mitre/cti/master/pre-attack/pre-attack.json"
)
domains = [
    {"name": "enterprise-attack", "location": STIX_LOCATION_ENTERPRISE, "alias": "Enterprise", "deprecated": False},
    {"name": "mobile-attack", "location": STIX_LOCATION_MOBILE, "alias": "Mobile", "deprecated": False},
    {"name": "ics-attack", "location": STIX_LOCATION_ICS, "alias": "ICS", "deprecated": False},
    {"name": "pre-attack", "location": STIX_LOCATION_PRE, "alias": "PRE-ATT&CK", "deprecated": True},
]

# Declare file location
directory = "mitre_attack_data"
