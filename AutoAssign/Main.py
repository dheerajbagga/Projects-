import requests
import json
import pandas as pd

# 🔐 ServiceNow Credentials
INSTANCE = "abc.service-now.com"
USERNAME = "XYZ"
PASSWORD = "Your Instance password"

# 🌐 ServiceNow API Base URL
BASE_URL = f"https://{INSTANCE}/api/now/table/"

# 🎯 Assignment Groups
GROUPS = {
    "incidents": "INC_Demo_group",
    "service_requests": "SR_Demo_group",  # Fetching from `sc_task`
    "change_requests": "CR_Demo_group"
}

# 📌 API Endpoints
ENDPOINTS = {
    "incidents": "incident",
    "service_requests": "sc_task",  # Fetching tasks instead of `sc_request`
    "change_requests": "change_request"
}

# 📩 Headers for API Requests
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def get_group_sysid(group_name):
    """Retrieve sys_id for a given assignment group"""
    try:
        url = f"{BASE_URL}sys_user_group?sysparm_query=name={group_name}&sysparm_limit=1"
        response = requests.get(url, auth=(USERNAME, PASSWORD), headers=HEADERS)

        if response.status_code == 200:
            result = response.json().get("result", [])
            if result:
                sys_id = result[0]["sys_id"]
                print(f"✅ Group Found: {group_name} -> sys_id: {sys_id}")
                return sys_id

        print(f"❌ No sys_id found for group: {group_name}")
        return None
    except Exception as e:
        print(f"🚨 Error retrieving group sys_id: {str(e)}")
        return None

def fetch_servicenow_data(endpoint, group_name, state_filter, state_field="state"):
    """Fetch filtered ServiceNow data based on assignment group and state"""
    sys_id = get_group_sysid(group_name)
    if not sys_id:
        return []

    # 🔥 Use `task_state` for `sc_task`
    if endpoint == "sc_task":
        state_field = "task_state"

    query = f"assignment_group={sys_id}^{state_field}IN{','.join(map(str, state_filter))}"
    url = f"{BASE_URL}{endpoint}?sysparm_query={query}&sysparm_fields=number&sysparm_limit=1000"

    print(f"🔍 Fetching data from: {url}")  # Debugging line

    try:
        response = requests.get(url, auth=(USERNAME, PASSWORD), headers=HEADERS)

        if response.status_code == 200:
            data = response.json().get("result", [])
            print(f"✅ {len(data)} records found for {endpoint}")

            # Extract only "number" field
            extracted_numbers = [{"number": item["number"]} for item in data if "number" in item]
            return extracted_numbers

        print(f"❌ Error {response.status_code}: {response.text}")
        return []
    except Exception as e:
        print(f"🚨 Request failed: {str(e)}")
        return []

def export_servicenow_data():
    """Fetch and export only 'number' field for incidents, service requests, and change requests"""
    all_data = {
        "Incidents": fetch_servicenow_data(ENDPOINTS["incidents"], GROUPS["incidents"], [1, 2, 3], "incident_state"),
        "Service_Requests": fetch_servicenow_data(ENDPOINTS["service_requests"], GROUPS["service_requests"], [1, 2, 3, 4, 5], "task_state"),
        "Change_Requests": fetch_servicenow_data(ENDPOINTS["change_requests"], GROUPS["change_requests"], [1, 2, 3, 4, 5], "task_state")
    }

    # Convert to DataFrame for better export formatting
    for category, records in all_data.items():
        if records:
            df = pd.DataFrame(records)
            df.to_csv(f"{category}.csv", index=False)
            print(f"📂 {category} exported successfully: {category}.csv")
        else:
            print(f"⚠️ No records found for {category}")

if __name__ == "__main__":
    export_servicenow_data()
