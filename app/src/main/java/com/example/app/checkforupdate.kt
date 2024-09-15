    package com.example.app

    import android.content.Context
    import android.content.Intent
    import android.net.Uri
    import okhttp3.OkHttpClient
    import okhttp3.Request
    import kotlinx.coroutines.Dispatchers
    import kotlinx.coroutines.withContext
    import org.json.JSONObject
    import java.io.IOException

    private const val VERSION_URL = "https://marryjaneandthang.com/get_version"
    private val client = OkHttpClient()

    suspend fun checkForUpdate(currentVersion: String, context: Context): Boolean {
        return try {
            val request = Request.Builder()
                .url(VERSION_URL)
                .build()
            withContext(Dispatchers.IO) {
                client.newCall(request).execute().use { response ->
                    if (response.isSuccessful) {
                        val responseBody = response.body?.string()
                        val jsonResponse = JSONObject(responseBody ?: "{}")
                        val latestVersion = jsonResponse.optString("message", "0.0")
                        if (latestVersion != currentVersion) {
                            openUpdateUrl(context)
                            true
                        } else {
                            false
                        }
                    } else {
                        false
                    }
                }
            }
        } catch (e: IOException) {
            false
        }
    }

    private fun openUpdateUrl(context: Context) {
        val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://discord.gg/kws47CDsd8"))
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK)
        context.startActivity(intent)
    }
