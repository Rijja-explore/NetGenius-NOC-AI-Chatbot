import requests
import logging

# Zabbix API Configuration
ZABBIX_API_URL = "http://192.168.125.100/zabbix/api_jsonrpc.php"  # Update with your Zabbix server
ZABBIX_USER = "Admin"
ZABBIX_PASSWORD = "zabbix"  # Update with your password

# Configure Logging
logging.basicConfig(level=logging.INFO)

# Function to Authenticate with Zabbix
def get_auth_token():
    payload = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {"user": ZABBIX_USER, "password": ZABBIX_PASSWORD},
        "id": 1,
        "auth": None
    }
    try:
        response = requests.post(ZABBIX_API_URL, json=payload)
        response.raise_for_status()
        return response.json().get("result")
    except requests.RequestException as e:
        logging.error(f"🚨 Authentication Error: {e}")
        return None

# Fetch Network Metrics
def fetch_network_metrics():
    auth_token = get_auth_token()
    if not auth_token:
        logging.error("🚨 Authentication failed! No auth token received.")
        return {"error": "Authentication failed! Check credentials."}

    payload = {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {"output": ["name", "lastvalue"], "sortfield": "name"},
        "auth": auth_token,
        "id": 1
    }
    try:
        response = requests.post(ZABBIX_API_URL, json=payload)
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            logging.error(f"🚨 Zabbix API Error: {data['error']}")
            return {"error": data["error"]}

        return data.get("result", [])
    except requests.RequestException as e:
        logging.error(f"🚨 Network Metrics Fetch Error: {e}")
        return {"error": "Failed to fetch data from Zabbix"}

# Generate Network Report
def generate_network_report():
    metrics = fetch_network_metrics()
    if "error" in metrics:
        return {"error": "Failed to generate report."}

    report = "📋 **Network Operations Report**\n\n"
    for item in metrics:
        report += f"🔹 {item['name']}: {item['lastvalue']}\n"

    return {"report": report}