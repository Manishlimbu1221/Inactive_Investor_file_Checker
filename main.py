import xml.etree.ElementTree as ET
import getpass
from file_processor import FileProcessor
import pyodbc
import sys

# ASCII Art for decoration - Remove if it causes issues
ascii_art = r"""
                            .---.         ,,
                 ,,        /     \       ;,,'
                ;, ;      (  o  o )      ; ;
                  ;,';,,,  \  \/ /      ,; ;
               ,,,  ;,,,,;;,`   '-,;'''',,,'
              ;,, ;,, ,,,,   ,;  ,,,'';;,,;''';
                 ;,,,;    ~~'  '';,,''',,;''''  
                                    '''
"""
ascii_title = r"""              +-+-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+
              |i|n|a|c|t|i|v|e| |c|h|e|c|k|e|r|
              +-+-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+
"""

print(ascii_art)
print(ascii_title)

if __name__ == "__main__":
    while True:
        try:
            # Parse the XML file
            tree = ET.parse('settings.xml')
            root = tree.getroot()

            # Asks for SQL username and password and tests the connection
            sql_username = input('Enter SQL Username: ').strip()
            sql_password = getpass.getpass('Enter SQL Password: ').strip()
            sql_server = root.find('sql_server').text
            sql_database = root.find('sql_database').text
            sql_driver = root.find('sql_driver').text

            # Sets the connection string for SQL db access
            connection_string = f'DRIVER={sql_driver};Server={sql_server};Database={sql_database};UID={sql_username};PWD={sql_password};Authentication=ActiveDirectoryPassword;Encrypt=yes;TrustServerCertificate=no;'

            print('Checking Credentials...')
            test_connection = pyodbc.connect(connection_string)
            test_connection.close()
            print('Credentails accepted, connected to DB...')

            # Created a loop, so you don't have to enter sql username and password each time can just change the folder names
            re_run = True

            while re_run:
                try:
                    print(
                        '=======================================================================================================================')
                    file_path = input('File Path to Check the files: ').strip()

                    # Runs the process to extract inactive CONS based on the valuation files in the directory specified
                    processor = FileProcessor(file_path, connection_string)
                    processor.connect_to_db()
                    processor.process_files()
                    processor.close_connection()

                    _exit = input(
                        '=======================================================================================================================\n'
                        'Script has been successfully run.\n'
                        'Enter (y) to run again - # Note please modify the folder names before running again, if running for multiple folders.\n'
                        'Enter (n) to Exit.\n'
                        'Please enter your options (y/n): ').lower().strip()
                    if _exit.lower() == 'y':
                        print('Please change the folder if required')
                        print(
                            '=======================================================================================================================')
                    else:
                        print('Exiting Script')
                        re_run = False

                except FileNotFoundError as e:
                    print(f"Error: {e}")
                    print("Please provide a valid directory.")
                except Exception as e:
                    print(f"An error occurred: {e}")
                    print("Please ensure the right folder is selected.")

            if not re_run:
                sys.exit()

        except Exception as e:
            print(f"Database connection error: {e}")
            print("Please check your SQL credentials and try again.\n")


