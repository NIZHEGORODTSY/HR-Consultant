import jwt

def decode_jwt(token: str) -> tuple[int, str]:
    decoded = jwt.decode(token, 'ashjashjsahjsfbsduifvbifbdhidiufdbsibfiubuidb')
    return decoded['uid'], decoded['name']