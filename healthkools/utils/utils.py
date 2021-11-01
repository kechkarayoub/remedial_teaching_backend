import datetime


def date_from_string(date_string):
    try:
        return datetime.datetime.strptime(date_string, "%d/%m/%Y")
    except:
        return None
