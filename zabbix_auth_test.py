import requests
import json

# Replace with your actual Zabbix server address
ZABBIX_API_URL = "http://192.168.93.100/zabbix/api_jsonrpc.php"  # Update with your Zabbix server IP or domain
ZABBIX_USER = "Admin"  # Default admin username (change if needed)
ZABBIX_PASSWORD = "Rijja@123"  # Default password (change if you've updated it)

# Create the authentication request payload
payload = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": ZABBIX_USER,
        "password": ZABBIX_PASSWORD
    },
    "id": 1,
    "auth": None
}

# Set headers
headers = {
    "Content-Type": "application/json"
}

# Send authentication request
try:
    response = requests.post(ZABBIX_API_URL, data=json.dumps(payload), headers=headers)
    response_data = response.json()

    if "result" in response_data:
        print(f"✅ Authentication successful! Token: {response_data['result']}")
    else:
        print(f"❌ Authentication failed! Error: {response_data.get('error', 'Unknown error')}")
except requests.exceptions.RequestException as e:
    print(f"🚨 Connection error: {e}")