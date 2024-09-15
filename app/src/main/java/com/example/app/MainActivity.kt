package com.example.app
import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import kotlinx.coroutines.delay
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.platform.LocalContext
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.ui.text.input.KeyboardType
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody.Companion.toRequestBody
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import okhttp3.*
import org.json.JSONObject
import java.io.IOException
import androidx.core.content.ContextCompat
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Settings
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.material3.OutlinedTextField
import android.content.Intent
import android.content.Context
import org.json.JSONArray
import androidx.lifecycle.lifecycleScope
import android.net.Uri
private const val TAG = "LoginScreen"
private val client = OkHttpClient()



class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        val currentVersion = "2.0"
        lifecycleScope.launch {

            val updateAvailable = checkForUpdate(currentVersion, this@MainActivity)
            if (updateAvailable) {
                // If update is available, the user will be redirected and won't be able to use the app
                return@launch
            }

            setContent {
                MaterialTheme {
                    NavHostSetup()
                }
            }

            val intent = Intent(this@MainActivity, NotificationService::class.java)
            ContextCompat.startForegroundService(this@MainActivity, intent)
        }
    }
}

@Composable
fun LoginScreen(navController: NavHostController, onLoginSuccess: () -> Unit) {
    val coroutineScope = rememberCoroutineScope()
    var password by remember { mutableStateOf("") }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var isLoggedIn by remember { mutableStateOf(false) }
    val context = LocalContext.current

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
            .background(color = Color(0xFFF4F4F4)),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = "Login",
            style = MaterialTheme.typography.headlineMedium,
            color = Color(0xFF007BFF),
            modifier = Modifier.padding(bottom = 16.dp)
        )
        OutlinedTextField(
            value = password,
            onValueChange = { password = it },
            label = { Text("Password") },
            modifier = Modifier.fillMaxWidth(),
            visualTransformation = PasswordVisualTransformation()
        )
        Spacer(modifier = Modifier.height(16.dp))
        Button(
            onClick = {
                coroutineScope.launch {
                    try {
                        val loginSuccessful = handleLogin(navController, password) { message ->
                            errorMessage = message
                        }
                        if (loginSuccessful) {
                            onLoginSuccess()
                        } else {
                            isLoggedIn = false
                        }
                    } catch (e: Exception) {
                        Log.e(TAG, "Error during login", e)
                        errorMessage = "Error during login: ${e.message}"
                    }
                }
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Login")
        }
        Spacer(modifier = Modifier.height(16.dp))
        Button(
            onClick = {
                val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://discord.gg/kws47CDsd8"))
                context.startActivity(intent)
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Join our Discord")
        }
        errorMessage?.let {
            Spacer(modifier = Modifier.height(16.dp))
            Text(
                text = it,
                color = Color.Red,
                style = MaterialTheme.typography.bodyMedium
            )
        }
    }
}




suspend fun handleLogin(
    navController: NavHostController,
    password: String,
    onError: (String) -> Unit
): Boolean {
    val requestBody = FormBody.Builder()
        .add("password", password)
        .build()
    val request = Request.Builder()
        .url("https://marryjaneandthang.com/tvbotlogin")
        .post(requestBody)
        .addHeader("Content-Type", "application/x-www-form-urlencoded")
        .build()

    return try {
        withContext(Dispatchers.IO) {
            client.newCall(request).execute().use { response ->
                val responseBody = response.body?.string() ?: ""
                Log.d(TAG, "Response Code: ${response.code}")
                Log.d(TAG, "Response Body: $responseBody")
                withContext(Dispatchers.Main) {
                    when (response.code) {
                        200 -> {
                            Log.d(TAG, "Login successful")
                            navController.navigate("home")
                            true
                        }
                        400 -> {
                            val jsonResponse = JSONObject(responseBody)
                            val message = jsonResponse.optString("message", "Unknown error")
                            onError(message)
                            false
                        }
                        else -> {
                            onError("An unexpected error occurred. Code: ${response.code}, Body: $responseBody")
                            false
                        }
                    }
                }
            }
        }
    } catch (e: IOException) {
        Log.e(TAG, "Network error: ${e.message}", e)
        withContext(Dispatchers.Main) {
            onError("Network error: ${e.message ?: "Unknown error"}")
        }
        false
    } catch (e: Exception) {
        Log.e(TAG, "Unexpected error: ${e.message}", e)
        withContext(Dispatchers.Main) {
            onError("Unexpected error: ${e.message ?: "Unknown error"}")
        }
        false
    }
}

@Composable
fun NavHostSetup() {
    val navController = rememberNavController()
    var isLoggedIn by remember { mutableStateOf(false) }

    Scaffold(
        bottomBar = { CustomBottomNavBar(navController) }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = if (isLoggedIn) "home" else "login",
            Modifier.padding(innerPadding)
        ) {
            composable("login") {
                LoginScreen(
                    navController = navController,
                    onLoginSuccess = { isLoggedIn = true }
                )
            }
            composable("home") {
                MainScreen(isLoggedIn)
            }
            composable("settings") {
                SettingsScreen()
            }
        }
    }
}



@Composable
fun CustomBottomNavBar(navController: NavHostController) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
            .height(56.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        IconButton(onClick = { navController.navigate("home") }) {
            Icon(Icons.Filled.Home, contentDescription = "Home")
        }
        IconButton(onClick = { navController.navigate("settings") }) {
            Icon(Icons.Filled.Settings, contentDescription = "Settings")
        }
    }
}

@Composable
fun MainScreen(isLoggedIn: Boolean, modifier: Modifier = Modifier) {
    val context = LocalContext.current
    val coroutineScope = rememberCoroutineScope()

    var channel by remember { mutableStateOf("") }
    var amount by remember { mutableStateOf("") }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var successMessage by remember { mutableStateOf<String?>(null) }
    var isButtonEnabled by remember { mutableStateOf(true) }
    var lastButtonClickTime by remember { mutableStateOf(0L) }
    var countdownTime by remember { mutableStateOf(0) }
    var recentChannels by remember { mutableStateOf<List<Pair<String, String>>>(emptyList()) }

    val clearRecentChannelsHandler: () -> Unit = {
        coroutineScope.launch {
            clearRecentChannels(context)
            recentChannels = loadRecentChannels(context)
        }
    }
    LaunchedEffect(Unit) {
        recentChannels = loadRecentChannels(context)
    }
    val currentTime = System.currentTimeMillis()
    val cooldownElapsed = (currentTime - lastButtonClickTime) >= 60 * 1000
    LaunchedEffect(isButtonEnabled) {
        if (!isButtonEnabled) {
            countdownTime = ((60 * 1000 - (currentTime - lastButtonClickTime)) / 1000).toInt()
            while (countdownTime > 0) {
                delay(1000)
                countdownTime--
            }
            isButtonEnabled = true
        }
    }

    if (!isLoggedIn) {
        Column(
            modifier = modifier
                .fillMaxSize()
                .padding(16.dp)
                .background(color = Color(0xFFF4F4F4)),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "Login to continue\n\nJoin the discord for the password",
                style = MaterialTheme.typography.headlineMedium,
                color = Color.Red
            )
            Button(
                onClick = {
                    val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://discord.gg/kws47CDsd8"))
                    context.startActivity(intent)
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Discord")
            }
            Text(
                text = "After you get the password restart the app to login",
                style = MaterialTheme.typography.headlineMedium,
                color = Color.Black
            )
        }
    } else {
        Column(
            modifier = modifier
                .fillMaxSize()
                .padding(16.dp)
                .background(color = Color(0xFFF4F4F4)),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "Twitch Live View Bot",
                style = MaterialTheme.typography.headlineLarge,
                color = Color(0xFF007BFF),
                modifier = Modifier.padding(bottom = 24.dp)
            )

            OutlinedTextField(
                value = channel,
                onValueChange = { channel = it },
                label = { Text("Channel") },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 32.dp)
            )

            Spacer(modifier = Modifier.height(16.dp))

            OutlinedTextField(
                value = amount,
                onValueChange = { amount = it },
                label = { Text("Amount") },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 32.dp),
                keyboardOptions = KeyboardOptions.Default.copy(keyboardType = KeyboardType.Number)
            )

            Spacer(modifier = Modifier.height(24.dp))

            Button(
                onClick = {
                    coroutineScope.launch {
                        try {
                            if (cooldownElapsed) {
                                val response = sendViewerRequest(channel, amount)
                                successMessage = response
                                errorMessage = null
                                lastButtonClickTime = System.currentTimeMillis()
                                isButtonEnabled = false
                                val updatedChannels = recentChannels.toMutableSet().apply {
                                    add(Pair(channel, amount))
                                }.toList()
                                saveRecentChannels(context, updatedChannels)
                                recentChannels = updatedChannels
                            } else {
                                errorMessage = "Please wait before sending more viewers."
                                successMessage = null
                            }
                        } catch (e: Exception) {
                            errorMessage = e.message
                            successMessage = null
                        }
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 32.dp),
                enabled = isButtonEnabled
            ) {
                Text("Send Viewers")
            }

            successMessage?.let {
                Spacer(modifier = Modifier.height(24.dp))
                Text(
                    text = it,
                    color = Color.Green,
                    style = MaterialTheme.typography.bodyMedium
                )
            }

            errorMessage?.let {
                Spacer(modifier = Modifier.height(24.dp))
                Text(
                    text = it,
                    color = Color.Red,
                    style = MaterialTheme.typography.bodyMedium
                )
            }
            Spacer(modifier = Modifier.height(24.dp))
            Text("Recent Channels:", style = MaterialTheme.typography.headlineMedium)

            LazyColumn {
                items(recentChannels) { (recentChannel, sentAmount) ->
                    Text(
                        text = "$recentChannel - Viewers Sent: $sentAmount",
                        style = MaterialTheme.typography.bodyMedium,
                        modifier = Modifier.padding(vertical = 4.dp)
                    )
                }
            }

            Spacer(modifier = Modifier.height(24.dp))
            Button(
                onClick = clearRecentChannelsHandler,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 32.dp)
            ) {
                Text("Clear Recent Channels")
            }
        }
    }
}

fun loadRecentChannels(context: Context): List<Pair<String, String>> {
    return try {
        val json = context.openFileInput("recent.json").bufferedReader().use { it.readText() }
        val jsonArray = JSONArray(json)
        (0 until jsonArray.length()).map {
            val jsonObject = jsonArray.getJSONObject(it)
            Pair(jsonObject.getString("channel"), jsonObject.getString("amount"))
        }.distinct()
    } catch (e: Exception) {
        emptyList()
    }
}

fun saveRecentChannels(context: Context, channels: List<Pair<String, String>>) {
    try {
        val jsonArray = JSONArray()
        channels.forEach { (channel, amount) ->
            val jsonObject = JSONObject().apply {
                put("channel", channel)
                put("amount", amount)
            }
            jsonArray.put(jsonObject)
        }
        context.openFileOutput("recent.json", Context.MODE_PRIVATE).use { output ->
            output.write(jsonArray.toString().toByteArray())
        }
    } catch (e: Exception) {
        //pp
    }
}

fun clearRecentChannels(context: Context) {
    try {
        context.openFileOutput("recent.json", Context.MODE_PRIVATE).use { output ->
            output.write("[]".toByteArray())
        }
    } catch (e: Exception) {
        //pp
    }
}




@Preview(showBackground = true)
@Composable
fun PreviewApp() {
    MaterialTheme {
        NavHostSetup()
    }
}
