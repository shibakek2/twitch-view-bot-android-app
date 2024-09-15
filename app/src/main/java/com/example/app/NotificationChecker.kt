package com.example.app

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Intent
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import kotlinx.coroutines.*
import org.json.JSONArray
import java.net.HttpURLConnection
import java.net.URL

private const val CHANNEL_ID = "notifications_channel"
private const val CHANNEL_NAME = "Notifications"
private const val CHANNEL_DESCRIPTION = "Channel for notifications"
private const val NOTIFICATION_ID = 1

class NotificationService : Service() {

    private var lastMessage: String? = null
    private lateinit var notificationBuilder: NotificationCompat.Builder

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        notificationBuilder = NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle("Shiba Views V2.0")
            .setContentText("Checking for notifications...")
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setOngoing(true)
            .setVibrate(longArrayOf(1000, 1000))
            .setSound(android.provider.Settings.System.DEFAULT_NOTIFICATION_URI)

        startForeground(NOTIFICATION_ID, notificationBuilder.build())
        startChecking()
    }

    override fun onBind(intent: Intent?): IBinder? {
        return null
    }

    private fun startChecking() {
        CoroutineScope(Dispatchers.IO).launch {
            while (true) {
                val notifications = fetchNotifications()
                if (notifications != null) {
                    handleNotifications(notifications)
                }
                delay(10_000) // Check every 10 seconds
            }
        }
    }

    private suspend fun fetchNotifications(): JSONArray? {
        return withContext(Dispatchers.IO) {
            try {
                val url = URL("https://marryjaneandthang.com/get_notifications")
                val connection = url.openConnection() as HttpURLConnection
                connection.requestMethod = "GET"
                val responseCode = connection.responseCode

                if (responseCode == HttpURLConnection.HTTP_OK) {
                    val response = connection.inputStream.bufferedReader().use { it.readText() }
                    JSONArray(response)
                } else {
                    null
                }
            } catch (e: Exception) {
                e.printStackTrace() // Log the exception for debugging
                null
            }
        }
    }

    private fun handleNotifications(notifications: JSONArray) {
        if (notifications.length() > 0) {
            for (i in 0 until notifications.length()) {
                val newNotification = notifications.getJSONObject(i)
                val message = newNotification.optString("message")

                if (message != lastMessage) {
                    sendNotification(message)
                    lastMessage = message

                    // Update the foreground notification with the latest message
                    updateForegroundNotification(message)
                }
            }
        }
    }

    private fun sendNotification(message: String) {
        val notificationBuilder = NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle("New Notification")
            .setContentText(message)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setVibrate(longArrayOf(1000, 1000))
            .setSound(android.provider.Settings.System.DEFAULT_NOTIFICATION_URI)
            .setAutoCancel(true)

        with(NotificationManagerCompat.from(this)) {
            notify(NOTIFICATION_ID, notificationBuilder.build())
        }
    }

    private fun updateForegroundNotification(message: String) {
        val updatedNotification = notificationBuilder
            .setContentText(message)
            .build()

        startForeground(NOTIFICATION_ID, updatedNotification)
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                CHANNEL_NAME,
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = CHANNEL_DESCRIPTION
            }

            val notificationManager = getSystemService(NotificationManager::class.java)
            notificationManager.createNotificationChannel(channel)
        }
    }
}
