# Target input container for relative positioning
    st.markdown("<div style='position: relative;'>", unsafe_allow_html=True)
    
    target_text = st.text_area(
        "Input Text Stream for Analysis:", 
        value=default_val, 
        placeholder=chosen_placeholder,
        height=120
    )

    # Floating Voice Microphone Overlay inside the input box
    voice_component_html = f"""
    <style>
        .mic-overlay {{
            position: absolute;
            top: -105px;
            right: 15px;
            z-index: 999;
        }}
        .mic-btn {{
            background: {btn_bg};
            color: #ffffff;
            border: none;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.3);
            transition: transform 0.2s;
        }}
        .mic-btn:hover {{
            transform: scale(1.1);
        }}
    </style>
    <div class="mic-overlay">
        <button id="record-btn" class="mic-btn" title="Tap to Speak Input">
            <span id="mic-icon">🎙️</span>
        </button>
    </div>

    <script>
        const btn = document.getElementById('record-btn');
        const micIcon = document.getElementById('mic-icon');
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (SpeechRecognition) {{
            const recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';
            let isRecording = false;

            btn.onclick = () => {{
                if (!isRecording) {{
                    recognition.start();
                    isRecording = true;
                    micIcon.innerText = '🔴';
                }} else {{
                    recognition.stop();
                    isRecording = false;
                    micIcon.innerText = '🎙️';
                }}
            }};

            recognition.onresult = (event) => {{
                const transcript = event.results[0][0].transcript;
                micIcon.innerText = '🎙️';
                isRecording = false;
                navigator.clipboard.writeText(transcript);
                alert('Captured speech copied! Paste (Ctrl+V / Cmd+V) into the text box: "' + transcript + '"');
            }};

            recognition.onerror = () => {{
                micIcon.innerText = '🎙️';
                isRecording = false;
            }};
        }} else {{
            btn.style.display = 'none';
        }}
    </script>
    """
    components.html(voice_component_html, height=0)
    st.markdown("</div>", unsafe_allow_html=True)