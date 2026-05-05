from supabase import acreate_client, AsyncClient


class DatabaseError(Exception):
    pass


class NotFoundError(Exception):
    pass


class ForeignKeyError(Exception):
    pass


class InvalidSignInCredentialsError(Exception):
    pass


def get_supabase_client(url: str, key: str):
    """Factory that returns an async dependency function with url and key baked in."""

    async def dependency() -> AsyncClient:
        supabase: AsyncClient = await acreate_client(url, key)
        return supabase

    return dependency
