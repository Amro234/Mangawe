from typing import Optional
from pydantic import BaseModel, ConfigDict

class TokenResponse_Base(BaseModel):
    access_token : str
    token_type: str = 'bearer'