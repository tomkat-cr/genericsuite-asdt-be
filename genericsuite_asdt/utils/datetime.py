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
