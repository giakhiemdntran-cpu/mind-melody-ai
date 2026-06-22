from collections import Counter


POSITIVE_WORDS = [
    "vui",
    "vui vẻ",
    "hạnh phúc",
    "tích cực",
    "tuyệt vời",
    "ổn",
    "rất ổn",
    "tốt",
    "rất tốt",
    "thoải mái",
    "dễ chịu",
    "phấn khởi",
    "hào hứng",
    "tự tin",
    "yêu đời",
    "may mắn",
    "biết ơn",
    "thành công",
    "đẹp trai",
    "xinh",
    "xinh đẹp",
    "giỏi",
    "rất giỏi",
    "tự hào",
    "năng lượng",
    "tràn đầy năng lượng",
    "hôm nay ổn",
    "mình ổn",
    "tôi ổn",
    "bản thân mình rất đẹp",
    "bản thân mình rất đẹp trai",
]

SAD_WORDS = [
    "buồn",
    "cô đơn",
    "chán",
    "thất vọng",
    "tủi thân",
    "khóc",
    "mất động lực",
    "không vui",
    "trống rỗng",
]

STRESS_WORDS = [
    "stress",
    "căng thẳng",
    "khó thở",
    "bất an",
    "rối",
    "quá tải",
    "mệt đầu",
    "đau đầu",
]

TIRED_WORDS = [
    "mệt",
    "mệt mỏi",
    "kiệt sức",
    "đuối",
    "hết năng lượng",
    "buồn ngủ",
    "uể oải",
    "rã rời",
]

PRESSURE_WORDS = [
    "áp lực",
    "deadline",
    "thi",
    "bài tập",
    "công việc nhiều",
    "không kịp",
    "quá nhiều việc",
    "bị dí",
]

ANXIETY_WORDS = [
    "lo",
    "lo lắng",
    "sợ",
    "hoang mang",
    "bồn chồn",
    "lo quá",
    "bất an",
    "run",
]


NEGATION_PATTERNS = [
    "không vui",
    "không ổn",
    "không tốt",
    "không hạnh phúc",
    "chưa ổn",
    "khá tệ",
    "rất tệ",
]


def count_matches(text, words):
    count = 0

    for word in words:
        if word in text:
            count += 1

    return count


def detect_emotion(text="", has_audio=False, has_camera=False):
    if text is None:
        text = ""

    text = text.lower().strip()

    if text == "":
        if has_audio and has_camera:
            return (
                "cần thư giãn",
                "Qua giọng nói và biểu hiện, tôi cảm thấy bạn đang cần được lắng nghe và thư giãn."
            )

        if has_audio:
            return (
                "cần thư giãn",
                "Tôi đã nhận được chia sẻ bằng giọng nói. Tôi cảm thấy bạn đang cần một không gian nhẹ nhàng hơn."
            )

        if has_camera:
            return (
                "cần thư giãn",
                "Qua biểu hiện khuôn mặt, tôi cảm thấy bạn đang cần một chút thư giãn."
            )

        return (
            "cần thư giãn",
            "Tôi cảm thấy bạn đang cần một chút thư giãn và cân bằng lại cảm xúc."
        )

    scores = {
        "vui vẻ": count_matches(text, POSITIVE_WORDS),
        "buồn": count_matches(text, SAD_WORDS),
        "căng thẳng": count_matches(text, STRESS_WORDS),
        "mệt mỏi": count_matches(text, TIRED_WORDS),
        "áp lực": count_matches(text, PRESSURE_WORDS),
        "lo lắng": count_matches(text, ANXIETY_WORDS),
    }

    # Xử lý phủ định: "không vui", "không ổn" không được tính là tích cực
    for pattern in NEGATION_PATTERNS:
        if pattern in text:
            scores["vui vẻ"] = 0
            scores["buồn"] += 1

    best_emotion = max(
        scores,
        key=scores.get
    )

    best_score = scores[best_emotion]

    if best_score == 0:
        return (
            "cần thư giãn",
            "Tôi đã lắng nghe chia sẻ của bạn. Hiện tại cảm xúc của bạn khá trung tính và có thể cần một chút thư giãn nhẹ."
        )

    messages = {
        "vui vẻ": "Tôi cảm thấy bạn đang có tâm trạng tích cực, tự tin và vui vẻ.",
        "buồn": "Tôi cảm thấy bạn đang buồn hoặc có chút cô đơn.",
        "căng thẳng": "Tôi cảm thấy bạn đang hơi căng thẳng và cần được thư giãn.",
        "mệt mỏi": "Tôi cảm thấy bạn đang khá mệt mỏi và cần nghỉ ngơi một chút.",
        "áp lực": "Tôi cảm thấy bạn đang chịu nhiều áp lực trong thời gian này.",
        "lo lắng": "Tôi cảm thấy bạn đang có chút lo lắng và bất an.",
    }

    return (
        best_emotion,
        messages[best_emotion]
    )


def life_analysis(journal):
    if not journal:
        return "Chưa có đủ dữ liệu để phân tích cuộc sống cảm xúc của bạn."

    emotions = []

    for item in journal:
        emotion = item.get("Cảm xúc")

        if emotion:
            emotions.append(emotion)

    if not emotions:
        return "Chưa có đủ dữ liệu để phân tích cuộc sống cảm xúc của bạn."

    counter = Counter(emotions)

    top_emotion = counter.most_common(1)[0][0]

    negative_emotions = [
        "căng thẳng",
        "áp lực",
        "mệt mỏi",
        "buồn",
        "lo lắng",
    ]

    negative_count = sum(
        counter.get(emotion, 0)
        for emotion in negative_emotions
    )

    positive_count = counter.get("vui vẻ", 0)

    if top_emotion in ["căng thẳng", "áp lực", "mệt mỏi"]:
        return (
            "Dữ liệu gần đây cho thấy bạn có thể đang trải qua giai đoạn khá nhiều áp lực. "
            "Mind Melody khuyên bạn nên nghỉ ngơi đều hơn, giảm tải công việc và dành thời gian cho bản thân."
        )

    if top_emotion == "buồn":
        return (
            "Dữ liệu cho thấy bạn có nhiều khoảnh khắc trầm xuống. "
            "Hãy thử chia sẻ với người thân, nghỉ ngơi và chọn các hoạt động nhẹ nhàng hơn."
        )

    if top_emotion == "lo lắng":
        return (
            "Bạn đang có xu hướng lo lắng trong thời gian gần đây. "
            "Hãy thử hít thở chậm, sắp xếp lại việc cần làm và cho bản thân một khoảng nghỉ ngắn."
        )

    if positive_count > negative_count:
        return (
            "Bạn đang duy trì trạng thái cảm xúc khá tích cực. "
            "Hãy tiếp tục giữ những thói quen tốt và lan tỏa năng lượng này."
        )

    return (
        "Trạng thái cảm xúc của bạn tương đối cân bằng. "
        "Hãy tiếp tục theo dõi hành trình cảm xúc cùng Mind Melody."
    )