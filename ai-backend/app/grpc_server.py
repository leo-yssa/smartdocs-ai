import grpc
from concurrent import futures
from app import smartdocs_pb2, smartdocs_pb2_grpc
from app.services import rag_service
from app.services import llm_service
from dotenv import load_dotenv
load_dotenv()

class RagServiceServicer(smartdocs_pb2_grpc.RagServiceServicer):
    def UploadDocument(self, request, context):
        print(f"UploadDocument called: {request.title}, {request.content}")
        doc_id = rag_service.upload_document(request.title, request.content)
        return smartdocs_pb2.UploadDocumentResponse(document_id=doc_id, message="Document uploaded and indexed.")

    def Search(self, request, context):
        print(f"Search called with query: {request.query}")
        results = rag_service.search_documents(request.query, request.top_k or 3)
        doc_ids = [doc_id for doc_id, _ in results]
        titles = [title for _, title in results]
        return smartdocs_pb2.SearchResponse(document_ids=doc_ids, titles=titles)

    def Ask(self, request, context):
        print(f"Ask called with question: {request.question}")
        try:
            answer, context_docs = rag_service.ask_question(request.question, request.top_k or 3)
        except Exception as e:
            print(f"LLM error: {e}")
            answer = f"Error: {e}"
            context_docs = []
        return smartdocs_pb2.AskResponse(answer=answer, context_documents=context_docs)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    smartdocs_pb2_grpc.add_RagServiceServicer_to_server(RagServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve() 