# DiscBL

DiscBL is an endpoint that returns a JSON key array of blacklisted URLS.

# Why?

Discord bot developers can use this endpoint to automatically delete hash-verified blacklisted URLs such as porn and gore.

# How to use this?

To use this API, send a GET request to the following URL:
`https://discbl.sdlsr.dpdns.org/blacklist?category=[category]`

Permitted categories can be found [here](https://discbl.sdlsr.dpdns.org/blacklist/view)

The response looks like this:
```Json
{
  "[category]": {
    "[hash]": [
        "[knownlink]",
        "[another known link]"
    ],
    "[hash2]": [
        "[knownlink]"
    ]
  }
}
```

# Get started with self hosting

Install the dependencies:

```Bash
cd src
pip install -r requirements.txt
```

Generate the Api Key:

```Bash
python3 generate_api_key.py
```

Create the .env:

```env
API_KEY=sat_...
BASE_DOMAIN=YourDomainOrLocalHost
```

Run the server:

```Bash
uvicorn main:app
```

### Blacklisting

You can blacklist Hashes/URLS on your own server by sending a GET request to `/blacklist/add`:

```URI
https://example.com/blacklist/add?auth=sat_...&c=[category]&file_hash=[file_hash]&url=[file_url]
```