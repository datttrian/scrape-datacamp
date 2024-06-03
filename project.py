import sys
from langchain_community.document_loaders import DirectoryLoader


DATA_PATH = "data/books"


def main():
    documents = load_documents()
    print(documents)


def load_documents():
    if len(sys.argv) != 2:
        sys.exit("Usage: python project.py file.pdf")

    pdf_file = sys.argv[1]
    loader = DirectoryLoader(DATA_PATH, glob=pdf_file)
    documents = loader.load()
    return documents


if __name__ == "__main__":
    main()
