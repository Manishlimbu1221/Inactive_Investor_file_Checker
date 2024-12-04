# Inactive_Investor_file_Checker
InactiveChecker is a Python-based application designed to process files and identify inactive investors by cross-referencing with an SQL database. The results are saved to a CSV file for further analysis.

## Features

- **Database Connection Validation**: Verifies SQL server credentials before proceeding.
- **File Processing**: Processes files from a user-specified directory.
- **Database Querying**: Identifies inactive investors based on specified criteria.
- **CSV Output**: Outputs the results of inactive investors and their associated files to a CSV file with a timestamped name.
- **Retry Mechanism**: Allows repeated execution for different file paths without restarting the application.

---

## Installation

### Prerequisites

- Python 3.7 or higher
- Required Python packages (install via `pip`):
  - `pyodbc`
  - `pandas`
  - `re`
  - `pyinstaller

 - Configure the settings.xml file:
 - Update the following fields with your SQL server details:
   `<sql_server>your_sql_server</sql_server>`
    `<sql_database>your_database</sql_database>`
    `<sql_driver>{ODBC Driver 17 for SQL Server}</sql_driver>`
- Ensure you have the necessary permissions to connect to the SQL server.
## Creating a Standalone Executable with PyInstaller
1. Install pyinstaller:
   `pip install pyinstaller`
2. Generate an executable:
  `pyinstaller --onefile --noconsole main.py`

---

## Usage
1. Run the application:
   `python main.py`
2. Follow the prompts to:
    - Enter SQL server credentials.
    - Specify the file path for processing.
    - Re-run the script with different paths if needed.
3. The results will be saved as a timestamped CSV file in the script's directory.

---

## Contact
For questions or support, please reach out via my [GitHub Profile](https://github.com/Manishlimbu1221).
