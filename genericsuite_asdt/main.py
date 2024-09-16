#!/usr/bin/env python
import sys
import os

from genericsuite_asdt.crew import GenericsuiteAsdtCrew

from genericsuite_asdt.utils.datetime import (
    get_inputs,
)

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run(project: str = None, topic: str = None):
    """
    Run the crew.
    """
    inputs = get_inputs(project, topic)
    GenericsuiteAsdtCrew().crew().kickoff(inputs=inputs)


def train(project: str = None, topic: str = None):
    """
    Train the crew for a given number of iterations.
    """
    inputs = get_inputs(project, topic)
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
    try:
        GenericsuiteAsdtCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test(project: str = None, topic: str = None):
    """
    Test the crew execution and returns the results.
    """
    inputs = get_inputs(project, topic)
    try:
        GenericsuiteAsdtCrew().crew().test(
            # n_iterations=int(sys.argv[1]),
            n_iterations=int(sys.argv[3] if len(sys.argv) > 3 else 1),
            # openai_model_name=sys.argv[2],
            openai_model_name=os.getenv('OPENAI_MODEL', 'gpt-4-mini'),
            inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
