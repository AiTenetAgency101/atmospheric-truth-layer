# OBS YouTube Streaming Setup for AiTenet Weather Stream

## Quick Start

### 1. Install Node.js Dependencies
```powershell
cd C:\AiTenet\weather-stream
npm install
```

### 2. Configure Weather API (Optional)
Edit `.env`:
```
OPENWEATHER_API_KEY=your_key_here  # Get free key from openweathermap.org
LOCATION=Sydney  # Your city
PORT=9099
```

Without an API key, the server runs in stub mode (simulated data).

### 3. Start the Weather Stream Server
```powershell
npm start
```

You'll see:
```
🌍 AiTenet Weather Stream running on http://localhost:9099
📡 API endpoint: http://localhost:9099/stream/weather
🎬 Overlay URL for OBS: http://localhost:9099/
```

### 4. Set Up OBS

#### Add Browser Source
1. OBS → Sources → + (Add) → Browser
2. URL: `http://localhost:9099/`
3. Width: 1920, Height: 1080 (or your stream resolution)
4. Check "Shutdown source when not visible"

#### Stream to YouTube
1. OBS → Settings → Stream
2. Service: YouTube - RTMP
3. Paste your YouTube stream key (you provided it)
4. Click "Test Stream" to verify
5. Click "Start Streaming"

#### Optional: Add Webcam or Desktop
- Add your camera/desktop as a second source
- Position the weather overlay as corner/overlay

### 5. Go Live
- In OBS: File → Start Streaming
- Check your YouTube Studio to confirm broadcast is live
- Monitor the weather metrics updating every 5 seconds

## Troubleshooting

**Browser source shows "Loading..."?**
- Verify `npm start` is running
- Check firewall allows localhost:9099
- Refresh OBS source (right-click → Refresh)

**No weather data appearing?**
- Check console output from `npm start`
- Verify `.env` file has correct API key (if using real data)
- In stub mode, data generates automatically

**OBS won't stream to YouTube?**
- Double-check stream key in Settings
- Test with YouTube Studio's "Check encoder" button
- Verify internet connection is stable

## Data Sources

- **With API Key**: Real data from OpenWeatherMap (satellite-informed)
- **Without API Key**: Simulated data that updates every 30 seconds
- Updates refresh every 5 seconds on the overlay

Enjoy your live weather stream!
