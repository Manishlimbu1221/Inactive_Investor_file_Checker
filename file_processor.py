import os
import pyodbc
from datetime import datetime
import sys
import pandas as pd
import re


def split_portfolio_name(filenames):
    investors = []

    for file in filenames:
        rest = file.rsplit('_', -1)
        investors.append(rest[3])

    print(f'Retrieved {len(investors)} contact numbers from the file names...')
    return investors


class FileProcessor:
    def __init__(self, directory, connection_string):
        self.directory = directory
        self.connection_string = connection_string
        self.connection = None
        # Get the directory of the executable or script
        if hasattr(sys, "_MEIPASS"):
            self.script_directory = os.path.dirname(sys.executable)
        else:
            self.script_directory = os.path.dirname(os.path.abspath(__file__))

    def connect_to_db(self):
        """Establish database connection"""
        self.connection = pyodbc.connect(self.connection_string)

    def get_filenames(self):
        """Retreive filenames from the directory"""
        # Get all the filenames from the directory and store them in a list
        filenames = os.listdir(self.directory)

        print('Getting File Names from the directory...')
        # Filter the list to exclude directories, if needed
        return [f for f in filenames if os.path.isfile(os.path.join(self.directory, f))]

    def check_investors_in_db(self, investors):
        """Check if Investor is active in DB"""
        # Join the values into a string that SQL understands (comma-separated and quoted)
        investors_sql = ",".join(f"'{value}'" for value in investors)
        print('Checking the Contact numbers against the database to see if they are active...')
        sql_query = f"select oct_conno, CASE WHEN statecode = '0' then'yes' WHEN statecode = '1' then 'no' END, CASE WHEN statuscode = '2' then 'Inactive' END from ods_dynamics365.contact where oct_conno in ({investors_sql}) AND (statecode = '1' OR statuscode = '801800002')"

        cursor = self.connection.cursor()
        cursor.execute(sql_query)

        # Fetch the rows from sql and stores it into a dictionary
        inactive_inv = []
        for row in cursor.fetchall():
            row_dict = {
                'contact_number': row[0],  # 'string1'
                'IsActive': row[1],  # int
                'Status': row[2],  # 'string2'
            }
            inactive_inv.append(row_dict)

        # Gets just the list of inactive invs from the dictionary
        return inactive_inv

    def output_inactive_contacts(self, contact):
        """Outputs contacts to a csv file"""
        # Loops through dictionary and uses dictionary comprehension to add the filenames into the dictionary
        for con in contact:
            con['files'] = ', '.join(
                filename for filename in os.listdir(self.directory)
                if re.search(r'(?<!\d)' + re.escape(con['contact_number']) + r'(?!\d)', filename)
            )

        # Generate a timestamp for the filename in the format YYYY-MM-DD_HH-MM-SS
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Write the matching files to the csv output file
        if contact:
            df = pd.DataFrame(contact)
            csv_file = os.path.join(self.script_directory, f"contact_files_{timestamp}.csv")
            df.to_csv(csv_file, index=False)

            print(f"Matching file names have been saved to {csv_file}")
        else:
            print(f"All contacts within the specified directory is active")

    def process_files(self):
        """Main function to process files"""
        filenames = self.get_filenames()
        investors = split_portfolio_name(filenames)
        inactive_con = self.check_investors_in_db(investors)
        self.output_inactive_contacts(inactive_con)

    def close_connection(self):
        """Closes DB connection"""
        if self.connection:
            self.connection.close()
            print("Database connection Closed.")
