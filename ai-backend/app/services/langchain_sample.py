from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os

# 환경변수에서 OpenAI API 키 불러오기 (필요시 .env 사용)
openai_api_key = os.getenv("OPENAI_API_KEY")

# 1. 문서 로딩 (PDF, TXT 등)
def load_documents(file_path: str):
    if file_path.lower().endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding="utf-8")
    return loader.load()

# 2. 텍스트 분할 (chunk 단위)
def split_documents(documents, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)

# 3. 임베딩 및 벡터스토어 저장
def embed_and_store(docs, persist_path=None):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_documents(docs, embeddings)
    if persist_path:
        vectorstore.save_local(persist_path)
    return vectorstore

# 4. 샘플 실행 함수
def run_sample(file_path: str, persist_path: str = None):
    print(f"[1] 문서 로딩: {file_path}")
    documents = load_documents(file_path)
    print(f"[2] 문서 분할: {len(documents)}개 → ", end="")
    docs = split_documents(documents)
    print(f"{len(docs)}개 chunk")
    print(f"[3] 임베딩 및 벡터스토어 저장...")
    vectorstore = embed_and_store(docs, persist_path)
    print(f"[완료] 벡터스토어에 {len(docs)}개 chunk 저장됨.")
    return vectorstore

# 사용 예시 (직접 실행 시)
if __name__ == "__main__":
    # 예시: sample.pdf 또는 sample.txt 파일 경로 지정
    sample_file = "sample.pdf"  # 또는 "sample.txt"
    persist_dir = "faiss_index"
    run_sample(sample_file, persist_dir) 