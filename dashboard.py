target_text = st.text_area(
        "Input Text Stream for Analysis:", 
        value=default_val, 
        placeholder=chosen_placeholder,
        height=120
    )

    # Dedicated Speech-to-Text Voice Toolbar right beneath the text box
    voice_component_html = f"""
    <div style="display: flex; align-items: center; gap: 10px; margin-top: -5px; margin-bottom: 10px; font-family: sans-serif;">
        <button id="record-btn" style="
            background: {btn_bg}; 
            color: #ffffff; 
            border: none; 
            padding: 6px 14px; 
            border-radius: 16px; 
            font-weight: bold; 
            cursor: pointer; 
            display: flex; 
            align-items: center; 
            gap: 6px;
            font-size: 0.8rem;
        ">
            <span id="mic-icon">🎙️</span> <span id="btn-text">Tap to Speak Input</span>
        </button>
        <span id="status-text" style="font-size: 0.780rem; color: {title_color}; font-style: italic;"></span>
    </div>

    <script>
        const btn = document.getElementById('record-btn');
        const btnText = document.getElementById('btn-text');
        const micIcon = document.getElementById('mic-icon');
        const statusText = document.getElementById('status-text');

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {{
            btn.style.display = 'none';
            statusText.innerText = 'Speech-to-text not supported in this browser.';
        }} else {{
            const recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';

            let isRecording = false;

            btn.onclick = () => {{
                if (!isRecording) {{
                    recognition.start();
                    isRecording = true;
                    btnText.innerText = 'Listening... Speak now';
                    micIcon.innerText = '🔴';
                    statusText.innerText = 'Recording...';
                }} else {{
                    recognition.stop();
                    isRecording = false;
                    btnText.innerText = 'Tap to Speak Input';
                    micIcon.innerText = '🎙️';
                    statusText.innerText = '';
                }}
            }};

            recognition.onresult = (event) => {{
                const transcript = event.results[0][0].transcript;
                statusText.innerText = 'Captured: "' + transcript + '"';
                btnText.innerText = 'Tap to Speak Input';
                micIcon.innerText = '🎙️';
                isRecording = false;

                navigator.clipboard.writeText(transcript);
                alert('Speech recorded and copied! Click inside the text box above and press Paste (Ctrl+V / Cmd+V): "' + transcript + '"');
            }};

            recognition.onerror = (event) => {{
                statusText.innerText = 'Error: ' + event.error;
                btnText.innerText = 'Tap to Speak Input';
                micIcon.innerText = '🎙️';
                isRecording = false;
            }};
        }}
    </script>
    """
    components.html(voice_component_html, height=40)