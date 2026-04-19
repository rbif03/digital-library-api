from supabase import Client
from fastapi.responses import JSONResponse

from utils.try_result import TryResult


def try_insert_dict_to_table(
    supabase_client: Client, table_name: str, data_dict: dict
) -> JSONResponse:
    """
    Tries to insert a dictionary into a specified Supabase table and returns a fastapi JSONResponse indicating success or failure.
    """
    try:
        supabase_client.table(table_name).insert(data_dict).execute()
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Added object to database successfully.",
                "data": data_dict,
            },
        )

    except Exception as e:
        error_message = f"Failed to insert into {table_name}: {str(e)}"
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": error_message,
                "data": None,
            },
        )


def try_get_row_by_id(
    supabase_client: Client, table_name: str, row_id: str
) -> TryResult:
    """
    Tries to retrieve a row from a specified Supabase table by its ID and returns a TryResult indicating success or failure.
    """
    try:
        response = (
            supabase_client.table(table_name).select("*").eq("id", row_id).execute()
        )
        data = response.data
        if data:
            return TryResult(success=True, data=data[0])
        else:
            return TryResult(success=False, message=f"No row found with id {row_id}")

    except Exception as e:
        error_message = f"Failed to retrieve from {table_name}: {str(e)}"
        return TryResult(success=False, message=error_message)
