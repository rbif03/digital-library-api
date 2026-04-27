from typing import Literal, Optional, List

from pydantic import BaseModel


class BaseResponse(BaseModel):
    status: Literal["success", "error"]
    message: Optional[str] = None
    data: Optional[List[dict] | dict] = None


class OkResp(BaseResponse):
    """
    Used to return OK Responses
    """
    status: Literal["success"] = "success"


class ErrorResp(BaseResponse):
    """
    Used to return Error Responses
    """
    status: Literal["error"] = "error"


def get_resp_models(*status_codes):
    response_models = {
        200: {"model": OkResp},
        201: {"model": OkResp},
        404: {"model": ErrorResp},
        500: {"model": ErrorResp}
    }
    result = {}
    for status_code in status_codes:
        if status_code in response_models.keys():
            result[status_code] = response_models[status_code]
    print(result)
    return result
