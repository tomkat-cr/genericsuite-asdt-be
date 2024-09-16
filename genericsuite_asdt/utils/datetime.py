import sys
import datetime

# from pydantic import BaseModel
from dotenv import load_dotenv


# class RunInput(BaseModel):
#     project: str
#     topic: str = "Software Development"
#     year: str = datetime.datetime.now().year


def get_current_year():
    """
    Get the current year.
    """
    return datetime.datetime.now().year


def get_inputs(project: str = None, topic: str = None):
    load_dotenv()
    if not project:
        project = sys.argv[1] if len(sys.argv) > 1 else None
    if not topic:
        topic = sys.argv[2] if len(sys.argv) > 2 else None
    if not project and not topic:
        raise Exception('You must provide a project and/or topic')
    # return RunInput(
    #     project=project,
    #     topic=topic,
    # )
    return {
        'project': project,
        'topic': topic,
        'year': get_current_year(),
    }
