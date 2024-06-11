import os

import openai
from dotenv import load_dotenv
from openai import OpenAI

from langchain_community.utilities import SQLDatabase

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()


db = SQLDatabase.from_uri("sqlite:///Chinook.db")
print(db.dialect)
print(db.get_usable_table_names())
db.run("SELECT * FROM Artist LIMIT 10;")
