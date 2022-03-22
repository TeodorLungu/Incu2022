import requests
import os
from dotenv import load_dotenv

config = load_dotenv(".env")

roomId = os.getenv("ROOM_ID")
token = os.getenv("TOKEN_API")

url = "https://webexapis.com/v1/messages?roomId=" + roomId

header = {"content-type": "application/json; charset=utf-8",
          "authorization": "Bearer " + token}

response = requests.get(url, headers = header, verify = True)

print(response.json())
