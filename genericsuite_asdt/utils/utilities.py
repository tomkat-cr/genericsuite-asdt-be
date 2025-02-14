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


def remove_undesired_chars(text: str) -> str:
    """
    Remove undesired chars from a string. This solves the error:
    "ValueError: unsupported format character '%' (0x25) at index..."
    during the Planning step of the crew execution

    Args:
        text (str): The string to clean.

    Returns:
        str: The cleaned string.
    """
    return text.replace('%', '%%')


def get_file_or_text(file_or_text: str) -> dict:
    """
    Returns the content of a file if it starts with '[' and ends with ']'.
    Otherwise, returns the original string.

    Args:
        file_or_text (str): The string to check.

    Returns:
        str: The content of the file, or the original string.
    """
    result = get_default_resultset()
    result['content'] = None
    result['file_path'] = None
    if file_or_text.startswith('[') and file_or_text.endswith(']'):
        try:
            file_or_text = file_or_text[1:-1]
            with open(file_or_text, 'r') as f:
                result['content'] = f.read()
                result['file_path'] = file_or_text
        except Exception as e:
            result['error'] = True
            result['error_message'] = f"Error parsing file or text: {e}"
            return result
    else:
        result['content'] = file_or_text
    if result['content']:
        result['content'] = remove_undesired_chars(result['content'])
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

    file_or_text = get_file_or_text(project)
    if file_or_text['error']:
        result['error'] = True
        result['error_message'] = \
            f'Project cannot be loaded from file' \
            f' "{file_or_text["file_path"]}":' \
            f' {file_or_text["error_message"]}'
    else:
        result['project'] = file_or_text['content']

    file_or_text = get_file_or_text(topic)
    if file_or_text['error']:
        result['error'] = True
        result['error_message'] = \
            f'Topic cannot be loaded from file' \
            f' "{file_or_text["file_path"]}":' \
            f' {file_or_text["error_message"]}'
    else:
        result['topic'] = file_or_text['content']

    result['year'] = get_current_year()
    result['current_date'] = get_current_date()
    return result
