"""
General utilities
"""
import sys

from genericsuite_asdt.utils.datetime import (
    get_current_date, get_current_year)


def get_default_resultset() -> dict:
    """
    Returns a default resultset
    """
    return {
        "resultset": {},
        "error_message": "",
        "error": False,
        "warning": False,
        "warning_message": "",
    }


def error_resultset(
    error_message: str,
    message_code: str = ''
) -> dict:
    """
    Return an error resultset.
    """
    message_code = f" [{message_code}]" if message_code else ''
    result = get_default_resultset()
    result['error'] = True
    result['error_message'] = f"{error_message}{message_code}"
    return result


def get_inputs(project: str = None, topic: str = None,
               mandatory: bool = False):
    result = get_default_resultset()
    if not project:
        project = sys.argv[1] if len(sys.argv) > 1 else None
    if not topic:
        topic = sys.argv[2] if len(sys.argv) > 2 else None
    if not project and not topic:
        if mandatory:
            # raise Exception('You must provide a project and/or topic')
            result['error'] = True
            result['error_message'] = \
                'Project and topic not provided. Stop execution...'
        else:
            project = None
            topic = None
            result['warning'] = True
            result['warning_message'] = \
                'Project and topic not provided. User input required.'
    result['project'] = project
    result['topic'] = topic
    result['year'] = get_current_year()
    result['current_date'] = get_current_date()
    return result
