import uuid
import pytest
from datetime import datetime, timezone

from app.core.security import (verify_password,
                               hash_password,
                               create_tokens, 
                               decode_token)
from app.logic.main_logic import get_time_for_jwt
from app.schemas.pydantic_schemas import GetToken, TokensPayload
from tests.utils_for_tests import test_users, TestPassword


# ----------------- app/core/security.py --------------------
@pytest.mark.unit
def test_hash_password():
    user = test_users[0]
    hashed_pass = hash_password(user.password)
    assert user.password != hashed_pass


@pytest.mark.unit
def test_verify_password():
    true_verify = verify_password(raw_password=TestPassword.password,
                                  hash_password=TestPassword.hashed_password)
    false_verify = verify_password(
        raw_password=f'{TestPassword.password}wrongString',
        hash_password=TestPassword.hashed_password)
    assert true_verify == True
    assert false_verify == False


@pytest.mark.unit
def test_create_tokens_and_decode_token():
    test_uuid = uuid.uuid7()
    tokens = create_tokens(user_uuid=test_uuid)
    access_payload = decode_token(tokens.access_token)
    refresh_payload = decode_token(tokens.refresh_token)
    assert isinstance(tokens, GetToken)
    assert isinstance(tokens.access_token, str)
    assert isinstance(tokens.access_token, str)
    assert isinstance(access_payload, TokensPayload)
    assert isinstance(refresh_payload, TokensPayload)
    assert isinstance(access_payload.sub, uuid.UUID)
    assert isinstance(refresh_payload.sub, uuid.UUID)
    assert access_payload.token_type == 'access'
    assert refresh_payload.token_type == 'refresh'
    assert access_payload.iat < access_payload.exp
    assert refresh_payload.iat < refresh_payload.exp
    assert len(str(access_payload.iat)) == 10
    assert len(str(refresh_payload.iat)) == 10 
    assert len(str(access_payload.exp)) == 10
    assert len(str(refresh_payload.exp)) == 10 
# ---------------------------------------------------------------
 

# -------------------- app/logic/main_logic.py ------------------
@pytest.mark.unit
def test_get_time_for_jwt():
    now_unix = int(datetime.now(timezone.utc).timestamp())
    time_5min = get_time_for_jwt(now=now_unix, minutes=5)
    time_5hours = get_time_for_jwt(now=now_unix, hours=5)
    multi_time = get_time_for_jwt(now=now_unix,
                                  minutes=2, 
                                  hours=1, 
                                  days=2)
    assert len(str(time_5min)) == 10
    assert len(str(time_5hours)) == 10
    assert len(str(multi_time)) == 10
    assert time_5min < time_5hours
    assert time_5hours < multi_time
# ----------------------------------------------------------------
