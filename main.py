import secrets
import base64
import hashlib

# Generate a random code verifier
code_verifier = secrets.token_urlsafe(32)

# Generate the code challenge
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).rstrip(b'=').decode()

print("Code Verifier:", code_verifier)
print("Code Challenge:", code_challenge)