import streamlit as st
from PIL import Image
import random
import pandas as pd


from ai.health_score import calculate_emotional_health_score

from database import (
    init_db,
    save_journal,
    load_journal,
    clear_journal
)

from ai.speech_ai import speech_to_text
from ai.face_ai import (
    face_emotion_detection,
    convert_face_emotion
)

from ai.emotion_ai import (
    detect_emotion,
    life_analysis
)

from data.playlists import playlist_bank, get_playlists

#git add .
#git commit -m "Update app.py with new features and improvements"
#git push origin main


st.set_page_config(
    page_title="Mind Melody",
    page_icon="image/logo.png",
    layout="wide"
)
init_db()


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

.slogan{
    text-align:center;
    font-size:30px;
    font-weight:850;
    color:#6c4df6;
    margin-top:-70px;
    margin-bottom:10px;
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

.hero-row{
    display:flex;
    align-items:center;
    justify-content:center;
    gap:20px;
}

.hero-slogan{
    text-align:center;
    font-size:36px;
    font-weight:850;
    color:#6c4df6;
    margin-top:40px;
    margin-bottom:-70px;
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

# ===================== APPEARANCE =====================
logo = Image.open("image/apperance.png")

st.markdown("""
<div class='hero-slogan'>
Cảm xúc của bạn, hãy để chúng tôi lắng nghe 🎵
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.35,0.5,0.25])

with col2:
    st.image(
        logo,
        width=350
    )

st.markdown("""
<div class='slogan'>
Mỗi cảm xúc đều có một giai điệu riêng
</div>
""", unsafe_allow_html=True)


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
                🧠 Bạn đồng hành AI   &nbsp;&nbsp; 🎙️ Chia sẻ bằng giọng nói &nbsp;&nbsp; 📷 Nhận biết cảm xúc của bạn bằng AI &nbsp;&nbsp; 🎵 Cảm nhận giai điệu
                </div>
                """,
                unsafe_allow_html=True
            )

    if analyze:
        has_audio = audio_data is not None
        has_camera = camera_image is not None
        text_input = user_text if "user_text" in locals() else ""

        face_emotion = None

        if has_camera:
            face_emotion = face_emotion_detection(
                camera_image
            )
            
        voice_text = ""

        if has_audio:
            status = st.empty()

            status.info("🧠 Mind Melody đang lắng nghe cảm xúc của bạn...")

            voice_text = speech_to_text(audio_data)

            status.empty()

            st.success("🎙️ Đã cảm nhận chia sẻ của bạn")

            st.write("### Cảm xúc cảm nhận được:")
            st.write(voice_text)

            if face_emotion:

                st.write(
                    f"📷 DeepFace nhận diện: {face_emotion}"
                )

        combined_text = text_input + " " + voice_text

        if combined_text.strip() == "" and not has_camera:
            st.warning("Bạn hãy ghi âm, chụp khuôn mặt hoặc mở phần văn bản để chia sẻ trước nhé.")
        else:
            emotion, message = detect_emotion(
                combined_text,
                has_audio,
                has_camera
            )

            if face_emotion:

                emotion = convert_face_emotion(
                    face_emotion
                )

                message = (
                    f"Tôi cảm thấy bạn đang {emotion} "
                    f"dựa trên biểu hiện khuôn mặt."
                )

            st.markdown("## 🧠 Kết quả AI cảm nhận")
            st.markdown(f'<div class="ai-result">{message}</div>', unsafe_allow_html=True)

            st.markdown(f"### Trạng thái cảm xúc chính: **{emotion}**")

            st.write(
                "Mind Melody đang tổng hợp tín hiệu từ giọng nói, biểu hiện khuôn mặt và nội dung chia sẻ "
                "để hiểu bạn đang trải qua điều gì."
            )

            advice = {
                "căng thẳng": "Hãy thử hít thở sâu, nghỉ ngơi vài phút và nghe một playlist nhẹ nhàng.",
                "mệt mỏi": "Bạn nên cho cơ thể nghỉ ngơi, uống nước và tránh làm việc quá sức.",
                "áp lực": "Hãy chia nhỏ công việc, ưu tiên việc quan trọng và dành vài phút thư giãn.",
                "buồn": "Hãy cho phép bản thân được nghỉ ngơi, nghe một bài nhạc dịu nhẹ hoặc chia sẻ với người thân.",
                "lo lắng": "Hãy thử hít thở chậm, viết ra điều khiến bạn lo lắng và nghỉ ngơi vài phút.",
                "vui vẻ": "Hãy tận hưởng năng lượng tích cực này và lan tỏa niềm vui đến những người xung quanh.",
                "cần thư giãn": "Hãy cho bản thân vài phút yên tĩnh và nghe một playlist nhẹ nhàng."
            }

            st.info(
                "💚 Tư vấn nhẹ: " + advice.get(
                    emotion,
                    advice["cần thư giãn"]
                )
            )

            st.markdown("## 🎧 Playlist gợi ý cho bạn")

            for playlist in get_playlists(emotion):
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
                get_playlists(emotion)
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
                for p in get_playlists(emotion):
                    st.link_button(
                        p["name"],
                        p["url"]
                    )


            source = ", ".join(
                [
                    "Giọng nói" if has_audio else "",
                    "Khuôn mặt" if has_camera else "",
                    "Văn bản" if text_input.strip() else "",
                    "Giọng nói → văn bản" if voice_text.strip() else ""
                ]
            ).replace(", ,", ",").strip(", ")

            save_journal(
                emotion=emotion,
                source=source,
                note=message,
                playlist=selected_playlist["name"]
            )

        st.success("Đã lưu vào nhật ký cảm xúc.")

# ===================== TAB 2 =====================
with tab2:
    st.markdown("## 🌱 Hành trình cảm xúc")

    rows = load_journal()

    if rows:
        df = pd.DataFrame(
            rows,
            columns=[
                "Thời gian",
                "Cảm xúc",
                "Nguồn dữ liệu",
                "Ghi chú",
                "Playlist"
            ]
        )

        st.dataframe(df, use_container_width=True)

        st.markdown("## 📊 Biểu đồ cảm xúc")
        chart_data = df["Cảm xúc"].value_counts().reset_index()
        chart_data.columns = ["Cảm xúc", "Số lần"]

        st.bar_chart(chart_data.set_index("Cảm xúc"))

        if st.button("🗑️ Xóa nhật ký cảm xúc"):
            clear_journal()
            st.rerun()
    else:
        st.info("Chưa có dữ liệu. Hãy sang mục Lắng nghe tôi để phân tích cảm xúc đầu tiên.")

# ===================== TAB 3 =====================
with tab3:

    st.markdown("## 📊 Phân tích cuộc sống cảm xúc")

    rows = load_journal()

    if not rows:
        st.info(
            "Hãy sử dụng ứng dụng vài lần để Mind Melody có thêm dữ liệu phân tích."
        )

    else:
        score, score_message = calculate_emotional_health_score(rows)

        st.markdown("### 💚 AI Emotional Health Score")

        st.metric(
            label="Điểm cân bằng cảm xúc",
            value=f"{score}/100"
        )

        if score >= 85:
            st.success(score_message)
        elif score >= 70:
            st.info(score_message)
        elif score >= 50:
            st.warning(score_message)
        else:
            st.error(score_message)

        df = pd.DataFrame(
            rows,
            columns=[
                "Thời gian",
                "Cảm xúc",
                "Nguồn dữ liệu",
                "Ghi chú",
                "Playlist"
            ]
        )

        journal_for_analysis = [
            {
                "Cảm xúc": row[1]
            }
            for row in rows
        ]

        analysis = life_analysis(journal_for_analysis)

        st.markdown("### 🧠 Nhận xét từ Mind Melody")

        st.markdown(f"""
        <div class="ai-result">
            {analysis}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📝 Tóm tắt gần đây")

        st.write(
            f"Số lần ghi nhận cảm xúc: **{len(df)}**"
        )

        st.write(
            f"Cảm xúc xuất hiện nhiều nhất: **{df['Cảm xúc'].mode()[0]}**"
        )

        st.markdown("### 📈 Xu hướng cảm xúc")

        emotion_count = (
            df["Cảm xúc"]
            .value_counts()
            .reset_index()
        )

        emotion_count.columns = [
            "Cảm xúc",
            "Số lần"
        ]

        st.bar_chart(
            emotion_count.set_index("Cảm xúc")
        )

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