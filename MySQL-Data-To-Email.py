import mysql.connector
import pandas as pd
import os
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

# Database connection details
db_config = {
    'host': 'xx.xx.xx.xx',  # Replace with your MySQL host
    'user': 'xxxxxxxx',  # Replace with your MySQL username
    'password': 'xxxxxxxx',  # Replace with your MySQL password
    'database': 'xxxxxxxx'  # Replace with your database name
}

# List of table names to query
table_DN = [
    "Table1", "Table2", "Table3", "Table4", "Table5", 
    "Table6", "Table7", "Table8", "Table9", "Table10", 
    "Table11", "Table12"
]

# Email configuration
email_sender = "xxxxxxx@xxxxxxxx.com" # Replace with your Sender
email_password = "xxxxxxxx" # Replace with your Password
email_receiver = "xxxxxxxx@xxxxxxxxx.com" # Replace with your Receiver
email_cc = ["xxxxxxxx@xxxxxxxxx.com"]  # List of CC recipients
email_subject = f"SQL DATA REPORT - {datetime.now().strftime('%m/%d/%Y')}" # Replace with your Email subject
email_body = """\
Hello Everyone,

Please find attached files.

Thank you.


This is an automated email process by Debasis Nandi. If you have any inquiries, please contact.
"""

# Calculate today's date in the format MMDD
today_folder = datetime.now().strftime('%m%d')
today_date = datetime.now().strftime('%Y%m%d')

try:
    # Connect to the database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Directory to save the CSV files
    output_dir = os.path.join('D:\\xxxxxxxx\\xxxxxxxx\\xxxxxxxx\\xxxxxxxx\\', today_folder) # Replace with your save file path
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # List to keep track of the file paths
    file_paths = []

    # Iterate through each table and run the query
    for table_name in table_DN:
        # SQL query template with dynamic table name
        query_DN = f"""
        SELECT xxxxxxxx
        FROM xxxxxxxx.{table_name}
        INNER JOIN xxxxxxxx ON ({table_name}.xxxxxxxx = xxxxxxxx)
        INNER JOIN xxxxxxxx ON (xxxxxxxx = xxxxxxxx);
        """
        
        # Execute the query and fetch data into a DataFrame
        cursor.execute(query_DN)
        df = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
        
        # File path for the current table's data with prefix, table name, and today's date
        output_file = os.path.join(output_dir, f"xxxxxxxx_{table_name}_{today_date}.csv") # Replace with your files name
        
        # Save the DataFrame to a CSV file
        df.to_csv(output_file, index=False)
        
        # Add the file path to the list
        file_paths.append(output_file)
        
        print(f"Data for table '{table_name}' has been successfully exported to {output_file}")

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Email the files
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Cc'] = ", ".join(email_cc)
    msg['Subject'] = email_subject
    msg.attach(MIMEText(email_body))

    for file_path in file_paths:
        with open(file_path, 'rb') as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
            msg.attach(part)

    # Combine TO and CC for the final recipient list
    final_recipients = [email_receiver] + email_cc

    # Connect to the email server and send the email
    with smtplib.SMTP('smtp.office365.com', 587) as server:
        server.starttls()
        server.login(email_sender, email_password)
        server.sendmail(email_sender, final_recipients, msg.as_string())

    print("Email with attached files has been sent successfully.")

except mysql.connector.Error as err:
    print(f"Database error: {err}")

except Exception as e:
    print(f"An error occurred: {e}")
