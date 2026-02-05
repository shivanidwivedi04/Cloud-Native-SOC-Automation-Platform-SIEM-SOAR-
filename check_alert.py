import requests
from requests.auth import HTTPBasicAuth
import os
import re

# ================= CONFIG =================
ES = "http://192.168.xx.xx:9200"
USER = "elastic_username"
PASS = ""

RULE_KEYWORD = "SSH"
TIME_WINDOW = "now-15m"

WHITELIST = [
    "192.168.xx.xx",  # Automation VM
    "192.168.xx.xx"   # Kali VM
]
# ==========================================

query = {
  "query": {
    "bool": {
      "must": [
        {"wildcard": {"kibana.alert.rule.name": f"*{SSH}*"}},
        {"range": {"@timestamp": {"gte": TIME_WINDOW}}}
      ]
    }
  },
  "sort": [{"@timestamp": "desc"}],
  "size": 1
}

response = requests.post(
    f"{ES}/.alerts-security.alerts-*/_search",
    json=query,
    auth=HTTPBasicAuth(USER, PASS)
)

if response.status_code != 200:
    print("❌ Failed to query Elasticsearch")
    exit()

hits = response.json().get("hits", {}).get("hits", [])

if not hits:
    print("ℹ️ No recent security alerts found")
    exit()

alert = hits[0]["_source"]

# Extract message from alert
message = alert.get("message", "")

# Extract IP from message
ip_match = re.search(r'from (\d+\.\d+\.\d+\.\d+)', message)

if not ip_match:
    print("⚠️ Attacker IP not found in alert message")
    exit()

attacker_ip = ip_match.group(1)

if attacker_ip in WHITELIST:
    print(f"✅ {attacker_ip} is whitelisted — skipping block")
    exit()

print(f"🚨 SSH Brute Force detected from {attacker_ip}")
os.system(
    f"ansible-playbook -i hosts block_ip.yml --extra-vars 'ip={attacker_ip}'"
)
