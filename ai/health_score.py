def calculate_emotional_health_score(rows):
    """
    rows lấy từ load_journal()
    Mỗi row hiện có dạng:
    time, emotion, source, note, playlist
    """

    if not rows:
        return 75, "Chưa có đủ dữ liệu. Đây là điểm khởi đầu mặc định."

    score = 80

    positive_emotions = [
        "vui vẻ",
    ]

    neutral_emotions = [
        "cần thư giãn",
    ]

    negative_emotions = [
        "buồn",
        "lo lắng",
        "căng thẳng",
        "áp lực",
        "mệt mỏi",
    ]

    # Chỉ lấy tối đa 10 lần ghi nhận gần nhất
    recent_rows = rows[:10]

    for row in recent_rows:
        emotion = row[1]

        if emotion in positive_emotions:
            score += 3

        elif emotion in neutral_emotions:
            score += 0

        elif emotion in negative_emotions:
            score -= 6

    score = max(0, min(100, score))

    if score >= 85:
        message = "Bạn đang có trạng thái cảm xúc khá tích cực và cân bằng."

    elif score >= 70:
        message = "Bạn đang ở trạng thái tương đối ổn, nhưng vẫn nên duy trì thời gian nghỉ ngơi."

    elif score >= 50:
        message = "Bạn có dấu hiệu hơi căng thẳng hoặc mệt mỏi. Hãy dành thời gian thư giãn nhẹ."

    else:
        message = "Bạn có nhiều dấu hiệu cảm xúc tiêu cực gần đây. Hãy nghỉ ngơi và chia sẻ với người thân hoặc người tin cậy."

    return score, message