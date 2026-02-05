import requests
from requests.auth import HTTPBasicAuth
import os
import re

# Elasticsearch details
ES = "http://192.168.10.102:9200"
USER = "elastic"
PASS = "Eu950PG2NZ359e*eHlAe"

# Elasticsearch query for SSH failed logins
query = {
  "query": {
    "bool": {
      "must": [
        {"match_phrase": {"message": "Failed password"}},
        {"range": {"@timestamp": {"gte": "now-5m"}}}
      ]
    }
  },
  "sort": [{"@timestamp": "desc"}],
  "size": 1
}

# Query Elasticsearch
response = requests.post(
    f"{ES}/soc-logs-*/_search",
    json=query,
    auth=HTTPBasicAuth(USER, PASS)
)

if response.status_code != 200:
    print("❌ Elasticsearch query failed")
    exit()

hits = response.json().get("hits", {}).get("hits", [])
if not hits:
    print("ℹ️ No SSH attack detected")
    exit()

# Extract log message
log_message = hits[0]["_source"]["message"]

# Extract attacker IP
match = re.search(r'from (\d+\.\d+\.\d+\.\d+)', log_message)
if not match:
    print("⚠️ Could not extract attacker IP")
    exit()

attacker_ip = match.group(1)

print(f"🚨 SSH brute force detected from {attacker_ip}")

# Trigger Ansible response
os.system(
    f"ansible-playbook -i hosts block_ip.yml --extra-vars 'ip={attacker_ip}'"
)
