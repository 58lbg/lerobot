import json

def calculate_target_speed(current_duration, current_speed, target_duration):
    """
    根据当前音频长度、当前语速和目标音频长度，计算目标语速。

    参数：
        current_duration (float): 当前音频长度（秒）
        current_speed (float): 当前语速（1.0 表示正常语速）
        target_duration (float): 目标音频长度（秒）

    返回：
        float: 目标语速（倍速）
    """
    if current_duration < 6 :
        return 0.9
    if 6 < current_duration < 6.5:
        return 1.0
    if 6.5 < current_duration < 7:
        return 1.05
    if 7 < current_duration < 7.5:
        return 1.10
    if 7.5 < current_duration < 8:
        return 1.15
    if 8 < current_duration < 8.5:
        return 1.20
    if 8.5 < current_duration < 9:
        return 1.25
    return 1.3

def format_seconds(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = seconds % 60
    return "{:02d}:{:02d}:{:06.3f}".format(hours, minutes, remaining_seconds)

def main(txt2audio: str, pics:str, audioDuration, audioUrl) -> dict:
    audioResult = json.loads(txt2audio)
    #audioResult = json.loads(audioResult["txt2audio"])
    # return audioResult
    target_speed = calculate_target_speed(audioResult["duration"], 1.3, 10)
    audioDuration2 = audioResult["duration"]
    offset = abs(10 - audioDuration)
    offset2 = abs(10 - audioDuration2)
    if audioDuration2 < 10 and offset2 < offset:
        return {
            "audioUrl": audioResult["audioInfo"],
            "audioDuration": audioDuration2,
            "formatDuration": format_seconds(audioDuration2),
            "target_speed": target_speed,
        }
    else:
        return {
            "audioUrl": audioUrl,
            "audioDuration": audioDuration,
            "formatDuration": format_seconds(audioDuration),
            "target_speed": target_speed,
        }

if __name__ == '__main__':
    calculate_target_speed(7.84,1.3, 10)