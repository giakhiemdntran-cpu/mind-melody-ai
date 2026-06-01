import streamlit as st
import pandas as pd
from datetime import datetime
import random
import tempfile
from PIL import Image
# from faster_whisper import WhisperModel

st.set_page_config(
    page_title="Mind Melody",
    page_icon="image/logo.png",
    layout="wide"
)


# ===================== SESSION =====================
if "journal" not in st.session_state:
    st.session_state.journal = []

# ===================== CSS =====================
st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at top left, #ead7ff 0%, transparent 28%),
        radial-gradient(circle at top right, #fff1b8 0%, transparent 28%),
        radial-gradient(circle at bottom left, #d9f3ff 0%, transparent 30%),
        linear-gradient(135deg, #f9f4ff 0%, #ecf8ff 48%, #fff8e6 100%);
    color: #1f2550;
}

.block-container {
    max-width: 1250px;
    padding-top: 28px;
}

.main-title {
    text-align: center;
    font-size: 66px;
    font-weight: 950;
    background: linear-gradient(90deg, #5f6cff, #d946ef, #ff4f8b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.slogan {
    text-align: center;
    font-size: 26px;
    font-weight: 850;
    color: #6c4df6;
    margin-bottom: 25px;
}

.splash {
    position: fixed;
    inset: 0;
    z-index: 999999;
    background: linear-gradient(135deg, #6c63ff, #d946ef, #ff6b9a);
    display: flex;
    justify-content: center;
    align-items: center;
    animation: splashFade 3.8s forwards;
}

.splash-text {
    color: white;
    font-size: 42px;
    font-weight: 950;
    text-align: center;
    padding: 40px;
    animation: blinkText 1s infinite;
}

@keyframes blinkText {
    0% { opacity: 0.25; transform: scale(0.96); }
    50% { opacity: 1; transform: scale(1.04); }
    100% { opacity: 0.25; transform: scale(0.96); }
}

@keyframes splashFade {
    0% { opacity: 1; visibility: visible; }
    75% { opacity: 1; visibility: visible; }
    100% { opacity: 0; visibility: hidden; pointer-events: none; }
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.78);
    border-radius: 28px;
    box-shadow: 0 15px 42px rgba(80,70,180,0.14);
    border: 1px solid rgba(255,255,255,0.9);
    padding: 22px;
}

.stButton button {
    border-radius: 16px;
    height: 54px;
    font-weight: 850;
    color: #6c4df6;
    border: 1px solid #7c4dff;
    background: white;
}

.stButton button:hover {
    background: linear-gradient(90deg, #6c63ff, #d946ef);
    color: white;
    border: none;
}

.ai-result {
    padding: 28px;
    border-radius: 26px;
    background: linear-gradient(135deg, #6c63ff, #d946ef);
    color: white;
    font-size: 25px;
    font-weight: 850;
    text-align: center;
    box-shadow: 0 14px 35px rgba(80,70,180,0.25);
}

.small-note {
    color: #5d6380;
    font-size: 15px;
}

.playlist-card {
    padding: 18px;
    border-radius: 20px;
    background: rgba(255,255,255,0.82);
    box-shadow: 0 10px 25px rgba(80,70,180,0.10);
    margin-bottom: 15px;
}

.tech-box {
    padding: 22px;
    border-radius: 26px;
    background: rgba(255,255,255,0.70);
    box-shadow: 0 12px 35px rgba(80,70,180,0.12);
    text-align: center;
    font-size: 17px;
    margin-top: 20px;
}

.footer {
    text-align: center;
    color: #7357db;
    font-size: 21px;
    font-weight: 750;
    margin-top: 32px;
}
</style>

<div class="splash">
    <div class="splash-text">
        Cảm xúc của bạn, hãy để chúng tôi lắng nghe. 🎵
    </div>
</div>
""", unsafe_allow_html=True)

# ===================== LOGO =====================

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image("image/logo.png", width=220)

st.markdown(
    '<div class="slogan">Cảm xúc của bạn, hãy để chúng tôi lắng nghe 🎵</div>',
    unsafe_allow_html=True
)




# ===================== DATA =====================
playlist_bank = {

    "căng thẳng": [
        {
            "name": "Lofi Việt Chill",
            "url": "https://www.youtube.com/results?search_query=lofi+viet+chill"
        },
        {
            "name": "Piano Thư Giãn",
            "url": "https://www.youtube.com/results?search_query=piano+thu+gian"
        },
        {
            "name": "Nhạc Cafe Chill",
            "url": "https://www.youtube.com/results?search_query=cafe+music+viet"
        }
    ],

    "mệt mỏi": [
        {
            "name": "Healing Music",
            "url": "https://www.youtube.com/results?search_query=healing+music+viet"
        },
        {
            "name": "Acoustic Việt",
            "url": "https://www.youtube.com/results?search_query=acoustic+viet"
        },
        {
            "name": "Nhạc Ngủ Ngon",
            "url": "https://www.youtube.com/results?search_query=nhac+ngu+ngon"
        }
    ],

    "áp lực": [
        {
            "name": "Study Lofi",
            "url": "https://www.youtube.com/results?search_query=study+lofi+viet"
        },
        {
            "name": "Deep Focus",
            "url": "https://www.youtube.com/results?search_query=deep+focus+music"
        },
        {
            "name": "Nhạc Tập Trung",
            "url": "https://www.youtube.com/results?search_query=nhac+tap+trung+hoc+bai"
        }
    ],

    "buồn": [
        {
            "name": "Ballad Việt",
            "url": "https://www.youtube.com/results?search_query=ballad+viet"
        },
        {
            "name": "Indie Việt",
            "url": "https://www.youtube.com/results?search_query=indie+viet"
        },
        {
            "name": "Nhạc Chữa Lành",
            "url": "https://www.youtube.com/results?search_query=healing+vietnamese+music"
        }
    ],

    "vui vẻ": [
        {
            "name": "V-Pop Tích Cực",
            "url": "https://www.youtube.com/results?search_query=vpop+happy+songs"
        },
        {
            "name": "Nhạc Tạo Động Lực",
            "url": "https://www.youtube.com/results?search_query=motivational+music+vietnamese"
        },
        {
            "name": "Nhạc Trẻ Việt",
            "url": "https://www.youtube.com/results?search_query=nhac+tre+viet+hay"
        }
    ],

    "cần thư giãn": [
        {
            "name": "Café Sữa Đá Lofi",
            "url": "https://www.youtube.com/results?search_query=cafe+sua+da+lofi"
        },
        {
            "name": "Chill Việt",
            "url": "https://www.youtube.com/results?search_query=chill+viet"
        },
        {
            "name": "Nature Sounds",
            "url": "https://www.youtube.com/results?search_query=nature+sounds+relax"
        }
    ],

    "lo lắng": [
        {
            "name": "Calm Music",
            "url": "https://www.youtube.com/results?search_query=calm+music"
        },
        {
            "name": "Meditation Music",
            "url": "https://www.youtube.com/results?search_query=meditation+music"
        },
        {
            "name": "Piano Bình Yên",
            "url": "https://www.youtube.com/results?search_query=peaceful+piano"
        }
    ]
}

# @st.cache_resource(show_spinner=False)
# def load_whisper_model():
#     return WhisperModel(
#         "small",
#         device="cpu",
#         compute_type="int8"
#     )

def speech_to_text(audio_data):
    return "Tôi đang thử nghiệm chức năng Speech-to-Text."
    # if audio_data is None:
    #     return ""

    # with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
    #     tmp_file.write(audio_data.getbuffer())
    #     audio_path = tmp_file.name

    # model = load_whisper_model()

    # segments, info = model.transcribe(
    #     audio_path,
    #     language="vi",
    #     beam_size=5
    # )

    # text = " ".join([segment.text for segment in segments])

    # return text.strip()

def detect_emotion(text, has_audio=False, has_camera=False):
    text = text.lower()

    if any(w in text for w in ["stress", "căng thẳng", "khó thở", "bất an"]):
        return "căng thẳng", "Tôi cảm thấy bạn đang hơi căng thẳng và cần được thư giãn."

    if any(w in text for w in ["mệt", "kiệt sức", "đuối", "hết năng lượng", "buồn ngủ"]):
        return "mệt mỏi", "Tôi cảm thấy bạn đang khá mệt mỏi và cần nghỉ ngơi một chút."

    if any(w in text for w in ["áp lực", "deadline", "thi", "bài tập", "quá tải", "công việc nhiều"]):
        return "áp lực", "Tôi cảm thấy bạn đang chịu nhiều áp lực trong thời gian này."

    if any(w in text for w in ["buồn", "cô đơn", "chán", "thất vọng", "tủi thân"]):
        return "buồn", "Tôi cảm thấy bạn đang buồn hoặc có chút cô đơn."

    if any(w in text for w in ["vui", "hạnh phúc", "thành công", "phấn khởi", "tuyệt vời"]):
        return "vui vẻ", "Tôi cảm thấy bạn đang có tâm trạng tích cực và vui vẻ."

    if has_audio and has_camera:
        return "cần thư giãn", "Qua giọng nói và biểu hiện, tôi cảm thấy bạn đang cần được lắng nghe và thư giãn."

    if has_audio:
        return "cần thư giãn", "Tôi đã nhận được chia sẻ bằng giọng nói. Tôi cảm thấy bạn đang cần một không gian nhẹ nhàng hơn."

    if has_camera:
        return "cần thư giãn", "Qua biểu hiện khuôn mặt, tôi cảm thấy bạn đang cần một chút thư giãn."

    return "cần thư giãn", "Tôi cảm thấy bạn đang cần một chút thư giãn và cân bằng lại cảm xúc."

def life_analysis(journal):
    if not journal:
        return "Chưa có đủ dữ liệu để phân tích cuộc sống cảm xúc của bạn."

    emotions = [item["Cảm xúc"] for item in journal]
    top = max(set(emotions), key=emotions.count)

    if top in ["căng thẳng", "áp lực", "mệt mỏi"]:
        return "Dữ liệu gần đây cho thấy bạn có thể đang trải qua giai đoạn khá nhiều áp lực. Mind Melody khuyên bạn nên nghỉ ngơi đều hơn, giảm tải công việc và dành thời gian cho bản thân."
    if top == "buồn":
        return "Dữ liệu cho thấy bạn có nhiều khoảnh khắc trầm xuống. Hãy thử chia sẻ với người thân, nghỉ ngơi và chọn các hoạt động nhẹ nhàng hơn."
    if top == "vui vẻ":
        return "Bạn đang có xu hướng cảm xúc tích cực. Hãy tiếp tục duy trì các thói quen tốt và lan tỏa năng lượng này."
    return "Bạn đang cần cân bằng lại cảm xúc. Những playlist nhẹ nhàng và thói quen nghỉ ngơi ngắn có thể giúp ích."

# ===================== HEADER =====================
st.markdown('<div class="main-title">🎵 Mind Melody ♪</div>', unsafe_allow_html=True)
st.markdown('<div class="slogan">Mỗi cảm xúc đều có một giai điệu riêng</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🧠 Lắng nghe tôi",
    "🌱 Hành trình cảm xúc",
    "📊 Phân tích cuộc sống",
    "🚀 AI Behind Mind Melody"
])

# ===================== TAB 1 =====================
with tab1:
    left, main = st.columns([0.8, 2.2], gap="large")

    with left:
        with st.container(border=True):
            st.markdown("### ✍️ Viết nếu bạn muốn")
            with st.expander("Mở phần chia sẻ bằng văn bản"):
                user_text = st.text_area(
                    "Bạn muốn viết điều gì?",
                    height=170,
                    placeholder="Ví dụ: Hôm nay tôi thấy mệt và áp lực vì deadline..."
                )
            st.caption("Văn bản chỉ là lựa chọn phụ. Mind Melody ưu tiên giọng nói và biểu hiện khuôn mặt.")

    with main:
        with st.container(border=True):
            st.markdown("## 🎙️ Hãy chia sẻ cảm xúc của bạn")
            st.write("Bạn có thể nói bằng giọng nói hoặc chụp biểu hiện khuôn mặt để Mind Melody lắng nghe.")

            c1, c2 = st.columns(2)

            with c1:
                audio_data = st.audio_input("🎤 Ghi âm giọng nói")

            with c2:
                camera_image = st.camera_input("📷 Chụp biểu hiện khuôn mặt")

            analyze = st.button("✨ Phân tích cảm xúc tổng hợp", use_container_width=True)

            st.markdown(
                """
                <div class="tech-box">
                🧠 Bạn đồng hành AI của bạn &nbsp;&nbsp; 🎙️ Chia sẻ bằng giọng nói &nbsp;&nbsp; 📷 Nhận biết cảm xúc của bạn &nbsp;&nbsp; 🎵 Cảm nhận giai điệu
                </div>
                """,
                unsafe_allow_html=True
            )

    if analyze:
        has_audio = audio_data is not None
        has_camera = camera_image is not None
        text_input = user_text if "user_text" in locals() else ""

        voice_text = ""

        if has_audio:
            status = st.empty()

            status.info("🧠 Mind Melody đang lắng nghe cảm xúc của bạn...")

            voice_text = speech_to_text(audio_data)

            status.empty()

            st.success("🎙️ Đã cảm nhận chia sẻ của bạn")

            st.write("### Cảm xúc cảm nhận được:")
            st.write(voice_text)

        combined_text = text_input + " " + voice_text

        if combined_text.strip() == "" and not has_camera:
            st.warning("Bạn hãy ghi âm, chụp khuôn mặt hoặc mở phần văn bản để chia sẻ trước nhé.")
        else:
            emotion, message = detect_emotion(combined_text, has_audio, has_camera)

            st.markdown("## 🧠 Kết quả AI cảm nhận")
            st.markdown(f'<div class="ai-result">{message}</div>', unsafe_allow_html=True)

            st.markdown(f"### Trạng thái cảm xúc chính: **{emotion}**")

            st.write(
                "Mind Melody đang tổng hợp tín hiệu từ giọng nói, biểu hiện khuôn mặt và nội dung chia sẻ "
                "để hiểu bạn đang trải qua điều gì."
            )

            advice = {
                "căng thẳng": "Hãy thử hít thở chậm 3 phút, tạm rời màn hình và nghe một playlist nhẹ.",
                "mệt mỏi": "Bạn nên nghỉ ngơi ngắn, uống nước và chọn nhạc chậm để cơ thể thả lỏng.",
                "áp lực": "Hãy chia nhỏ công việc, ưu tiên việc quan trọng nhất và cho mình một khoảng nghỉ.",
                "buồn": "Bạn có thể nghe nhạc dịu nhẹ, viết ra điều đang làm mình buồn hoặc chia sẻ với người tin cậy.",
                "vui vẻ": "Hãy giữ năng lượng tích cực này và chọn playlist tươi sáng.",
                "cần thư giãn": "Hãy cho bản thân vài phút yên tĩnh và nghe một playlist nhẹ nhàng."
            }

            st.info("💚 Tư vấn nhẹ: " + advice[emotion])

            st.markdown("## 🎧 Playlist gợi ý cho bạn")

            for playlist in playlist_bank[emotion]:
                st.markdown(f"""
                <div class="playlist-card">
                    <b>🎵 {playlist["name"]}</b><br>
                    <span class="small-note">
                        Playlist được gợi ý theo trạng thái: {emotion}
                    </span>
                </div>
                """, unsafe_allow_html=True)

                st.link_button(
                    f"▶️ Mở {playlist['name']}",
                    playlist["url"]
                )

            selected_playlist = random.choice(
                playlist_bank[emotion]
            )

            st.markdown(
                f"## 🎵 Liều thuốc âm nhạc hôm nay"
            )

            st.success(
                selected_playlist["name"]
            )

            st.link_button(
                "🎧 Nghe ngay trên YouTube",
                selected_playlist["url"]
            )

            with st.expander("🎶 Thêm gợi ý khác"):
                for p in playlist_bank[emotion]:
                    st.link_button(
                        p["name"],
                        p["url"]
                    )


            st.session_state.journal.append({
                "Thời gian": datetime.now().strftime("%H:%M - %d/%m/%Y"),
                "Cảm xúc": emotion,
                "Nguồn dữ liệu": ", ".join(
                    [
                        "Giọng nói" if has_audio else "",
                        "Khuôn mặt" if has_camera else "",
                        "Văn bản" if text_input.strip() else "",
                        "Giọng nói → văn bản" if voice_text.strip() else ""
                    ]
                ).replace(", ,", ",").strip(", "),
                "Ghi chú": message
            })

        st.success("Đã lưu vào nhật ký cảm xúc.")

# ===================== TAB 2 =====================
with tab2:
    st.markdown("## 📖 Nhật ký cảm xúc")

    if st.session_state.journal:
        df = pd.DataFrame(st.session_state.journal)
        st.dataframe(df, use_container_width=True)

        st.markdown("## 📊 Biểu đồ cảm xúc")
        chart_data = df["Cảm xúc"].value_counts().reset_index()
        chart_data.columns = ["Cảm xúc", "Số lần"]
        st.bar_chart(chart_data.set_index("Cảm xúc"))

        if st.button("🗑️ Xóa nhật ký cảm xúc"):
            st.session_state.journal = []
            st.rerun()
    else:
        st.info("Chưa có dữ liệu. Hãy sang mục Lắng nghe tôi để phân tích cảm xúc đầu tiên.")

# ===================== TAB 3 =====================
with tab3:
    st.markdown("## 📊 Phân tích cuộc sống cảm xúc")

    analysis = life_analysis(st.session_state.journal)

    st.markdown(f"""
    <div class="ai-result">
        {analysis}
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.journal:
        df = pd.DataFrame(st.session_state.journal)
        st.markdown("### Tóm tắt gần đây")
        st.write(f"Số lần ghi nhận cảm xúc: **{len(df)}**")
        st.write(f"Cảm xúc xuất hiện nhiều nhất: **{df['Cảm xúc'].mode()[0]}**")
    else:
        st.write("Hãy sử dụng ứng dụng vài lần để Mind Melody có thêm dữ liệu phân tích.")

# ===================== TAB 4 =====================
with tab4:
    st.markdown("## 🚀 AI Behind Mind Melody")

    st.markdown("""
    ### 1. Giọng nói
    - Người dùng nói cảm xúc.
    - Speech-to-Text chuyển giọng nói thành văn bản.
    - Có thể dùng: Whisper, Faster-Whisper hoặc Gemini Speech.

    ### 2. Khuôn mặt
    - Camera ghi nhận biểu hiện.
    - DeepFace nhận diện cảm xúc khuôn mặt.
    - Có thể phân tích: happy, sad, angry, fear, neutral.

    ### 3. Hành vi
    - YOLO nhận diện hành động như cúi đầu, dụi mắt, ngáp, nằm gục.
    - Từ đó suy luận mệt mỏi, thiếu ngủ hoặc căng thẳng.

    ### 4. Emotion Fusion Engine
    - Kết hợp dữ liệu từ giọng nói, khuôn mặt, văn bản và hành vi.
    - Đưa ra kết luận: “Tôi cảm thấy bạn đang...”

    ### 5. Tư vấn và âm nhạc
    - Gợi ý playlist theo trạng thái cảm xúc.
    - Đưa ra lời khuyên tinh thần nhẹ nhàng, không chẩn đoán bệnh.
    """)

    st.warning(
        "Lưu ý: Mind Melody chỉ hỗ trợ chăm sóc tinh thần nhẹ nhàng, "
        "không thay thế chuyên gia tâm lý hoặc bác sĩ."
    )

st.markdown(
    '<div class="footer">💜 Mind Melody – Cùng bạn lắng nghe và chăm sóc cảm xúc mỗi ngày 🎵</div>',
    unsafe_allow_html=True
)
