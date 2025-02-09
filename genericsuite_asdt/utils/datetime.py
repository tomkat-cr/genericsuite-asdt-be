import datetime


def get_current_year():
    """
    Get the current year.
    """
    return datetime.datetime.now().year


def get_current_date():
    """
    Get the current date.
    """
    return datetime.datetime.now().strftime('%Y-%m-%d')


def get_current_date_time():
    """
    Get the current date and time.
    """
    return datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
