import csv
import os
import main
import smtplib
from email.message import EmailMessage
import datetime


def check_file_exists(self, file_name):
    if os.path.exists(file_name):
        return True
    else:
        return False


def create_file(self, file_name):
    with open(file_name, 'w') as f:
        print("File Created")
        writer = csv.writer(f)
        writer.writerow(['Name', 'Age'])


def append_to_file(self, file_name, name, age):
    with open(file_name, 'a') as f:
        print("File appended.")
        writer = csv.writer(f)
        writer.writerow([name, age])


def file_handler(self, name, age):
    file_name = 'patient_' + name + '.csv'
    if self.check_file_exists(file_name):
        self.append_to_file(file_name, name, age)
    else:
        self.create_file(file_name)
        self.append_to_file(file_name, name, age)


def add_pain_report(self, name, age, level, confidence):
    print("(Debug) Name: " + name + " Age: " + str(age) + " Level: " + str(level) + " Confidence: " + str(confidence))
    file_name = 'patient_' + name + '.csv'
    with open(file_name, 'a') as f:
        print("File Updated")
        writer = csv.writer(f)
        writer.writerow(['Pain', name, age, level, confidence])


def add_drowsiness_report(self, name, age, level, confidence):
    file_name = 'patient_' + name + '.csv'
    with open(file_name, 'a') as f:
        print("File Updated")
        writer = csv.writer(f)
        writer.writerow(['Drowsiness', name, age, level, confidence])


def add_mental_health_report(self, name, age, mental_health_level, confidence):
    file_name = 'patient_' + name + '.csv'
    with open(file_name, 'a') as f:
        print("File Updated")
        writer = csv.writer(f)
        writer.writerow(['Mental Health', name, age, mental_health_level, confidence])


# This will likely never be used. It is here just in case.
def add_suicidal_thoughts_report(self, name="mental_emergency", age=-1, mental_health_level=0, confidence=100):
    file_name = 'patient_' + name + '.csv'
    with open(file_name, 'a') as f:
        print("File Updated")
        writer = csv.writer(f)
        writer.writerow(['Suicidal Thoughts', name, age, mental_health_level, confidence])


# Send email with patient_{name}.csv file attached
def send_email(self, name, email_from, password, email_to):
    file_name = 'patient_' + name + '.csv'
    try:
        msg = EmailMessage()
        msg['Subject'] = 'Patient Report'
        msg['From'] = email_from
        msg['To'] = email_to
        msg.set_content('Patient Report\n\nSee attached file for details.\nDate: ' + str(datetime.datetime.now()))
        with open(file_name, 'rb') as f:
            file_data = f.read()
            file_name = f.name
        msg.add_attachment(file_data, maintype='text', subtype='csv', filename=file_name)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_from, 'password')
            smtp.send_message(msg)
            print("Email Sent")
    except Exception as e:
        print(e)
        main.EmailFailedPopup().open()
