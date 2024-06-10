import os
import time

import openai
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


client = OpenAI()

file = client.files.create(
    file=open("world_happiness.csv", "rb"), purpose="assistants"
)

assistant = client.beta.assistants.create(
    name="Data visualizer",
    description="You are great at creating beautiful data visualizations. You analyze data present in .csv files, understand trends, and come up with data visualizations relevant to those trends. You also share a brief text summary of the trends observed.",
    model="gpt-4o",
    tools=[{"type": "code_interpreter"}],
    tool_resources={"code_interpreter": {"file_ids": [file.id]}},
)

thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": "Create 3 data visualizations using two columns or more based on the trends in this file.",
            "attachments": [
                {"file_id": file.id, "tools": [{"type": "code_interpreter"}]}
            ],
        }
    ]
)

run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
print(f"👉 Run Created: {run.id}")

while run.status != "completed":
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    print(f"🏃🏻 Run Status: {run.status}")
    time.sleep(1)
else:
    print("🏁 Run Completed!")

message_response = client.beta.threads.messages.list(thread_id=thread.id)


image_data = client.files.content(
    message_response.data[0].content[0].image_file.file_id
)
image_data_bytes = image_data.read()

with open("my-image.png", "wb") as file:
    file.write(image_data_bytes)


image = Image.open("my-image.png")
image.show()
