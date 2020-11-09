from Authentication import authenticate
from Crypto.PublicKey import RSA
import requests
from authlib.specs.rfc7519 import jwt

# parses the browser url in the submission page to isolate and return the authorization code
def getAuthCode(returned_url):
    splice = returned_url.split("=")
    return splice[1]

# parses information returned in the tokens string to isolate and return the ID token
def getIDToken(token):
    info = token.split(":")
    idToken = info[5]
    idTokenFinal = idToken[1:len(idToken) - 2]
    return str(idTokenFinal)

# decodes the ID token using a public key and authlib jwt, returns a JWTClaims object containing user information
def decodeToken(ID_token):
    public_key = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0VigO/g6UR7rL9g6lhq9EXQLWlHeml8h+HnLv+wGKvDcD9lgSlVDGMnKc9yvjm9s4CRfkLD2UuHwN/95snMU6VSXnWy43Ns0zXqU1rEWojw/7rIIRNfbukqSo1yiunWU+x98N+rKZCn3kTf1m+TN96TLtjs8ucqQkNblVLYTUIA/50CDpMfKqAj1EhPRZgYJCP5aKD+ju8Qq51kw60oIgY5uJo02/dgf0sr9hQffKOLHhLY0wdrgVo6BLa0IRNMyp42VWp9PZtoT3PkbVTVdxw07ulay5UMjMEiMd2LPBYvNITAFoqt/w+62cW3seEPW8i1zglUIdmjCzZREKiJQ3wIDAQAB\n-----END PUBLIC KEY-----'
    claims = jwt.decode(ID_token, public_key) # decode version using authlib jwt, not pyjwt
    return claims

# parses information in the decoded token to isolate and return the user's email
def getUserEmail(claims):
    info = str(claims)
    startPos = info.find(":")
    endPos = info.find(",")
    email = info[startPos + 3: endPos - 1]
    return email

# parses information in the decoded token to isolate and return the user's netID
def getUserNetID(claims):
    info = str(claims)
    startPos = info.find(":")
    endPos = info.find("@")
    netID = info[startPos + 3: endPos]
    return netID




# code = getAuthCode("http://localhost:5000/submission?code=L5lTte")
# token = authenticate(code)
# toke = getIDToken(token)
# claims = jwt.decode(toke, public_key) # decode version using authlib jwt, not pyjwt
# print(getUserEmail(claims))
# print(getUserNetID(claims))



#{'sub': 'nbk5@duke.edu', 'aud': 'bugbounty_dev', 'kid': 'rsa1', 'iss': 'https://oauth.oit.duke.edu/oidc/', 'exp': 1594826640, 'iat': 1594826040, 'jti': '86714ffd-69cf-431d-998a-56870427c59c'}

# key = RSA.generate(2048)
# private_key = key.exportKey()
# public_key = key.publickey().exportKey()
#jwt_options = {'verify_signature': True, 'verify_exp': True, 'verify_nbf': False, 'verify_iat': True, 'verify_aud': False}
# decoded = jwt.decode(toke, key=public_key, algorithms=['RS256'], options=jwt_options) // decode version using pyjwt, not authlib jwt



# def getAccessToken(token):

#     info = token.split(":")
#     excessInfo = info[1]
#     tokenInfo = excessInfo.split(",")
#     accessToken = tokenInfo[0]
#     #print(accessToken)
#     return accessToken


# def getUserInfo(access_token):

#     api_url = "https://oauth.oit.duke.edu/oidc/.well-known/openid-configuration"

#     headers = {'X-API-Key': "bugbounty_dev", 'Authorization': 'Bearer $'+ access_token}

#     r = requests.get(api_url, headers=headers)

#     ret = r.text

#     print(ret)
#     return ret

# getUserInfo(id_token)

#"eyJraWQiOiJyc2ExIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJuYms1QGR1a2UuZWR1IiwiYXpwIjoiYnVnYm91bnR5X2RldiIsImlzcyI6Imh0dHBzOlwvXC9vYXV0aC5vaXQuZHVrZS5lZHVcL29pZGNcLyIsImV4cCI6MTU5NDMwNjI5NCwiaWF0IjoxNTk0MzA1Njk0LCJqdGkiOiJhYjA2N2RiNC05MDBjLTRlMWQtYWUyYS02NDlhMmFhZjZjNGEifQ.X_6Nq27J4b2trtKkjLHokqVaYeSCd26VhptXCr3Qhs3DiXomnErH4-8PGCMsH_D43xX-OHhXSu_nRdR2PIYiMj0tOgxqMpKObly1EUi6O4VCTqVB9rZlulLBZiv4x4uU0D2xXQ5-WTY4o5Dt-OtZAolFMSmY0Pxx57H2qlhI6nfomjAeZ7YzmtzQ3LQpQV8k1vC7AsmcgWhCaesbgUag0OiDPbHttZvhHO0lZZrARoEda-q55dHPeQ5vHElv2VEz05SF1KK_pMCBluwJzeGdw5ppQmrHU_SVv_-ztqSfvM0PNxp44OJ0tyw59QpJ9IMyAch7xIEJiJnEthA37ruI_g","token_type"

#{"access_token":"eyJraWQiOiJyc2ExIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJuYms1QGR1a2UuZWR1IiwiYXpwIjoiYnVnYm91bnR5X2RldiIsImlzcyI6Imh0dHBzOlwvXC9vYXV0aC5vaXQuZHVrZS5lZHVcL29pZGNcLyIsImV4cCI6MTU5NDMwNTU1NywiaWF0IjoxNTk0MzA0OTU3LCJqdGkiOiIyZWI2ZmFlMy01YmZkLTRmOGEtYTkwYi01N2QwNTQ1MWJmOWMifQ.MxDje-JpPrLAWJxJ7cb6nKejNWvnaX_o7sbN9X2y_A8zUwvlJO0cWUFEm6Hl07HVivEMhOs7IUQyqJpJKDwN9sadJVP8B5Ug8dUGGXC8XXkqhq63gxvWu_cQFuBWzNXVjwcUi3fsUe2Oxz8iKJ13E742k9D7RihBLcKAF22j5An6ydZIsfyfnoFIBzxwrOGGNAVkzYR4nruNVC6KSMbyQys2VBVPXzRapOFvJBYPqjGGEwIh12FqU_7o681p6LDyv_-KB9KSBS8Xq3z1f8XQwuIXvc2U03QGS0shkchZ_9wsdOSXIPyFQwk9UuTigMrsorCBMuEMjaCQ8GeeQ8vuWg","token_type":"Bearer","expires_in":599,"scope":"openid","id_token":"eyJraWQiOiJyc2ExIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJuYms1QGR1a2UuZWR1IiwiYXVkIjoiYnVnYm91bnR5X2RldiIsImtpZCI6InJzYTEiLCJpc3MiOiJodHRwczpcL1wvb2F1dGgub2l0LmR1a2UuZWR1XC9vaWRjXC8iLCJleHAiOjE1OTQzMDU1NTcsImlhdCI6MTU5NDMwNDk1NywianRpIjoiNjM4NzEzZmUtMWI0Zi00NDU4LWFiMDAtZDM5NGJiYzYxMGY4In0.SxOkmelTObH_QiVYXeN2HUHCgj7Y-hTxYPdIctqcdQ1wqaiaXL7WHz7nDDyRUQpuEf8Y0od8Dv7faWRHN9Ubf5fItpgfuj2ufj6aJ1pTHJ2BHvBGK-zdR06J2XyEfDxZqhOZ4IWulw6BNc4SMQZI84sCJ_xpL_djG3sH2c-KldXfRxMJ9dKhFs94WXvuqaXI-EcVLPn7BX1G-nvVKILzAG9XpifwW00WXJVJM42f6Oqb8gvgB27Vb4aln3egqFBU7eDm9ECNgZvSrb5RRCV9ATKK3UU5NYrqJmFB_uXeHqmk9FuMSvaKNCv5oPYVgGa-bdq_RFfU7pGeGu0XBYPhLw"}

# below code didn't work because it's not a dictionary
# for k, v in token.items():
#         if k == "access_token":
#             accessToken = v