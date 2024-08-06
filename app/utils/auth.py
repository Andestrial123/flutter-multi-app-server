from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from firebase_admin import auth
from firebase_admin.auth import ExpiredIdTokenError


class FirebaseHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> dict:
        from fastapi import status
        try:
            r = await super().__call__(request)
            token = r.credentials
            token = auth.verify_id_token(token)
        except HTTPException as ex:
            assert ex.status_code == status.HTTP_403_FORBIDDEN, ex
            token = None
        except ExpiredIdTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'
            )

        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'
            )

        return token


auth_schema = FirebaseHTTPBearer()
