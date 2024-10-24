from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
adminlist = os.getenv('adminlist').split(",")
api_id = int(os.getenv('api_id'))
api_hash = os.getenv('api_hash')
proxy = os.getenv('proxy')
