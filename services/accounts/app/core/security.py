import jwt
import uuid
from datetime import datetime, timezone

from cryptography.hazmat.primitives.asymmetric import ed25519
from pwdlib import PasswordHash

from app.core.config import settings
from app.schemas.pydantic_schemas import GetToken, TokensPayload
from app.logic.main_logic import get_time_for_jwt

private_key_bytes = bytes.fromhex(settings.PRIVATE_KEY_HEX)

PRIVATE_KEY = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_bytes)
TOKEN_ALGORITHM = 'EdDSA'
HASH_ALGORITHM = PasswordHash.recommended() # алгоритм Argon2


def hash_password(password: str) -> str:
    return HASH_ALGORITHM.hash(password)


def veryfi_password(raw_password: str, hash_password: str) -> bool:
    return HASH_ALGORITHM.verify(raw_password, hash_password)


def create_tokens(user_uuid: uuid.UUID) -> GetToken:
    now_unix = int(datetime.now(timezone.utc).timestamp())
    exp_access_unix = get_time_for_jwt(now=now_unix, minutes=15)
    exp_refresh_unix = get_time_for_jwt(now=now_unix, days=2)

    json_access_payload = TokensPayload(
        sub = user_uuid,                  # ID пользователя
        iat = now_unix,                   # Время создания
        exp = exp_access_unix,            # Время действия
        token_type = "access"             # Тип токена
    ).model_dump(mode='json')
    json_refresh_payload = TokensPayload(    
        sub = user_uuid,
        iat = now_unix,
        exp = exp_refresh_unix,
        token_type = "refresh"
    ).model_dump(mode='json')

    access_token = jwt.encode(json_access_payload, PRIVATE_KEY, algorithm=TOKEN_ALGORITHM)
    refresh_token = jwt.encode(json_refresh_payload, PRIVATE_KEY, algorithm=TOKEN_ALGORITHM)
    return GetToken(access_token=access_token, refresh_token=refresh_token)


def decode_token(token):
    token = jwt.decode(algorithms=TOKEN_ALGORITHM, key=PRIVATE_KEY, jwt=token)
    return TokensPayload(**token)
