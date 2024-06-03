import os
import shutil
import sys

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings

CHROMA_PATH = "chroma"
DATA_PATH = "data/books"


def main():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents():
    if len(sys.argv) != 2:
        sys.exit("Usage: python project.py file.pdf")

    pdf_file = sys.argv[1]
    loader = DirectoryLoader(DATA_PATH, glob=pdf_file)
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[10]
    print(document.page_content)
    print(document.metadata)

    return chunks


def save_to_chroma(chunks: list[Document]):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )
    db.persist()


if __name__ == "__main__":
    main()
