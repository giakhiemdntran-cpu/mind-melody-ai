playlist_bank = {
    "vui vẻ": [
        {
            "name": "V-Pop Năng Lượng Tích Cực",
            "url": "https://www.youtube.com/results?search_query=vpop+happy+playlist"
        },
        {
            "name": "Nhạc Trẻ Việt Vui Tươi",
            "url": "https://www.youtube.com/results?search_query=nhac+tre+viet+vui+tuoi"
        },
        {
            "name": "Nhạc Tạo Động Lực Việt Nam",
            "url": "https://www.youtube.com/results?search_query=nhac+tao+dong+luc+viet+nam"
        }
    ],

    "buồn": [
        {
            "name": "Ballad Việt Nhẹ Nhàng",
            "url": "https://www.youtube.com/results?search_query=ballad+viet+nhẹ+nhàng"
        },
        {
            "name": "Acoustic Việt Tâm Trạng",
            "url": "https://www.youtube.com/results?search_query=acoustic+viet+tam+trang"
        },
        {
            "name": "Indie Việt Chữa Lành",
            "url": "https://www.youtube.com/results?search_query=indie+viet+chua+lanh"
        }
    ],

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

    "áp lực": [
        {
            "name": "Study Lofi Việt",
            "url": "https://www.youtube.com/results?search_query=study+lofi+viet"
        },
        {
            "name": "Deep Focus Music",
            "url": "https://www.youtube.com/results?search_query=deep+focus+music"
        },
        {
            "name": "Nhạc Tập Trung Học Bài",
            "url": "https://www.youtube.com/results?search_query=nhac+tap+trung+hoc+bai"
        }
    ],

    "mệt mỏi": [
        {
            "name": "Healing Music Việt",
            "url": "https://www.youtube.com/results?search_query=healing+music+viet"
        },
        {
            "name": "Nhạc Không Lời Thư Giãn",
            "url": "https://www.youtube.com/results?search_query=nhac+khong+loi+thu+gian"
        },
        {
            "name": "Nhạc Ngủ Ngon",
            "url": "https://www.youtube.com/results?search_query=nhac+ngu+ngon"
        }
    ],

    "lo lắng": [
        {
            "name": "Calm Piano",
            "url": "https://www.youtube.com/results?search_query=calm+piano"
        },
        {
            "name": "Meditation Music",
            "url": "https://www.youtube.com/results?search_query=meditation+music"
        },
        {
            "name": "Piano Bình Yên",
            "url": "https://www.youtube.com/results?search_query=peaceful+piano"
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
            "name": "Nature Sounds Relax",
            "url": "https://www.youtube.com/results?search_query=nature+sounds+relax"
        }
    ]
}


def get_playlists(emotion):
    return playlist_bank.get(
        emotion,
        playlist_bank["cần thư giãn"]
    )