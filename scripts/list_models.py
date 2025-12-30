from openai import OpenAI
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))
models = client.models.list()

for m in models.data:
    print(m.id)
    
print("---------------------")
client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),  # This is the default and can be omitted
)
page = client.models.list()
for i in page.data:
    print(i.id)
