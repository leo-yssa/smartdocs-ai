import uuid
from typing import Dict, List

class Document:
    def __init__(self, title: str, content: str, embedding):
        self.id = str(uuid.uuid4())
        self.title = title
        self.content = content
        self.embedding = embedding

class DocumentStore:
    def __init__(self):
        self.documents: Dict[str, Document] = {}
        self.id_list: List[str] = []

    def add_document(self, title: str, content: str, embedding) -> str:
        doc = Document(title, content, embedding)
        self.documents[doc.id] = doc
        self.id_list.append(doc.id)
        return doc.id

    def get_document(self, doc_id: str) -> Document:
        return self.documents.get(doc_id)

    def get_documents(self, doc_ids: List[str]) -> List[Document]:
        return [self.documents[doc_id] for doc_id in doc_ids if doc_id in self.documents]

    def all_embeddings(self):
        return [self.documents[doc_id].embedding for doc_id in self.id_list]

    def all_ids(self):
        return self.id_list

# 싱글턴 인스턴스
store = DocumentStore() 