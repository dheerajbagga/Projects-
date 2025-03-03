# Automated Ticket Management System

This project is an automated system designed to manage tickets within a ServiceNow instance. It automatically retrieves new, in progress, and on hold tickets (incidents, service requests, and change requests), assigns them to available agents, and attempts to generate initial resolutions for incidents and service requests using a Hugging Face language model.

## Features

*   **ServiceNow Integration:** Fetches tickets (incidents, service requests, change requests) from a ServiceNow instance using the ServiceNow API.
*   **Ticket Filtering:** Filters tickets based on their assignment group and state (New, In Progress, On Hold).
*   **Agent Assignment:** Distributes tickets evenly among available agents loaded from a CSV file.
*   **AI-Powered Resolution Generation:** Utilizes a Hugging Face language model (specifically, `gpt2` by default) to generate potential resolutions for incidents and service requests based on their descriptions.
*   **Automatic Resolution Update:** Automatically updates the `work_notes` field of incidents and service requests in ServiceNow with the generated resolution.
*   **Logging:** Implements comprehensive logging to track the system's actions and any errors encountered.
* **Configurable**: Uses a config.ini file to setup, servicenow credentials, file paths and other relevant information.

## Getting Started

### Prerequisites

Before running the system, ensure you have the following:

*   **Python 3.8+:** This project is written in Python and requires a Python 3.8 or higher environment.
*   **Python Packages:** Install the necessary Python packages using pip:
    ```bash
    pip install requests pandas configparser transformers
    ```
*   **ServiceNow Instance:** A ServiceNow instance with API access.
*   **ServiceNow Credentials:** A ServiceNow user account with the necessary permissions to access and update tickets.
*   **Hugging Face Model:**  The code downloads the `gpt2` model, but it may take a while. consider pre-downloading the model by      running `python -c "from transformers import pipeline; pipeline('text-generation', model='gpt2')"`
*   **Shift Roster CSV:** A CSV file (`shift_roster.csv` by default) containing the list of agents and their availability status. The CSV should have at least two columns:
    *   `Agent Name`: The name of the agent.
    *   `Status`: The agent's status (e.g., "Available", "On_Leave").
*   **Config file**: a file named config.ini that will store all the credentials, and paths.

### Installation and Configuration

1.  **Clone the Repository:** (If you have a repo for this project, otherwise you can skip this step)
    ```bash
    git clone [repository-url]
    cd [project-directory]
    ```

2.  **Create `config.ini`:** Create a file named `config.ini` in the same directory as `Main.py`. Populate it with the following content, replacing the placeholders with your actual data:

    ```ini
    [SERVICENOW]
    INSTANCE = your_servicenow_instance.service-now.com
    USERNAME = your_servicenow_username
    PASSWORD = your_servicenow_password

    [GROUPS]
    INCIDENTS = Your Incident Assignment Group
    SERVICE_REQUESTS = Your Service Request Assignment Group
    CHANGE_REQUESTS = Your Change Request Assignment Group

    [CSV_PATHS]
    SHIFT_ROSTER = shift_roster.csv

    [LOGGING]
    LOG_FILE = app.log
    ```
    * **[SERVICENOW]**: Replace with your own servicenow instance, username and password.
    * **[GROUPS]**: Replace with your groups names.
    * **[CSV_PATHS]**: ensure the file path is correct, modify if needed.
    * **[LOGGING]**: Change the log file name if needed.
3.  **Create `shift_roster.csv`:** Create a CSV file named `shift_roster.csv` (or whatever you specified in `config.ini`) with columns "Agent Name" and "Status." An example:

    ```csv
    Agent Name,Status
    John Doe,Available
    Jane Smith,Available
    Peter Jones,On_Leave
    ```

### Running the Project

1.  **Navigate to Project Directory:** Open a terminal or command prompt and navigate to the directory containing `Main.py`.

2.  **Run the Script:** Execute the `Main.py` script:

    ```bash
    python Main.py
    ```

    The script will:
    * load the shift roster.
    * Fetch tickets from ServiceNow.
    * Assign tickets to agents.
    * Generate resolutions.
    * Update ServiceNow records.

### Important Notes

*   **ServiceNow Permissions:** Ensure the ServiceNow user you configure in `config.ini` has the necessary permissions to:
    *   Read data from the `incident`, `sc_task`, and `change_request` tables.
    *   Update records on the `incident` and `sc_task` tables.
    * Access `sys_user_group` table
*   **Error Handling:** The script includes error handling and logging. Check the `app.log` (or the name you defined in the `config.ini` file) file for any errors or warnings.
*   **Hugging Face Model:** The code uses the `gpt2` model for resolution generation. You can change to another model inside the main.py file, in the model creation section.
*   **Change Requests**: as implemented, it will only skip resolution generation for change requests, as it is not implemented.
* **States**: the script will fetch tickets that are in new (1), in progress(2) and on hold(3) states.

## Contributing

If you wish to contribute to the project, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them.
4.  Push your changes to your fork.
5.  Submit a pull request.

## License

This project is licensed under the MIT License .

## Author

[Dheeraj Bagga] - Initial work.
