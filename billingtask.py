from datetime import date
import csv
import datetime
import os.path
import smtplib
from tempfile import NamedTemporaryFile
import shutil
from email.message import EmailMessage
import ssl
from email_validator import validate_email, EmailNotValidError
import datetime

print("welcome to billing management system")


def choose_enquiry():
    choose_items = int(
        input(
            "Enter your items:\n1:Customer\n2:Subscription\n3:send mail\n4:Exit:\n"
        ))

    data_enquiry = {
        1: sub_menu_customer,
        2: sub_menu_subscription,
        3: send_email,
        4: exit
    }
    if choose_items not in data_enquiry:
        print("invalid number")
        return choose_enquiry()

    data_enquiry.get(choose_items)()


def sub_menu_customer():
    choose_customer = int(
        input(
            "\n 1:create customer \n 2:retrieve \n 3:delete \n 4:list \n 5:update\n 6:Exit \n"
        ))
    data_sub_customer = {
        1: add_customer,
        2: retrieve_customer,
        3: delete_customer,
        4: list_customer,
        5: update_customer,
        6: exit
    }
    if choose_customer not in data_sub_customer:
        print("invalid nuber")
        return sub_menu_customer()
    data_sub_customer.get(choose_customer)()

    return choose_enquiry()


def add_customer():
    name = input("Enter the name:")
    file_exists = os.path.isfile('customer.csv')
    with open('customer.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for data in reader:
            if data["Name"] == name:
                print("name already exists!!")
                return add_customer()

    email = input("Enter email:")
    check_valid_email(email)
    phone = input("Enter the number:")
    status = input("Enter Status active/inactive:")
    create_at = date.today()

    with open('customer.csv', 'a') as csvfile:
        fields = ['Name', 'Email', 'Phone', 'Status', 'Date']
        writer = csv.DictWriter(csvfile,
                                delimiter=',',
                                lineterminator='\n',
                                fieldnames=fields)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'Name': name,
            'Email': email,
            'Phone': phone,
            'Status': status,
            'Date': create_at
        })


def retrieve_customer():
    search_name = input("Enter the name:")
    with open('customer.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for data in reader:
            if data["Name"] == search_name:
                print(data)


def list_customer():
    detail_customer = int(input("1:All\n2:active\n3:inactive\nexit\n"))
    data_dic = {
        1: all_customer_list,
        2: active_customer,
        3: inactive_customer,
        4: exit
    }
    data_dic.get(detail_customer)()


def delete_customer():
    lines = []
    lines1 = []
    customerName = input("Please enter a customerName to be deleted.")
    with open('customer.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            lines.append(row)
            for field in row:
                if field == customerName:
                    lines.remove(row)
    with open('customer.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)

    with open('subscription.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            lines1.append(row)
            for field in row:
                if field == customerName:
                    lines1.remove(row)
    with open('subscription.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines1)


def update_customer():
    search = input("Enter the customer Name")
    filename = 'customer.csv'
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    fields = ['Name', 'Email', 'Phone', 'Status', 'Date']
    with open(filename, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row['Name'] == search:
                print('updating row', row['Name'])
                row['Name'], row['Email'], row['Phone'], row['Status'], row[
                    'Date'] = input("Name"), input("Email"), input(
                        "Phone"), input("Status"), date.today()
            row = {
                'Name': row['Name'],
                'Email': row['Email'],
                'Phone': row['Phone'],
                'Status': row['Status'],
                'Date': row['Date']
            }
            writer.writerow(row)
    shutil.move(tempfile.name, filename)


def all_customer_list():
    with open('customer.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for data in reader:
            print(data)


def active_customer():
    with open('customer.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for data in reader:
            if data['Status'] == 'active':
                print(data)


def inactive_customer():

    with open('customer.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for data in reader:
            if data['Status'] == 'inactive':
                print(data)


def check_valid_email(email):
    try:

        valid = validate_email(email)
        email = valid["email"]
    except EmailNotValidError as e:
        print(str(e))
        return add_customer()


# subscription
def sub_menu_subscription():
    choose_customer = int(
        input(
            "\n 1:create subscription \n 2:retrieve \n 3:delete \n 4:list \n 5:update\n 6:Exit \n"
        ))
    data = {
        1: add_subscription,
        2: retrieve_customer,
        3: delete_subscription,
        4: list_subscription,
        5: update_subscription
    }
    data.get(choose_customer)()


def add_subscription():
    customer_name = input('please enter the valid customer name\n')
    with open('customer.csv') as read_customer:
        content = csv.DictReader(read_customer)

        for particular_data in content:
            if customer_name == particular_data['Name']:
                name = particular_data['Name']
                status = input("Enter Status: \n1:paid\n2:unpaid:\n")
                email = particular_data['Email']
                from_date = date.today()

                if status == "paid":
                    subscription_time = input("\n1month\n3month\n6month")
                    if subscription_time == "1month":
                        amount = 1000
                        to_date = from_date + datetime.timedelta(days=30)

                    elif subscription_time == '3month':
                        amount = 2500
                        # presentdate = date.today()
                        to_date = from_date + datetime.timedelta(days=90)
                    elif subscription_time == '6month':
                        amount = 5000
                        to_date = from_date + datetime.timedelta(days=180)
                else:
                    amount = 0
                    to_date = 0

                file_exists = os.path.isfile('subscription.csv')

                with open('subscription.csv', 'a') as csvfile:
                    fields = [
                        'Name', 'Amount', 'Status', 'Email', 'from_date',
                        'to_date'
                    ]
                    writer = csv.DictWriter(csvfile,
                                            delimiter=',',
                                            lineterminator='\n',
                                            fieldnames=fields)

                    if not file_exists:
                        writer.writeheader()

                    writer.writerow({
                        'Name': name,
                        'Amount': amount,
                        'Status': status,
                        'Email': email,
                        'from_date': from_date,
                        'to_date': to_date
                    })
        print("create customer id")


def list_subscription():
    detail_customer = int(input("1:All\n2:paid\n3:unpaid\n"))
    data_detail = {
        1: all_subscription_list,
        2: paid_subscription,
        3: unpaid_subscription,
        4: exit
    }
    data_detail.get(detail_customer)()


def all_subscription_list():
    with open('subscription.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for data in reader:
            print(data)


def retrieve_subscription():
    search_name = input("Enter the name:")
    with open('subscription.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for data in reader:
            # print(data)
            if data["Name"] == search_name:
                print(data)


def delete_subscription():
    lines1 = []
    customerName = input("Please enter a customerName to be deleted.")
    with open('subscription.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            lines1.append(row)
            for field in row:
                if field == customerName:
                    lines1.remove(row)
    with open('subscription.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines1)

    return sub_menu_customer()


def update_subscription():
    search = input("Enter the subscription Name")
    filename = 'subscription.csv'
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    fields = ['Name', 'Amount', 'Status', 'Email', 'from_date', 'to_date']
    with open(filename, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row['Name'] == search:
                print('updating row', row['Name'])
                row['Name'], row['Amount'], row['Status'], row['Email'], row[
                    'from_date'], row['to_date'] = input("Name"), input(
                        "Amount"), input("Status"), input(
                            "Email:"), date.today(), input("to date")
            row = {
                'Name': row['Name'],
                'Amount': row['Amount'],
                'Status': row['Status'],
                'Email': row['Email'],
                'from_date': row['from_date'],
                'to_date': row['to_date'],
            }
            writer.writerow(row)
    shutil.move(tempfile.name, filename)


def send_email():
    from datetime import datetime

    with open('subscription.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Status'] == 'paid':
                d1 = row['from_date']
                d2 = row['to_date']
                startdate = datetime.strptime(d1, '%Y-%m-%d').date()
                enddate = datetime.strptime(d2, '%Y-%m-%d').date()
                result = enddate - startdate
                subtractdate = result.days
                print(subtractdate)
                if subtractdate <= abs(5) and row['Status'] == 'paid':
                    print("hello")
                    email_sender = 'mission.sharma101@gmail.com'
                    email_password = 'zapgldcllkdallwb'
                    email_receiver = row["Email"]
                    subject = "Subscription time is going to timeout"
                    body = "Your subscripton is running out.\nThank You!!!"

                    em = EmailMessage()
                    em['from'] = email_sender
                    em['to'] = email_receiver
                    em['subject'] = subject
                    em.set_content(body)
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL('smtp.gmail.com',
                                          465,
                                          context=context) as smtp:
                        smtp.login(email_sender, email_password)
                        smtp.sendmail(email_sender, email_receiver,
                                      em.as_string())


def paid_subscription():
    with open('subscription.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for data in reader:
            if data['Status'] == 'paid':
                print(data)


def unpaid_subscription():
    with open('subscription.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for data in reader:
            if data['Status'] == 'unpaid':
                print(data)


choose_enquiry()