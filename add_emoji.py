import json
import os

keyword_to_emoji = {
    "기초 과학": "🔬",
    "연구": "🔬",
    "입자 가속기": "🔬",
    "핵물리학": "⚛️",
    "원자로": "☢️",
    "방사능": "☢️",
    "원자력": "☢️",
    "우라늄": "☢️",
    "플루토늄": "☢️",
    "우주": "🚀",
    "로켓": "🚀",
    "항공": "✈️",
    "비행기": "✈️",
    "제트": "✈️",
    "배터리": "🔋",
    "건전지": "🔋",
    "스마트폰": "📱",
    "터치스크린": "📱",
    "컴퓨터": "💻",
    "반도체": "💾",
    "메모리": "💾",
    "자석": "🧲",
    "모터": "🧲",
    "전기차": "🚗",
    "자동차": "🚗",
    "의료": "🏥",
    "의학": "🏥",
    "암": "💊",
    "엑스레이": "🩻",
    "조영제": "🩻",
    "소독": "💧",
    "수영장": "💧",
    "세균": "🧼",
    "살충제": "☠️",
    "쥐약": "☠️",
    "독성": "☠️",
    "조명": "💡",
    "전구": "💡",
    "레이저": "💥",
    "폭발": "💥",
    "형광": "✨",
    "네온": "✨",
    "카메라": "📷",
    "렌즈": "🔍",
    "보석": "💎",
    "귀금속": "💍",
    "금": "🪙",
    "합금": "⚙️",
    "강철": "🏗️",
    "건축": "🏗️",
    "뼈": "🦴",
    "치아": "🦷",
    "소금": "🧂",
    "식물": "🌱",
    "비료": "🌱",
    "혈액": "🩸",
    "광섬유": "🌐",
    "통신": "📡",
    "디스플레이": "📺",
    "모니터": "🖥️",
    "시계": "⌚",
    "온도계": "🌡️",
    "풍선": "🎈",
    "기구": "🎈",
    "광학": "🔭",
    "유리": "🪟",
    "화재": "🔥",
    "난연": "🧯"
}

target_file = "/Users/pochoco/Desktop/원소주기율표/elements_data.js"
if os.path.exists(target_file):
    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = content.replace("const elementsData = ", "").replace(";", "").strip()
    elements = json.loads(content)
    
    for el in elements:
        text_to_search = (el.get("use", "") + " " + el.get("desc", "") + " " + el.get("fact", "")).lower()
        assigned_emoji = "🧪" # default fallback
        
        for keyword, emoji in keyword_to_emoji.items():
            if keyword in text_to_search:
                assigned_emoji = emoji
                break # First match wins
        
        el["emoji"] = assigned_emoji

    with open(target_file, "w", encoding="utf-8") as f:
        f.write("const elementsData = ")
        json.dump(elements, f, ensure_ascii=False, indent=2)
        f.write(";")
    
    print("Updated elements with emojis.")
else:
    print("File not found")
