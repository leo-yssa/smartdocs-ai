package com.smartdocs.controller

import com.smartdocs.client.RagGrpcClient
import org.springframework.web.bind.annotation.*

@RestController
class GrpcTestController(
    private val ragGrpcClient: RagGrpcClient
) {
    @PostMapping("/grpc/upload")
    fun upload(@RequestParam title: String, @RequestParam content: String): Map<String, String> {
        val resp = ragGrpcClient.uploadDocument(title, content)
        return mapOf(
            "documentId" to resp.documentId,
            "message" to resp.message
        )
    }

    @GetMapping("/grpc/search")
    fun search(@RequestParam query: String, @RequestParam(required = false, defaultValue = "3") topK: Int): Map<String, Any> {
        val resp = ragGrpcClient.search(query, topK)
        return mapOf(
            "documentIds" to resp.documentIdsList,
            "titles" to resp.titlesList
        )
    }

    @GetMapping("/grpc/ask")
    fun ask(@RequestParam question: String, @RequestParam(required = false, defaultValue = "3") topK: Int): Map<String, Any> {
        val resp = ragGrpcClient.ask(question, topK)
        return mapOf(
            "answer" to resp.answer,
            "contextDocuments" to resp.contextDocumentsList
        )
    }
} 