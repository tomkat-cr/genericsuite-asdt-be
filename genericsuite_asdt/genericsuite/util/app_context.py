from typing import Any, Optional, Union
from genericsuite_asdt.genericsuite.util.jwt import AuthorizedRequest


class AppContext:
    """
    Context manager class to preserve data between GPT functions
    """
    def __init__(
        self,
        request: Optional[Union[AuthorizedRequest, None]] = None,
        blueprint: Optional[Any] = None
    ):
        # AuthorizedRequest object received from the endpoit handler
        self.request = request
        # Blueprint object received from the endpoit handler
        self.blueprint = blueprint
        # Curret user's data
        self.user_data = None
        # Any error happened during the user's data or other retrievals
        self.error_message = None
        # "self.other" was created to make globally available some values that
        # should not be calculated each time a GPT function is called.
        self.other_data = {}
        # Environment variables loaded from the database
        self.env_data = {}
