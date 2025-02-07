from typing import Any, Dict, Optional, Union
from pydantic import BaseModel


class Request(BaseModel):
    """
    Request class cloned from the selected Request framework super class.
    This class is the one to be imported by the project modules
    """
    method: Optional[str] = "GET"
    query_params: Optional[dict] = {}
    json_body: Optional[dict] = {}
    headers: Optional[dict] = {}
    event_dict: Optional[Dict[str, Any]] = {}
    lambda_context: Optional[Any] = None

    def to_dict(self):
        """
        Returns the request data as a dictionary.
        """
        return {
            "method": self.method,
            "query_params": self.query_params,
            "json_body": self.json_body,
            "headers": self.headers,
        }

    def to_original_event(self) -> Union[Dict[str, Any], None]:
        """
        Returns the original event dictionary.
        """
        return self.event_dict


class AuthTokenPayload(BaseModel):
    """
    Represents the user's payload structure of the JWT token.
    """
    public_id: str


class AuthorizedRequest(Request):
    """
    Represents the AuthorizedRequest payload structure of the JWT token,
    containing the authenticated user's data.
    """
    user: AuthTokenPayload
