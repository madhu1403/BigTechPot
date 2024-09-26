import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv
from faker import Faker
import requests

# SMTP Configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587
username = 'sharadajaganjsm@gmail.com'  # Your Gmail address
password = 'yoht tyth ktqd xese'  # Your Gmail App Password

# WordPress REST API URL
wp_site_url = 'http://localhost/wordpress'
rest_api_url = f'{wp_site_url}/wp-json/wp/v2/users'

# Create a Faker instance for generating dummy data
fake = Faker()

# Function to send email
def send_email(to_email, to_name):
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = to_email
    msg['Subject'] = 'Test Email Subject'
    
    # HTML content
    body = f'This is a test email sent to <b>{to_name}</b>!'
    msg.attach(MIMEText(body, 'html'))
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(username, password)
            server.sendmail(username, to_email, msg.as_string())
            print(f"Message sent to {to_name} <{to_email}>")
    except Exception as e:
        print(f"Failed to send email to {to_name} <{to_email}>: {str(e)}")

# Function to generate dummy data and save to CSV
def create_dummy_csv(csv_file, num_entries=10):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Email'])  # CSV Header
        # Explicitly include the email madhurya050@gmail.com
        writer.writerow(['Madhurya', 'madhurya050@gmail.com'])
        for _ in range(num_entries - 1):  # Reduce by 1 since we've added 1 manually
            name = fake.name()
            email = fake.email()
            writer.writerow([name, email])
    print(f"Dummy data saved to {csv_file}")

# Function to fetch users from WordPress REST API
def fetch_users_from_wp_api():
    try:
        response = requests.get(rest_api_url)
        response.raise_for_status()  # Raise an error for bad responses
        users = response.json()
        return users
    except requests.exceptions.RequestException as e:
        print(f"Error fetching users from WordPress: {str(e)}")
        return []

# Function to send emails from CSV
def send_emails_from_csv(csv_file):
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                name, email = row[0], row[1]
                send_email(email, name)
    except Exception as e:
        print(f"Error reading the CSV file: {str(e)}")

# Main function to run the workflow
def main():
    csv_file = 'emails.csv'
    
    # Create dummy data for testing
    create_dummy_csv(csv_file, num_entries=10)
    
    # Optionally fetch users from WordPress and print their details
    users = fetch_users_from_wp_api()
    if users:
        print("Fetched users from WordPress:")
        for user in users:
            print(f"User: {user.get('name')}, Email: {user.get('email')}")

    # Send emails to users in CSV
    send_emails_from_csv(csv_file)

# Run the script
if __name__ == "__main__":
    main()
