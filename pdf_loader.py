from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=10,
    separators=[
        "\n",
        ". ",
        ", "],
    is_separator_regex=False,
)

all_docs_lst=[]
def load_information(data):
    loader = PyMuPDFLoader(data)
    docs = loader.load()
    c=1
    for i in docs:
        texts = text_splitter.create_documents([i.page_content])
       
        for j in texts:
            data=Document(
                page_content=j.page_content,
                metadata={"page_number":c}
            )
            all_docs_lst.append(data)
        c+=1
    return all_docs_lst

# load_information(r"C:\Users\saisa\OneDrive\Desktop\Java Tutorial_ Learn Java Programming.pdf")

# print(texts[0])
# print(texts[1])