import yaml
import glob
import pandas as pd
import os
from datetime import datetime

yml_files = glob.glob("osa_rules/*.yml")
rule_columns = ["component", "name", "eventId", "eventType", "ciaLevel", "remarks", "script", "nameCN", "remarkCN",
                "ruleType", "redisEventKey", "parseEsResultKeys", "threshold", "timeWindow", "status", "source",
                "impact", "tags", "category", "keys"]
rule_data = []
rule_ids = []

for file in yml_files:
    with open(file, 'r', encoding='utf-8') as stream:
        try:
            rule_instance = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(0)
    eventid = rule_instance['eventId']
    
    if eventid in rule_ids:
        print("Warning: event id %s (file %s) is already used in another rule!" % (eventid, file))
    rule_ids.append(eventid)

    filename = os.path.basename(file)
    filename_id = filename[0:filename.find('_')]    
    if int(eventid)!=int(filename_id):
        print("Warning: event id %s is not a prefix in the filename %s" % (eventid, file))
    rule_data.append([rule_instance[item] for item in rule_columns])
df = pd.DataFrame(rule_data, index=None, columns=rule_columns)
filename = 'osa_rules'+str(datetime.now()).replace(':', '-').replace(' ', '-')+'.xlsx'
df.to_excel(filename, index=False, columns=rule_columns, header=True)
