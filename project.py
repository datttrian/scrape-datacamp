import os
import time
import openai
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()


def upload_file(file_path):
    return client.files.create(file=open(file_path, "rb"), purpose="assistants")


def create_assistant(name, description, file_id):
    return client.beta.assistants.create(
        name=name,
        description=description,
        model="gpt-4o",
        tools=[{"type": "code_interpreter"}],
        tool_resources={"code_interpreter": {"file_ids": [file_id]}},
    )


def run_assistant(thread_id, assistant_id):
    run = client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id
    )
    print(f"👉 Run Created: {run.id}")
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        print(f"🏃🏻 Run Status: {run.status}")
        time.sleep(1)
    print("🏁 Run Completed!")
    return run


def get_message_response(thread_id):
    return client.beta.threads.messages.list(thread_id=thread_id)


def save_image(image_data, output_path):
    image_data_bytes = image_data.read()
    with open(output_path, "wb") as file:
        file.write(image_data_bytes)
    image = Image.open(output_path)
    image.show()


def impute_data(file_id):
    assistant = create_assistant(
        name="Data Imputer",
        description="You are excellent at handling missing data. You analyze .csv files for missing values and impute them appropriately.",
        file_id=file_id,
    )
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "Impute any missing data in this file.",
                "attachments": [
                    {"file_id": file_id, "tools": [{"type": "code_interpreter"}]}
                ],
            }
        ]
    )
    run_assistant(thread.id, assistant.id)
    return get_message_response(thread.id)


def visualize_data(file_id):
    assistant = create_assistant(
        name="Data Visualizer",
        description="You are great at creating beautiful data visualizations. You analyze data present in .csv files, understand trends, and come up with data visualizations relevant to those trends. You also share a brief text summary of the trends observed.",
        file_id=file_id,
    )
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "Create 3 data visualizations using two columns or more based on the trends in this file.",
                "attachments": [
                    {"file_id": file_id, "tools": [{"type": "code_interpreter"}]}
                ],
            }
        ]
    )
    run_assistant(thread.id, assistant.id)
    return get_message_response(thread.id)


def feature_engineer_data(file_id):
    assistant = create_assistant(
        name="Feature Engineer",
        description="You excel at creating new features from existing data. You analyze .csv files and generate new, meaningful features that can improve the performance of machine learning models.",
        file_id=file_id,
    )
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "Engineer new features from the data in this file.",
                "attachments": [
                    {"file_id": file_id, "tools": [{"type": "code_interpreter"}]}
                ],
            }
        ]
    )
    run_assistant(thread.id, assistant.id)
    return get_message_response(thread.id)


def perform_unsupervised_learning(file_id):
    assistant = create_assistant(
        name="Unsupervised Learner",
        description="You are skilled at unsupervised learning techniques. You analyze .csv files and perform clustering or other unsupervised learning tasks to find patterns in the data.",
        file_id=file_id,
    )
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "Perform unsupervised learning on this file and identify clusters or patterns.",
                "attachments": [
                    {"file_id": file_id, "tools": [{"type": "code_interpreter"}]}
                ],
            }
        ]
    )
    run_assistant(thread.id, assistant.id)
    return get_message_response(thread.id)


def main():
    file = upload_file("world_happiness.csv")

    impute_data(file.id)
    visualize_response = visualize_data(file.id)
    feature_engineer_data(file.id)
    unsupervised_learning_response = perform_unsupervised_learning(file.id)

    image_data = client.files.content(
        visualize_response.data[0].content[0].image_file.file_id
    )
    save_image(image_data, "my-image.png")

    print("Unsupervised Learning Response: ", unsupervised_learning_response.data)


if __name__ == "__main__":
    main()
