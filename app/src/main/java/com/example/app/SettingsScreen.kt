package com.example.app

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.foundation.background
@Composable
fun SettingsScreen() {
    var sliderValue by remember { mutableStateOf(0f) }
    var switchChecked by remember { mutableStateOf(false) }

    val backgroundColor = Color(
        red = (255 * (1 - sliderValue / 100)).toInt(),
        green = (255 * (1 - sliderValue / 100)).toInt(),
        blue = (255 * (1 - sliderValue / 100)).toInt()
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
            .background(backgroundColor),  
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = "Settings (JUST A TEST)",
            style = MaterialTheme.typography.headlineMedium,
            color = Color(0xFF007BFF),
            modifier = Modifier.padding(bottom = 16.dp)
        )

        
        Text(text = "Slider Value: ${sliderValue.toInt()}", modifier = Modifier.padding(bottom = 16.dp))
        Slider(
            value = sliderValue,
            onValueChange = { sliderValue = it },
            valueRange = 0f..100f,
            modifier = Modifier.padding(bottom = 24.dp)
        )

        
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.padding(bottom = 24.dp)
        ) {
            Text(text = "Enable Feature", modifier = Modifier.padding(end = 16.dp))
            Switch(
                checked = switchChecked,
                onCheckedChange = { switchChecked = it }
            )
        }

        
        Button(onClick = { /*  */ }, modifier = Modifier.padding(bottom = 16.dp)) {
            Text("Test Button 1")
        }
        Button(onClick = { /*  */ }) {
            Text("Test Button 2")
        }
    }
}
