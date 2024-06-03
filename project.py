from langchain.document_loaders import DirectoryLoader


DATA_PATH = "data/books"


def main():
    documents = load_documents()
    print(documents)


def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.pdf")
    documents = loader.load()
    return documents


if __name__ == "__main__":
    main()
