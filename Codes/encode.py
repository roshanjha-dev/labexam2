import urllib.parse

# Original payload
payload = '<script>alert("hacked")</script>'

# Perform single-level URL encoding for each character in the string
encoded_payload = ''.join([urllib.parse.quote(char) for char in payload])

# Print the encoded payload
print(encoded_payload)


# Single encoded:
# %3C%73%63%72%69%70%74%3E%61%6C%65%72%74%28%22%68%61%63%6B%65%64%22%29%3C%2F%73%63%72%69%70%74%3E
