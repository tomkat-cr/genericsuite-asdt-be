import os

from crewai import LLM

from genericsuite_asdt.utils.app_logger import log_debug
from genericsuite_asdt.utils.utilities import (
    get_llm_provider,
    get_llm_name,
    get_default_llm_settings,
)


DEBUG = True


def get_llm_data(
    agent_role: str = None,
    llm_provider: str = None
) -> dict:
    """
    Get the data (model name, base_url, etc) of the LLM model to use.

    Args:
        agent_role (str): Manager agent type: 'manager', 'coding',
            'reasoning' or None. Defaults to None.
        llm_provider (str): LLM manufacturer. Possible values:
            "openai", "anthropic", "google", "ollama", "huggingface",
            "groq", "xai" or None.
            If None, the environment variable DEFAULT_LLM_PROVIDER is used.
            Defaults to None.
    """
    selected_llm_provider = get_llm_provider(llm_provider, agent_role)
    llm_config = {}
    llm_settings = get_default_llm_settings()

    # LiteLLM models providers reference
    # https://docs.litellm.ai/docs/providers

    if selected_llm_provider == 'openai':
        # Using OpenAI's model
        llm_name = get_llm_name(
            'OPENAI',
            'gpt-4o-mini',
            agent_role)
        llm_config["api_key"] = os.environ.get('OPENAI_API_KEY')

    elif selected_llm_provider == 'google':
        # Using Google's Gemini model
        llm_name = get_llm_name(
            'GOOGLE',
            'gemini-pro',
            agent_role,
            'gemini')
        llm_config["api_key"] = os.environ.get('GOOGLE_API_KEY')

    elif selected_llm_provider == 'anthropic':
        # Using Anthropic's Claude
        llm_name = get_llm_name(
            'ANTHROPIC',
            'claude-3-5-haiku-latest',
            agent_role)
        llm_config["api_key"] = os.environ.get('ANTHROPIC_API_KEY')

    elif selected_llm_provider == 'huggingface':
        # Using a Hugging Face model
        llm_name = get_llm_name(
            'HUGGINGFACE',
            'meta-llama/Meta-Llama-3.1-8B-Instruct',
            agent_role,
            'huggingface')
        llm_config["api_key"] = os.environ.get('HUGGINGFACE_API_KEY')

    elif selected_llm_provider == 'groq':
        # Using a Groq model
        llm_name = get_llm_name(
            'GROQ',
            'mixtral-8x7b-32768',
            agent_role,
            'groq')
        llm_config["api_key"] = os.environ.get('GROQ_API_KEY')

    elif selected_llm_provider == 'aimlapi':
        # Using a AI/ML API model
        llm_name = get_llm_name(
            'AIMLAPI',
            'gpt-4o-mini-2024-07-18',
            agent_role,
            'openai')
        llm_config["base_url"] = "https://api.aimlapi.com"
        llm_config["api_key"] = os.environ.get('AIMLAPI_API_KEY')

    elif selected_llm_provider == 'together_ai':
        # Using a Together AI model
        llm_name = get_llm_name(
            'TOGETHER_AI',
            'meta-llama/Llama-3.3-70B-Instruct-Turbo-Free',
            agent_role,
            'togethercomputer')
        llm_config["base_url"] = "https://api.together.xyz/v1"
        llm_config["stop"] = ["<|eot_id|>", "<|eom_id|>"]
        llm_config["api_key"] = os.environ.get('TOGETHER_AI_API_KEY')

    elif selected_llm_provider == 'openrouter':
        # Using a Groq model
        llm_name = get_llm_name(
            'OPENROUTER',
            'google/gemini-2.0-flash-exp:free',
            agent_role,
            'openrouter')
        llm_config["base_url"] = "https://openrouter.ai/api/v1"
        llm_config["api_key"] = os.environ.get('OPENROUTER_API_KEY')

    else:
        # Using Ollama's local model (default)
        llm_name = get_llm_name(
            'OLLAMA',
            'llama3.2',
            agent_role,
            'ollama')
        llm_config["base_url"] = os.environ.get(
            'OLLAMA_BASE_URL', 'http://localhost:11434')
        llm_settings = {
            "options": dict(llm_settings)
        }

    result = {
        'provider': selected_llm_provider,
        'name': llm_name,
        'config': llm_config,
        'settings': llm_settings
    }
    # _ = DEBUG and log_debug(f'get_llm_data | result: {result}')
    return result


def get_llm_model_object(
    agent_role: str = None,
    llm_provider: str = None
):
    """
    Get the LLM model object.

    Args:
        agent_role (str): Manager agent type: 'manager', 'coding',
            'reasoning' or None. Defaults to None.
        llm_provider (str): LLM provider. Possible values:
            "openai", "anthropic", "google", "ollama", "huggingface",
            "groq", "xai" or None.
            If None, the environment variable DEFAULT_LLM_PROVIDER is used.
            Defaults to None.

    Returns:
        LLM: LLM model object.
    """
    model_data = get_llm_data(agent_role, llm_provider)

    model_param = dict(model_data['config'])
    model_param.update(dict(model_data['settings']))
    model_param["model"] = model_data['name']

    llm = LLM(**model_param)

    _ = DEBUG and log_debug(
        '>> GET_LLM_MODEL_OBJECT'
        f'\n | agent_role: {agent_role}'
        f'\n | llm_provider: {llm_provider}'
        f'\n | model_data: {model_data}'
        f'\n | model_param: {model_param}'
        # f'\n | llm_model_object: {llm}'
    )
    return llm
