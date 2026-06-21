import os
import tempfile

try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except Exception:
    DeepFace = None
    DEEPFACE_AVAILABLE = False


FACE_MAP = {
    "happy": "vui vẻ",
    "sad": "buồn",
    "angry": "căng thẳng",
    "fear": "lo lắng",
    "neutral": "cần thư giãn",
    "surprise": "vui vẻ",
    "disgust": "căng thẳng",
}


def face_emotion_detection(camera_image):
    if camera_image is None or not DEEPFACE_AVAILABLE:
        return None
    # if camera_image is None:
    #     return None

    # image_path = None

    # try:
    #     with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
    #         tmp_file.write(camera_image.getvalue())
    #         image_path = tmp_file.name

    #     result = DeepFace.analyze(
    #         img_path=image_path,
    #         actions=["emotion"],
    #         enforce_detection=False,
    #     )

    #     if isinstance(result, list):
    #         return result[0].get("dominant_emotion")

    #     return result.get("dominant_emotion")

    # except Exception as e:
    #     print("DeepFace error:", e)
    #     return None

    # finally:
    #     if image_path and os.path.exists(image_path):
    #         os.remove(image_path)


def convert_face_emotion(face_emotion):
    if not face_emotion:
        return "cần thư giãn"

    return FACE_MAP.get(face_emotion, "cần thư giãn")