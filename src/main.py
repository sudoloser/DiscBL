import aiohttp
import asyncio
import json
import os

from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pathlib import Path

load_dotenv()

api_key = os.getenv("API_KEY")
base_domain = os.getenv("BASE_DOMAIN")

# Define a new fastapi app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


filename = "blacklist.json"
filepath = Path(filename)

if filepath.is_file():
    with open(filename, 'r', encoding="utf-8") as file:
        blacklist = json.load(file)
else:
    with open(filename, 'w', encoding="utf-8") as file:
        file.write("{}")


categories = []
for i in blacklist:
    categories.append(i)
    print(i)

# Define root endpoint
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "base_domain": base_domain
        }
    )

# Define health endpoint
@app.get("/health")
async def health():
    return {"Status": "OKAY"}

@app.get("/blacklist")
async def blacklist_route(c: str = None):

    if c is None:
        return {"Error": "Please provide the desired category in the query."}
    if c in blacklist and blacklist[c]:
        return blacklist[c]
    return {"Error": f"Provided category is not valid. Available categories: {categories}"}

@app.get("/blacklist/search")
async def blacklist_search(file_hash: str = None):
    if file_hash is None:
        return {"Error": "Please specifiy a File Hash to query for."}
    else:
        for category, items in blacklist.items():
            for item in items:
                if item == file_hash.lower():
                    return {"found": "true", "hash": file_hash}
        return {"found": "false"}

@app.get("/blacklist/view")
async def blacklist_view(request: Request, c: str = "all"):

    if c.lower() == "all":
        temp = blacklist
    else:
        if c in blacklist:
            c = c.lower()
            temp = {
                c: {}
            }
            temp[c] = blacklist[c]
        else:
            return {"error", "Provided category does not exist"}
    return templates.TemplateResponse(
        request = request,
        name = "blacklist.html",
        context = {
           "blacklist": temp
        }
    )

@app.get("/blacklist/add")
async def blacklist_add(auth: str = None, c: str = None, file_hash: str = None, url: str = None):

    if auth is None:
        return {"Error": "Access not permitted"}
    if c is None:
        return {"Error": "Please provide a category to add to"}
    if file_hash is None:
        return {"Error": "Please provide file hash"}
    if url is None:
        return {"Error": "Please provide media url"}

    if auth != api_key:
        return {"Error": "Access not permitted"}
    else:
        if c in blacklist:
            if file_hash in blacklist[c]:
                for i in blacklist[c][file_hash]:
                    if i == url:
                        return {"Error": "The provided url is already present in the blacklist."}
                blacklist[c][file_hash].append(url)
            else:
                blacklist[c][file_hash] = [
                    f"{url}"
                ]
        else:
            blacklist[c] = {
                file_hash: [url]
            }
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(blacklist, file, indent=4)
        return {"Status": "Success.", "Category": f"{c}", "file_hash": f"{file_hash}", "URL": f"{url}"}