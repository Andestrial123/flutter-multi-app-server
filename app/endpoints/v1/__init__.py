from fastapi import APIRouter, Depends

from app.utils.auth import auth_schema

router_v1 = APIRouter(
    prefix="/multi/v1",
    tags=["Routes v1"],
    dependencies=[Depends(auth_schema)],
    responses={
        401: {
            "description": "Not Authorized"
        },
        404: {
            "description": "Not Found"
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example":
                        {
                            "detail": [
                                {
                                    "loc": [
                                        "string",
                                        0
                                    ],
                                    "msg": "string",
                                    "type": "string"
                                }
                            ]
                        }
                }
            }
        },
        500: {
            "description": "Internal Server Error"
        },
    },
)
