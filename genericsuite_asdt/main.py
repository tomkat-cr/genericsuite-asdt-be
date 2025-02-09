#!/usr/bin/env python
import sys
import os
from dotenv import load_dotenv

from genericsuite_asdt.utils.app_logger import log_debug, log_error

from genericsuite_asdt.crew import GenericsuiteAsdtCrew
from genericsuite_asdt.utils.utilities import get_inputs

DEBUG = True

load_dotenv()

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


if os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT'):
    # Monitoring
    _ = DEBUG and log_debug("Initializing OpenLit...")
    import openlit
    openlit.init()
    _ = DEBUG and log_debug("OpenLit initialized")


def run(project: str = None, topic: str = None):
    """
    Run the crew.
    """
    inputs = get_inputs(project, topic)
    if inputs['error']:
        log_error(inputs['error_message'])
        return
    _ = DEBUG and log_debug(f"CrewAI Run | Inputs: {inputs}")
    _ = DEBUG and log_debug("Command line mode...")
    crew = GenericsuiteAsdtCrew().crew()
    crew.kickoff(inputs=inputs)


def stream_run(project: str = None, topic: str = None):
    """
    Run the crew and stream the output.
    """
    inputs = get_inputs(project, topic)
    if inputs['error']:
        log_error(inputs['error_message'])
        return
    _ = DEBUG and log_debug(f"CrewAI stream_run | Inputs: {inputs}")
    _ = DEBUG and log_debug("Streamimg mode...")
    result = GenericsuiteAsdtCrew().crew().kickoff(inputs=inputs)
    for line in result.split('\n'):
        yield line


def train(project: str = None, topic: str = None):
    """
    Train the crew for a given number of iterations.
    """
    inputs = get_inputs(project, topic)
    if inputs['error']:
        log_error(inputs['error_message'])
        return
    n_iterations = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    filename = sys.argv[4] if len(sys.argv) > 4 else None
    _ = DEBUG and log_debug(f"CrewAI Train | Inputs: {inputs}" +
                            f"\nN_iterations: {n_iterations}" +
                            f"\nFilename: {filename}")
    try:
        GenericsuiteAsdtCrew().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    task_id = int(sys.argv[1]) if len(sys.argv) > 1 else None
    _ = DEBUG and log_debug(f"CrewAI Train | task_id: {task_id}")
    try:
        GenericsuiteAsdtCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test(project: str = None, topic: str = None):
    """
    Test the crew execution and returns the results.
    """
    inputs = get_inputs(project, topic)
    if inputs['error']:
        log_error(inputs['error_message'])
        return
    n_iterations = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    openai_model_name = os.getenv('TESTING_MODEL_NAME', 'ollama/llama3.2')
    _ = DEBUG and log_debug(f"CrewAI Train | Inputs: {inputs}" +
                            f"\nN_iterations: {n_iterations}" +
                            f"\nOpenai_model_name: {openai_model_name}")
    try:
        GenericsuiteAsdtCrew().crew().test(
            n_iterations=n_iterations,
            openai_model_name=openai_model_name,
            inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


if __name__ == "__main__":
    project = input("What is the project (purpose/question/action)? ")
    topic = input("Optionally, what is the topic? ")
    run(project, topic)
    # for output in stream_run(project, topic):
    #     print(output)
