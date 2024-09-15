package com.example.app

import okhttp3.*
import org.json.JSONObject
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.IOException
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody.Companion.toRequestBody

private val client = OkHttpClient()

suspend fun sendViewerRequest(channel: String, amount: String): String {
    val json = JSONObject().apply {
        put("channel", channel)
        put("amount", amount)
    }
    val requestBody = json.toString().toRequestBody("application/json".toMediaTypeOrNull())
    val request = Request.Builder()
        .url("https://marryjaneandthang.com/api/twitch/v1/view")
        .post(requestBody)
        .addHeader("Content-Type", "application/json")
        .build()

    return withContext(Dispatchers.IO) {
        try {
            val response = client.newBuilder()
                .callTimeout(120, java.util.concurrent.TimeUnit.SECONDS)
                .build()
                .newCall(request)
                .execute()

            val responseBody = response.body?.string()

            when (response.code) {
                200 -> {
                    responseBody?.let {
                        try {
                            val jsonResponse = JSONObject(it)
                            val successMessage = jsonResponse.optString("message", "Successfully sent viewers")
                            successMessage
                        } catch (e: Exception) {
                            "Error parsing response: ${e.message ?: "Unknown error"}"
                        }
                    } ?: "No response body"
                }
                400 -> {
                    "Bad Request: ${responseBody ?: "Invalid request"}"
                }
                403 -> {
                    "Forbidden: ${responseBody ?: "Access denied"}"
                }
                429 -> {
                    "Rate Limit Exceeded: ${responseBody ?: "Too many requests"}"
                }
                500 -> {
                    "Server Error: ${responseBody ?: "Something went wrong on the server"}"
                }
                else -> {
                    "Unexpected error: ${response.code}. Response: ${responseBody ?: "No response body"}"
                }
            }
        } catch (e: IOException) {
            "Network error: ${e.message ?: "Unknown network error"}"
        }
    }
}
