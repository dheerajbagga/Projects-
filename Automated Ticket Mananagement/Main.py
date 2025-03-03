import requests
import json
import pandas as pd
import logging
import configparser
from itertools import cycle
from transformers import pipeline  # Import the pipeline

# --- Configuration Loading ---
config = configparser.ConfigParser()
config.read("config.ini")

# ServiceNow Credentials
INSTANCE = config.get("SERVICENOW", "INSTANCE")
USERNAME = config.get("SERVICENOW", "USERNAME")
PASSWORD = config.get("SERVICENOW", "PASSWORD")

# Assignment Groups
GROUPS = {
    "incidents": config.get("GROUPS", "INCIDENTS"),
    "service_requests": config.get("GROUPS", "SERVICE_REQUESTS"),
    "change_requests": config.get("GROUPS", "CHANGE_REQUESTS"),
}

# CSV Paths
SHIFT_ROSTER_PATH = config.get("CSV_PATHS", "SHIFT_ROSTER")

# Logging
LOG_FILE = config.get("LOGGING", "LOG_FILE")
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ServiceNow API Base URL
BASE_URL = f"https://{INSTANCE}/api/now/table/"

# API Endpoints
ENDPOINTS = {
    "incidents": "incident",
    "service_requests": "sc_task",
    "change_requests": "change_request",
}

# Headers for API Requests
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

# --- Hugging Face Model ---
# Load the pre-downloaded model
try:
    resolution_generator = pipeline("text-generation", model="gpt2")  # You can use any other model as per your requirement
    logging.info("✅ Hugging Face model loaded successfully.")
except Exception as e:
    logging.error(f"🚨 Error loading Hugging Face model: {str(e)}")
    resolution_generator = None  # Set to None if loading fails


# --- Helper Functions ---

def get_group_sysid(group_name):
    """Retrieve sys_id for a given assignment group"""
    try:
        url = f"{BASE_URL}sys_user_group?sysparm_query=name={group_name}&sysparm_limit=1"
        logging.info(f"🔍 Attempting to get sys_id for group: {group_name} - URL: {url}")
        response = requests.get(url, auth=(USERNAME, PASSWORD), headers=HEADERS)

        logging.debug(f"🔄 Response status code: {response.status_code}")
        logging.debug(f"🔄 Response body: {response.text}")

        if response.status_code == 200:
            try:
                result = response.json().get("result", [])
                if result:
                    sys_id = result[0]["sys_id"]
                    logging.info(f"✅ Group Found: {group_name} -> sys_id: {sys_id}")
                    return sys_id
                else:
                    logging.warning(f"❌ No sys_id found for group: {group_name} (empty result)")
                    return None

            except json.JSONDecodeError as e:
                logging.error(f"🚨 Error decoding JSON response for group {group_name}: {e}")
                return None
        elif response.status_code == 401:
            logging.error(f"🚨 Unauthorized access (401) when trying to get group {group_name} - check your credentials.")
            return None
        else:
            logging.error(f"❌ Error retrieving group sys_id for {group_name}: Status code: {response.status_code}, Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"🚨 Network-related error when retrieving group sys_id for {group_name}: {e}")
        return None
    except Exception as e:
        logging.error(f"🚨 Error retrieving group sys_id: {str(e)}")
        return None


def fetch_servicenow_data(endpoint, group_name, state_filter, state_field="state", fields="number,short_description"):
    """Fetch filtered ServiceNow data based on assignment group and state"""
    sys_id = get_group_sysid(group_name)
    if not sys_id:
        return []

    if endpoint == "sc_task":
        state_field = "task_state"

    query = f"assignment_group={sys_id}^{state_field}IN{','.join(map(str, state_filter))}"
    url = f"{BASE_URL}{endpoint}?sysparm_query={query}&sysparm_fields={fields}&sysparm_limit=1000"

    logging.info(f"🔍 Fetching data from: {url}")

    try:
        response = requests.get(url, auth=(USERNAME, PASSWORD), headers=HEADERS)
        logging.debug(f"🔄 Response status code: {response.status_code}")
        logging.debug(f"🔄 Response body: {response.text}")

        if response.status_code == 200:
            data = response.json().get("result", [])
            logging.info(f"✅ {len(data)} records found for {endpoint}")
            return data
        elif response.status_code == 401:
            logging.error(f"🚨 Unauthorized access (401) when trying to get tickets - check your credentials.")
            return []
        else:
            logging.error(f"❌ Error {response.status_code}: {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        logging.error(f"🚨 Network-related error: {str(e)}")
        return []
    except Exception as e:
        logging.error(f"🚨 Request failed: {str(e)}")
        return []


def update_servicenow_record(endpoint, sys_id, update_data):
    """Update a ServiceNow record with the given data"""
    url = f"{BASE_URL}{endpoint}/{sys_id}"
    try:
        response = requests.put(url, auth=(USERNAME, PASSWORD), headers=HEADERS, data=json.dumps(update_data))
        if response.status_code == 200:
            logging.info(f"✅ Record {sys_id} updated successfully.")
            return True
        elif response.status_code == 401:
            logging.error(f"🚨 Unauthorized access (401) when trying to update ticket {sys_id} - check your credentials.")
            return False
        else:
            logging.error(f"❌ Error updating record {sys_id}: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f"🚨 Network-related error while updating ticket {sys_id} : {str(e)}")
        return False
    except Exception as e:
        logging.error(f"🚨 Error updating record {sys_id}: {str(e)}")
        return False


def get_available_agents(csv_file):
    """Load available agents from the CSV, excluding those 'On_Leave'"""
    try:
        df = pd.read_csv(csv_file)
        available_agents = df[df["Status"] != "On_Leave"]["Agent Name"].tolist()
        logging.info(f"✅ Available agents loaded: {available_agents}")
        return available_agents
    except FileNotFoundError:
        logging.error(f"🚨 Error: Shift roster CSV file not found at {csv_file}")
        return []
    except Exception as e:
        logging.error(f"🚨 Error loading agent data: {str(e)}")
        return []


def assign_tickets(tickets, agents):
    """Distribute tickets evenly among agents"""
    assignments = {}
    if not agents:
        logging.warning("⚠️ No agents available for ticket assignment.")
        return assignments

    agent_cycle = cycle(agents)
    for ticket in tickets:
        agent = next(agent_cycle)
        if agent not in assignments:
            assignments[agent] = []
        assignments[agent].append(ticket)
    logging.info(f"✅ Tickets assigned to agents: {assignments}")
    return assignments


def generate_resolution(description):
    """Generate a resolution using the Hugging Face model."""
    if resolution_generator is None:
        logging.warning("⚠️ Hugging Face model is not available. Skipping resolution generation.")
        return None
    try:
        logging.info(f"🤖 Generating resolution for description: {description[:50]}...")
        resolution = resolution_generator(description, max_length=50, num_return_sequences=1)[0]["generated_text"]
        logging.info(f"✅ Generated resolution: {resolution}")
        return resolution
    except Exception as e:
        logging.error(f"🚨 Error generating resolution: {str(e)}")
        return None


def main():
    """Main function to orchestrate the process."""

    # 1. Extract Available Agents
    available_agents = get_available_agents(SHIFT_ROSTER_PATH)

    # 2. Retrieve Tickets from ServiceNow
    ticket_data = {}
    for ticket_type, group_name in GROUPS.items():
        state_filter = [1, 2, 3]  # New, in progress , on hold
        if ticket_type == 'incidents':
            state_field = "incident_state"
        else:
            state_field = "task_state"
        tickets = fetch_servicenow_data(ENDPOINTS[ticket_type], group_name, state_filter, state_field,
                                        fields='number,short_description,sys_id,description')

        if tickets:
            ticket_data[ticket_type] = tickets

    # Log fetched Data
    logging.info(f"📋 Fetched Ticket Data: {ticket_data}")

    # 3. Assign Tickets Equally
    all_tickets = []
    for ticket_list in ticket_data.values():
        all_tickets.extend(ticket_list)

    assigned_tickets = assign_tickets(all_tickets, available_agents)

    # log assigned data
    logging.info(f"📋 Assigned Ticket Data: {assigned_tickets}")

    # 4 & 5. Generate and Update Resolutions
    for agent, tickets in assigned_tickets.items():
        logging.info(f"👩‍💻 Processing tickets for agent: {agent}")
        for ticket in tickets:
            try:
                ticket_type = [key for key, value in ticket_data.items() if ticket in value][0]
                logging.info(f"ℹ️ Processing ticket type: {ticket_type}")

                if "description" in ticket and ticket['description']:
                    resolution = generate_resolution(ticket["description"])

                    if resolution:
                        if ticket_type in ["incidents", "service_requests"]:
                            update_data = {"work_notes": resolution}  # Use work_notes for resolution
                            update_result = update_servicenow_record(ENDPOINTS[ticket_type], ticket["sys_id"], update_data)

                            if update_result:
                                logging.info(
                                    f"✅ Resolution updated for ticket {ticket['number']} of {ticket_type} assigned to agent {agent}")
                            else:
                                logging.error(
                                    f"❌ Failed to update resolution for ticket {ticket['number']} of {ticket_type} assigned to agent {agent}")
                        else:
                            logging.info(f"ℹ️ Skipping resolution update for change request {ticket['number']}.")
                else:
                    logging.warning(f"⚠️ No description found for ticket {ticket['number']}")
            except Exception as e:
                logging.error(
                    f"🚨 An unexpected error occurred while processing ticket {ticket.get('number', 'Unknown')}: {str(e)}")


if __name__ == "__main__":
    main()
