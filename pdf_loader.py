from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter



def Pdf_Reader(path):
    docs = []
    
    loader = [PyPDFLoader(path)]
    for file in loader:
        docs.extend(file.load())
    
    splitter = RecursiveCharacterTextSplitter(chunk_size = 10000, chunk_overlap = 100)
    documents = splitter.split_documents(docs)

    return documents
