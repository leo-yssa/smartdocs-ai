import faiss
import numpy as np
from app.services.document_store import store

# all-MiniLM-L6-v2 임베딩 차원
index = faiss.IndexFlatL2(384)

# 문서 임베딩 추가 (문서 저장소와 연동)
def add_document_embedding(embedding: np.ndarray):
    index.add(np.array([embedding]).astype('float32'))

# 쿼리 임베딩으로 유사 문서 ID 반환
def search_similar(embedding: np.ndarray, top_k=3):
    if index.ntotal == 0:
        return []
    D, I = index.search(np.array([embedding]).astype('float32'), top_k)
    id_list = store.all_ids()
    # FAISS 인덱스와 문서 ID 매핑
    return [id_list[i] for i in I[0] if 0 <= i < len(id_list)]

# 샘플 문서 임베딩 추가 함수
def add_sample_documents():
    from app.services.embedding_service import embed_text
    docs = ["Hello world", "SmartDocs AI", "Document search example"]
    for doc in docs:
        emb = embed_text(doc)
        add_document_embedding(emb) 