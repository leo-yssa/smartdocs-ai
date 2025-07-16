package com.smartdocs.client

import io.grpc.ManagedChannel
import io.grpc.ManagedChannelBuilder
import smartdocs.RagServiceGrpc
import smartdocs.Smartdocs.UploadDocumentRequest
import smartdocs.Smartdocs.UploadDocumentResponse
import smartdocs.Smartdocs.SearchRequest
import smartdocs.Smartdocs.SearchResponse
import smartdocs.Smartdocs.AskRequest
import smartdocs.Smartdocs.AskResponse
import org.springframework.stereotype.Component

@Component
class RagGrpcClient {
    private val channel: ManagedChannel = ManagedChannelBuilder.forAddress("localhost", 50051)
        .usePlaintext()
        .build()
    private val stub: RagServiceGrpc.RagServiceBlockingStub = RagServiceGrpc.newBlockingStub(channel)

    fun uploadDocument(title: String, content: String): UploadDocumentResponse {
        val request = UploadDocumentRequest.newBuilder()
            .setTitle(title)
            .setContent(content)
            .build()
        return stub.uploadDocument(request)
    }

    fun search(query: String, topK: Int = 3): SearchResponse {
        val request = SearchRequest.newBuilder()
            .setQuery(query)
            .setTopK(topK)
            .build()
        return stub.search(request)
    }

    fun ask(question: String, topK: Int = 3): AskResponse {
        val request = AskRequest.newBuilder()
            .setQuestion(question)
            .setTopK(topK)
            .build()
        return stub.ask(request)
    }
} 