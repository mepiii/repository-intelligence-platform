from auth.jwt_auth import TokenService

def test_token_creation():
    token = TokenService.create_access_token("user123")
    assert token is not None
