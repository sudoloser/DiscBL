import secrets

key = secrets.token_urlsafe(24)

print("sat_" + key)
print("Note: 'sat_' stands for 'standard access token'.")