import getpass
import os

def vector_creation(file):
    if not os.environ.get("COHERE_API_KEY"):
        os.environ["COHERE_API_KEY"] = "1oemmq68XtQlDNZvtbT2KieE6HoDPNIWdiI7xn2f"

    from langchain_cohere import CohereEmbeddings

    embeddings = CohereEmbeddings(model="embed-english-v3.0")
    import faiss
    from langchain_community.docstore.in_memory import InMemoryDocstore
    from langchain_community.vectorstores import FAISS

    index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))
    print(index)
    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )

    from uuid import uuid4

    from pdf_loader import load_information

    documents=load_information(file)
    # print("1")
    print(len(documents))
    uuids = [str(uuid4()) for _ in range(len(documents))]
    print(uuids)
    vector_store.add_documents(documents=documents, ids=uuids)

    return vector_store

    # print(vector_store.delete(ids=[uuids[-1]]))

    # results = vector_store.similarity_search(
    #     "What is java",
    #     k=2,

    # )
    # print(results)
    # context=""
    # for res in results:
    #     print(f"* {res.page_content} [{res.metadata}]")
    #     context+=f"* {res.page_content} \n[{res.metadata}\n\n"
    # return context