
# 🎭 Pinokio Avatar Setup Guide
> Create AI-powered talking avatars using Open WebUI + F5-TTS + KDTalker

## 🔧 Installation Steps

1. **Download Components**  
   - Pinokio Computer (Windows)
   - AllTalk-TTSv2
   - KDTalker
   - Open WebUI

2. **Verify Setup**
   ✅ Ensure all components are working
   ✅ Configure F5 voice and KDTalker avatar image
   
## ⚙️ Configuration

### 🛠 Open WebUI Settings
1. Navigate to:  
   `Admin Panel > Settings > Audio`
   
2. Set TTS endpoint:
```python
http://localhost:7851/v1  # AllTalk server with F5-TTS
```

### 💡 Add Functionality
- Create new function named KDTalker in Admin Panel using:
```python
OpenWebUIAction.py  # Action code implementation
```

## 🎨 Avatar Creation Setup

1. **Prepare Files**
   - Download `KDtalkerGradio.py`
   - Place avatar image in same directory
   - Update audio file path to your AllTalkTTS temp directory (e.g., `c:\pinokio\api\alltalk-tts.git\app\outputs`)

2. **Verify Functionality**  
   ✅ Run script with:  
   ```bash
   python KDtalkerGradio.py
   ```
   ✅ Output video plays in default player

3. **Launch Server**
```bash
python server.py  # Must be run from same directory
```

## 🧪 Model Configuration

1. In Open WebUI Workspace:
   - Create new model
   - Enable KDTalker function (previously added)

## ▶️ Usage Instructions

1. Select `NewModel` in chat interface
2. After receiving LLM response, click **KDTalker** button under message to generate video avatar using your configured setup
 
---

> 💡 Tip: Make sure all services (Open WebUI, AllTalk-TTSv2, KDTalker) are running in the background before attempting model usage.
