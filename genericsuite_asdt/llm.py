import os

from genericsuite_asdt.genericsuite.util.app_context import AppContext
from genericsuite_asdt.genericsuite_ai.lib.ai_langchain_models import get_model
from genericsuite_asdt.genericsuite.utils.app_logger import log_debug


DEBUG = True


def get_llm_provider(llm_provider: str = None) -> str:
    if llm_provider is None:
        selected_llm_provider = os.environ.get('LANGCHAIN_DEFAULT_MODEL', 'openai')
    else:
        selected_llm_provider = llm_provider
    return selected_llm_provider


def get_llm_name(llm_var_name: str, llm_def_val: str,
                 manager_agent: bool, ma_llm_var_name: str,
                 prefix: str = None) -> str:
    """
    Get the name of the LLM model to use. If manager_agent is True,
    try to find the LLM model name from the *_MANAGER_AGENT_MODEL
    environment variable. If it doesn't exist, use the e *_MODEL value,
    if not, use the default value.

    Args:
        llm_var_name (str): LLM environment variable name.
        llm_def_val (str ): LLM default value.
        manager_agent (bool): Manager agent flag.
        ma_llm_var_name (str): Manager agent LLM environment variable name.
        prefix (str): Prefix to add to the LLM name. Defaults to None.

    Returns:
        str: LLM model name.
    """
    llm = os.environ.get(llm_var_name, llm_def_val)
    if manager_agent and ma_llm_var_name:
        llm = os.environ.get(ma_llm_var_name, llm)
    return f"{prefix+'/' if prefix else ''}{llm}"


def get_llm_agent(
    manager_agent: bool = False,
    llm_provider: str = None
) -> str:
    """
    Get the name of the LLM model to use.

    Args:
    manager_agent (bool): Manager agent flag.Defaults to False.
    llm_provider (str): LLM manufacturer. Possible values:
        "openai", "anthropic", "google", "ollama", "huggingface",
        "groq", None.
        If None, the environment variable LANGCHAIN_DEFAULT_MODEL is used.
        Defaults to None.
    """
    selected_llm_provider = get_llm_provider(llm_provider)

    # LiteLLM models providers reference
    # https://docs.litellm.ai/docs/providers

    if selected_llm_provider == 'anthropic':
        # Using Anthropic's Claude
        llm = get_llm_name('ANTHROPIC_MODEL',
                           'claude-3-5-sonnet-20240620',
                           manager_agent,
                           'ANTHROPIC_MANAGER_AGENT_MODEL')
    elif selected_llm_provider == 'ollama':
        # Using Ollama's local model
        llm = get_llm_name('OLLAMA_MODEL',
                           'llama2',
                           # 'llama3.1',
                           manager_agent,
                           'OLLAMA_MANAGER_AGENT_MODEL',
                           'ollama')
    elif selected_llm_provider == 'google':
        # Using Google's Gemini model
        llm = get_llm_name('GOOGLE_MODEL',
                           'gemini-pro',
                           manager_agent,
                           'GOOGLE_MANAGER_AGENT_MODEL',
                           'gemini')
    elif selected_llm_provider == 'huggingface':
        # Using a Hugging Face model
        llm = get_llm_name('HUGGINGFACE_MODEL',
                           'meta-llama/Meta-Llama-3.1-8B-Instruct',
                           manager_agent,
                           'HUGGINGFACE_MANAGER_AGENT_MODEL'
                           'huggingface')
    elif selected_llm_provider == 'groq':
        # Using a Groq model
        llm = get_llm_name('GROQ_MODEL',
                           'mixtral-8x7b-32768',
                           manager_agent,
                           'GROQ_MANAGER_AGENT_MODEL'
                           'groq')
    else:
        # Using OpenAI's model by default
        llm = get_llm_name('OPENAI_MODEL',
                           'gpt-4o-mini',
                           manager_agent,
                           'OPENAI_MANAGER_AGENT_MODEL')
    _ = DEBUG and log_debug(f'GET_LLM_AGENT | llm: {llm}')
    return llm


def get_llm_model_object(
    manager_agent: bool = False,
    llm_provider: str = None
):
    selected_llm_provider = get_llm_provider(llm_provider)
    app_context = AppContext()
    llm_model_object = get_model(app_context, selected_llm_provider, None,
                                 False)
    _ = DEBUG and log_debug(
        f'GET_LLM_MODEL_OBJECT | manager_agent: {manager_agent}' +
        f' | selected_llm_provider: {selected_llm_provider}' +
        f' | llm_model_object: {llm_model_object}')
    return llm_model_object
