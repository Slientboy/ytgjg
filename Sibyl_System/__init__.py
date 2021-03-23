"""Gets ENV vars or Config vars then calls class."""

from telethon import events
from telethon.sessions import StringSession
from motor import motor_asyncio
import aiohttp
import json
from datetime import datetime
import logging
import os
import re


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

ENV = bool(os.environ.get("ENV", False))
if ENV:
    API_ID_KEY = int(os.environ.get("3683760"))
    API_HASH_KEY = os.environ.get("753f879b9411fe8d3d3dc2eb01160eab")
    STRING_SESSION = os.environ.get("1BVtsOHgBu4Q6QTirbBVedC6PwfRpEIPvTYaJanFy3nQcSWdeCRN-KfIAdu7RLsehZw5iOIi65sOSsj0rgneLxItyB1kJe7mySQS0vWLGB31Ylt--3TQPWjD5SvM91zQYoXpuFY3cm_nkZVOvCAHefmM501FaG1LLFZHs_znLAcXRJSYpp1ynzYpVx6G6ugg0ruInAJhPY7ElYFVoARERiNCPasxUlIlzf5SYv-3xlPty9FtlUQj_XUVNIavnjWse-05Ma6KTfka4X6GjWatbTEWpvWgZ98_9N1Y46PycwNkYMWs8Irl8UEpTYDb-TVmXaLRIlqW-ZQhnsT1Y6Dx6RutO4y0a7uw=")
    HEROKU_API_KEY = os.environ.get("86794ca3-299c-448a-aeb3-0c027c0c7698")
    HEROKU_APP_NAME = os.environ.get("itachia")
    RAW_SIBYL = os.environ.get("SIBYL", "")
    RAW_ENFORCERS = os.environ.get("ENFORCERS", "")
    SIBYL = list(int(x) for x in os.environ.get("SIBYL", "").split())
    INSPECTORS = list(int(x) for x in os.environ.get("INSPECTORS", "").split())
    ENFORCERS = list(int(x) for x in os.environ.get("ENFORCERS", "").split())
    MONGO_DB_URL = os.environ.get("const MongoClient = require('mongodb').MongoClient;
const uri = "mongodb+srv://Arcanescanner:<Abhinavj@1234>@cluster0.va6iu.mongodb.net/Arcanescanner?retryWrites=true&w=majority";
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
client.connect(err => {
  const collection = client.db("test").collection("devices");
  // perform actions on the collection object
  client.close();
});")
    Sibyl_logs = int(os.environ.get("-1001317060675"))
    Sibyl_approved_logs = int(os.environ.get("-1001439418980"))
    GBAN_MSG_LOGS = int(os.environ.get("-1001342831787"))
    BOT_TOKEN = os.environ.get("1746986966:AAE8IImkwe5l_Txbah0u5GOLeRzuwhnKJMU")
else:
    import Sibyl_System.config as Config

    API_ID_KEY = Config.API_ID
    API_HASH_KEY = Config.API_HASH
    STRING_SESSION = Config.STRING_SESSION
    MONGO_DB_URL = Config.MONGO_DB_URL
    with open(os.path.join(os.getcwd(), "Sibyl_System\\elevated_users.json"), "r") as f:
        data = json.load(f)
    SIBYL = data["SIBYL"]
    ENFORCERS = data["ENFORCERS"]
    INSPECTORS = data["INSPECTORS"]
    Sibyl_logs = Config.Sibyl_logs
    Sibyl_approved_logs = Config.Sibyl_approved_logs
    GBAN_MSG_LOGS = Config.GBAN_MSG_LOGS
    BOT_TOKEN = Config.BOT_TOKEN

INSPECTORS.extend(SIBYL)
ENFORCERS.extend(INSPECTORS)

session = aiohttp.ClientSession()

MONGO_CLIENT = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URL)

from .client_class import SibylClient

System = SibylClient(StringSession(STRING_SESSION), API_ID_KEY, API_HASH_KEY)

collection = MONGO_CLIENT["Sibyl"]["Main"]


async def make_collections() -> str:
    if (
        await collection.count_documents({"_id": 1}, limit=1) == 0
    ):  # Blacklisted words list
        dictw = {"_id": 1}
        dictw["blacklisted"] = []
        await collection.insert_one(dictw)

    if (
        await collection.count_documents({"_id": 2}, limit=1) == 0
    ):  # Blacklisted words in name list
        dictw = {"_id": 2, "Type": "Wlc Blacklist"}
        dictw["blacklisted_wlc"] = []
        await collection.insert_one(dictw)
    if await collection.count_documents({"_id": 3}, limit=1) == 0:  # Gbanned users list
        dictw = {"_id": 3, "Type": "Gban:List"}
        dictw["victim"] = []
        dictw["gbanners"] = []
        dictw["reason"] = []
        dictw["proof_id"] = []
        await collection.insert_one(dictw)
    if await collection.count_documents({"_id": 4}, limit=1) == 0:  # Rank tree list
        sample_dict = {"_id": 4, "data": {}, "standalone": {}}
        sample_dict["data"] = {}
        for x in SIBYL:
            sample_dict["data"][str(x)] = {}
            sample_dict["standalone"][str(x)] = {
                "added_by": 777000,
                "timestamp": datetime.timestamp(datetime.now()),
            }
        await collection.insert_one(sample_dict)
    return ""


def system_cmd(
    pattern=None,
    allow_sibyl=True,
    allow_enforcer=False,
    allow_inspectors=False,
    allow_slash=True,
    force_reply=False,
    **args
):
    if pattern and allow_slash:
        args["pattern"] = re.compile(r"[\?\.!/]" + pattern)
    else:
        args["pattern"] = re.compile(r"[\?\.!]" + pattern)
    if allow_sibyl and allow_enforcer:
        args["from_users"] = ENFORCERS
    elif allow_inspectors and allow_sibyl:
        args["from_users"] = INSPECTORS
    else:
        args["from_users"] = SIBYL
    if force_reply:
        args["func"] = lambda e: e.is_reply
    return events.NewMessage(**args)
