"""
General utilities
"""
import os
import sys

from genericsuite_asdt.utils.datetime import (
    get_current_date, get_current_year)


# Stantdard resultsets


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


# User's input handling


def remove_undesired_chars(text: str, replacements: str = "%") -> str:
    """
    Replace special characters from a string with their double.
    This solves the error:
        "ValueError: unsupported format character '%' (0x25) at index..."
    during the Planning step of the crewai execution and other 
    frameworks' input handling (e.g. Camel-AI requires to use "{{" and "}}"
    in addition to "%%").

    Args:
        text (str): The string to clean.
        replacements (str): The characters to replace. E.g. "%{}".
            Defaults to "%".

    Returns:
        str: The cleaned string.
    """
    for rep in replacements:
        text = text.replace(rep, rep*2)
    return text


def get_file_or_text(file_or_text: str, replacements: str = "%") -> dict:
    """
    Returns the content of a file if it starts with '[' and ends with ']'.
    Otherwise, returns the original string.

    Args:
        file_or_text (str): The string to check.
        replacements (str): The characters to replace. E.g. "%{}".
            Defaults to "%".

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
        result['content'] = remove_undesired_chars(result['content'],
                                                   replacements)
    return result


def get_inputs(project: str = None, topic: str = None,
               mandatory: bool = False):
    """
    Get the project and topic from the command line arguments.
    If mandatory, return a error if the project or topic is not provided.

    Args:
        project (str): The project to use.
        topic (str): The topic to use.
        mandatory (bool): Whether to return an error if the project or topic
            is not provided. Defaults to False.

    Returns:
        dict: A dictionary with the project, topic, year, current_date, error,
            and error_message.
    """
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


# LLM PRovider and Model handling


def add_v1(base_url: str) -> str:
    """
    Adds /v1 to the end of a base URL if it doesn't already end with /v1.
    Additionally add the http:// prefix if it doesn't already have one.

    Args:
        base_url (str): The base URL.

    Returns:
        str: The base URL with /v1 appended, if necessary.
    """
    if base_url.endswith('/'):
        base_url = base_url[:-1]
    if not base_url.endswith('/v1'):
        base_url = base_url + '/v1'
    if not base_url.startswith('http'):
        base_url = 'http://' + base_url
    return base_url


def get_llm_provider(llm_provider: str = None, agent_role: str = None) -> str:
    """
    Get the LLM provider. If agent_role is not None, looks for the LLM provider
    in the DEFAULT_<agent_role>_LLM_PROVIDER environment variable.

    Args:
        llm_provider (str): LLM provider. Possible values:
            "openai", "anthropic", "google", "ollama", "huggingface",
            "groq", "xai", "together_ai", "openrouter", "aimlai" or None.
            If None, the environment variable DEFAULT_LLM_PROVIDER is used.
            Defaults to None.
        agent_role (str): Agent type: 'manager', 'coding', 'reasoning'
            or None. Defaults to None.

    Returns:
        str: LLM provider.
    """
    if llm_provider is None:
        selected_llm_provider = os.environ.get(
            'DEFAULT_LLM_PROVIDER',
            'ollama')
    else:
        selected_llm_provider = llm_provider
    if agent_role is not None:
        var_name = f'DEFAULT_{agent_role.upper()}_LLM_PROVIDER'
        selected_llm_provider = os.environ.get(var_name, selected_llm_provider)
    return selected_llm_provider


def get_llm_name(
    llm_var_base_name: str,
    llm_def_val: str,
    agent_role: str,
    prefix: str = None
) -> str:
    """
    Get the name of the LLM model to use. If agent_role is not None,
    find the LLM model name from the DEFAULT_<agent_role>_MODEL_NAME
    environment variable. If it doesn't exist, use the DEFAULT_MODEL value,
    if not, use the llm_def_val value.

    Args:
        llm_var_base_name (str): LLM environment variable base name.
        llm_def_val (str ): LLM default value.
        agent_role (str): Agent type: 'manager', 'coding', 'reasoning'
            or None.
        prefix (str): Prefix to add to the LLM name. Providers like LiteLLM
            require a prefix to differentiate between LLM providers, e.g.
            "ollama/llama32" to handle ollama models, or "gemini/gemini-pro"
            to handle google models.
            Defaults to None.

    Returns:
        str: LLM model name.
    """
    llm_var_name = f"{llm_var_base_name}_MODEL_NAME"
    llm = os.environ.get(llm_var_name, llm_def_val)
    if agent_role:
        ma_llm_var_name = f"{llm_var_base_name}_{agent_role.upper()}" \
                          "_MODEL_NAME"
        llm = os.environ.get(ma_llm_var_name, llm)
    return f"{prefix+'/' if prefix else ''}{llm}"


def get_default_llm_settings() -> dict:
    """
    Returns a default LLM settings
    """
    return {
        "temperature": 0.7,        # Higher for more creative outputs
        # "timeout": 120,            # Seconds to wait for response
        # "max_tokens": 4000,        # Maximum length of response
        # "top_p": 0.9,              # Nucleus sampling parameter
        # "frequency_penalty": 0.1,  # Reduce repetition
        # "presence_penalty": 0.1,   # Encourage topic diversity
        # "response_format": {"type": "json"},  # For structured outputs
        # "seed": 42                 # For reproducible results
    }
