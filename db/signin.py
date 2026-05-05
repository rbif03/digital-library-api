from pydantic import BaseModel, EmailStr
from supabase import AsyncClient
from supabase_auth.errors import AuthApiError
from tenacity import retry, retry_if_not_exception_type, stop_after_attempt, wait_fixed

from db.core import InvalidSignInCredentialsError


class SigninBody(BaseModel):
    email: EmailStr
    password: str


@retry(
    wait=wait_fixed(2),
    stop=stop_after_attempt(5),
    retry=retry_if_not_exception_type(InvalidSignInCredentialsError),
)
async def sign_in_user(body: SigninBody, supabase_client: AsyncClient):
    print("sign_in_user called")
    try:
        response = await supabase_client.auth.sign_in_with_password(
            body.model_dump(mode="json")
        )
    except AuthApiError as e:
        if e.code == "invalid_credentials":
            raise InvalidSignInCredentialsError("")

    return response
