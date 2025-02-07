"""
General utilities
"""
import sys
# from dotenv import load_dotenv

from genericsuite_asdt.utils.datetime import (
    get_current_date, get_current_year)


def get_inputs(project: str = None, topic: str = None):
    # load_dotenv()
    if not project:
        project = sys.argv[1] if len(sys.argv) > 1 else None
    if not topic:
        topic = sys.argv[2] if len(sys.argv) > 2 else None
    if not project and not topic:
        raise Exception('You must provide a project and/or topic')
    return {
        'project': project,
        'topic': topic,
        'year': get_current_year(),
        'current_date': get_current_date(),
    }
