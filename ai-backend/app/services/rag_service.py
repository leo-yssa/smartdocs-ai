# RAG(Retrieval-Augmented Generation) 서비스 로직 예시

from app.services.embedding_service import embed_text
from app.services.vector_search_service import add_document_embedding, search_similar
from app.services.document_store import store
from app.services import llm_service

# 문서 업로드/색인
def upload_document(title: str, content: str) -> str:
    emb = embed_text(content)
    doc_id = store.add_document(title, content, emb)
    add_document_embedding(emb)
    return doc_id

# 검색 (유사 문서 ID, 제목 반환)
def search_documents(query: str, top_k: int = 3):
    emb = embed_text(query)
    doc_ids = search_similar(emb, top_k)
    docs = store.get_documents(doc_ids)
    return [(doc.id, doc.title) for doc in docs]

# RAG 질의응답 (검색 결과 본문을 LLM에 컨텍스트로 넣어 답변 생성)
def ask_question(question: str, top_k: int = 3):
    emb = embed_text(question)
    doc_ids = search_similar(emb, top_k)
    docs = store.get_documents(doc_ids)
    context = "\n".join([doc.content for doc in docs])
    answer = llm_service.ask_llm_with_context(question, context)
    return answer, [doc.content for doc in docs] 