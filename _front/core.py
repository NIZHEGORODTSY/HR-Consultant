import jwt

def decode_jwt(token: str) -> tuple[int, str]:
    decoded = jwt.decode(token, 'ashjashjsahjsfbsduifvbifbdhidiufdbsibfiubuidb', algorithms='HS256')
    return decoded['uid'], decoded['name']