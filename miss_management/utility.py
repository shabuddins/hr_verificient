import csv
import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def write_to_csv(filename, data, type='a'):  # writes the given data to the csv filename provided
    with open(filename, type) as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(data)
    csv_file.close()


def verify_user_using_csv_data(file_name, user_name, password):
    with open(os.path.join(BASE_DIR, file_name), 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row[1] == user_name and row[2] == password:
                csv_file.close()
                return True, row[3]

    csv_file.close()
    return False, None


def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def is_integer(num):
    try:
        int(num)
        return True
    except:
        return False

