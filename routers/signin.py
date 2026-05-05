from typing import Annotated

from fastapi import APIRouter, Depends
from supabase import AsyncClient

import config
from db.core import get_supabase_client
from db.signin import SigninBody, sign_in_user

supabase_dependancy = get_supabase_client(config.SUPABASE_URL, config.SUPABASE_KEY)

router = APIRouter(prefix="/signin")


@router.post("/")
async def signin_user(
    body: SigninBody,
    supabase_client: Annotated[AsyncClient, Depends(supabase_dependancy)],
):
    response = await sign_in_user(body, supabase_client)
    return response
