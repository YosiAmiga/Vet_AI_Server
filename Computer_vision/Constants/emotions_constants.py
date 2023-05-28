emotions = { 1: 'happiness', 2: 'surprise', 3: 'sadness',
                4: 'anger', 5: 'disgust', 6: 'fear', 7: 'neutral'}


def get_emotion_id(emotion_name):
    for id, name in emotions.items():
        if name == emotion_name:
            return id
    return None  # emotion name not found in dictionary