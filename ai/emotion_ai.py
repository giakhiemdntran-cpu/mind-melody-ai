from collections import Counter


def detect_emotion(text="", has_audio=False, has_camera=False):
    """
    Phân tích cảm xúc từ văn bản đã nhập hoặc văn bản chuyển từ giọng nói.
    Trả về:
    - emotion: tên cảm xúc
    - message: câu phản hồi của AI
    """

    if text is None:
        text = ""

    text = text.lower()

    if any(word in text for word in [
        "stress",
        "căng thẳng",
        "khó thở",
        "bất an",
        "lo quá",
        "rối",
    ]):
        return (
            "căng thẳng",
            "Tôi cảm thấy bạn đang hơi căng thẳng và cần được thư giãn."
        )

    if any(word in text for word in [
        "mệt",
        "kiệt sức",
        "đuối",
        "hết năng lượng",
        "buồn ngủ",
        "uể oải",
    ]):
        return (
            "mệt mỏi",
            "Tôi cảm thấy bạn đang khá mệt mỏi và cần nghỉ ngơi một chút."
        )

    if any(word in text for word in [
        "áp lực",
        "deadline",
        "thi",
        "bài tập",
        "quá tải",
        "công việc nhiều",
        "không kịp",
    ]):
        return (
            "áp lực",
            "Tôi cảm thấy bạn đang chịu nhiều áp lực trong thời gian này."
        )

    if any(word in text for word in [
        "lo",
        "lo lắng",
        "sợ",
        "hoang mang",
        "bồn chồn",
    ]):
        return (
            "lo lắng",
            "Tôi cảm thấy bạn đang có chút lo lắng và bất an."
        )

    if any(word in text for word in [
        "buồn",
        "cô đơn",
        "chán",
        "thất vọng",
        "tủi thân",
        "khóc",
    ]):
        return (
            "buồn",
            "Tôi cảm thấy bạn đang buồn hoặc có chút cô đơn."
        )

    if any(word in text for word in [
        "vui",
        "hạnh phúc",
        "thành công",
        "phấn khởi",
        "tuyệt vời",
        "ổn",
        "tốt",
    ]):
        return (
            "vui vẻ",
            "Tôi cảm thấy bạn đang có tâm trạng tích cực và vui vẻ."
        )

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


def life_analysis(journal):
    """
    journal là list dạng:
    [
        {"Cảm xúc": "căng thẳng"},
        {"Cảm xúc": "buồn"},
        ...
    ]
    """

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