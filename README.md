# DiscBL

DiscBL is an endpoint that returns a JSON key array of blacklisted URLS.

> [!IMPORTANT]
> This is very early! As a matter of fact, i haven't even added a way to request a blacklist! This is also very unneccesary for the average bot, and mostly just to help me learn APIs.

# Why?

Discord bot developers can use this endpoint to automatically delete hash-verified blacklisted URLs such as porn and gore.

# How to use this?

For the full blacklist per category:
`https://discbl.sdlsr.dpdns.org/blacklist?c=[category]`

The response is an object that maps each file hash in that category to the list of known URLs:
```Json
{
    "[hash]": [
        "[knownlink]",
        "[another known link]"
    ],
    "[hash2]": [
        "[knownlink]"
    ]
}
```

Or you can use the search to avoid somewhat large data usage:
`https://discbl.sdlsr.dpdns.org/blacklist/search?file_hash=[file_hash]`

The search returns this little piece of Json if found:
```Json
{
    "found": "true",
    "hash": "[file_hash]"
}
```
And this if not found:
```Json
{
    "found": "false"
}
```

A human readable view of the blacklist is available at `/blacklist/view`:
`https://discbl.sdlsr.dpdns.org/blacklist/view`

It shows every category by default; pass `?c=[category]` to view a single one.

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

Create the blacklist file:

The server reads `blacklist.json` on startup and does not create it, so the file must already exist. An empty blacklist is just an empty object:

```Bash
echo '{}' > blacklist.json
```

Create the .env:

```env
API_KEY=sat_...
BASE_DOMAIN=YourDomainOrLocalHost
```

Run the server. The `blacklist.json`, `templates` and `static` paths are relative, so the server has to be started from inside `src`:

```Bash
uvicorn main:app
```

Or use the included `start.sh`, which installs the dependencies and serves on port 19291:

```Bash
./start.sh
```

### Blacklisting

You can blacklist Hashes/URLS on your own server by sending a GET request to `/blacklist/add`:

```URI
https://example.com/blacklist/add?auth=sat_...&c=[category]&file_hash=[file_hash]&url=[file_url]
```

If the category or hash does not exist yet it is created, and the URL is appended to the hash otherwise. The endpoint answers with an error object when a parameter is missing, the key is wrong, or the URL is already listed for that hash.
