import re
import json
import random
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# 載入 API 金鑰（建議從 .env）
genai.configure(api_key="AIzaSyAGsPf8khZvCh6g_4PIhQ1ltUJKV-11lu0")

@csrf_exempt
def roll_dice(request):
    if request.method != 'POST':
        return JsonResponse({
            "success": False,
            "message": "只接受 POST 請求",
            "data": None
        }, status=405)

    # 接收參數
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        return JsonResponse({"success": False, "message": "請傳送 JSON 格式", "data": None}, status=400)

    start_date = data.get('start_date', '2025-06-01')
    end_date = data.get('end_date', '2025-06-04')
    budget = data.get('budget', 6000)

    # 1. 隨機擲骰選主題
    themes = ["美食之旅","自然風景","文化歷史","冒險活動","購物娛樂","休閒放鬆"]

    selected_theme = random.choice(themes)

    # 2. 景點 & 活動清單（跟之前一樣）
    destinations = [
        {"name": "台北故宮博物院", "description": "擁有世界上最珍貴的中國藝術品，是了解中國歷史文化的最佳場所。"},
        {"name": "101大樓", "description": "台北的地標，提供絕佳的市區全景觀，還有購物與餐飲設施。"},
        {"name": "士林夜市", "description": "台北最大的夜市之一，擁有豐富的小吃和遊戲設施。"},
        {"name": "陽明山國家公園", "description": "以其壯麗的自然景觀和溫泉聞名，是登山健行和放鬆的好地方。"},
        {"name": "龍山寺", "description": "台北最古老且具有歷史意義的寺廟之一，著名的宗教與文化地標。"},
        {"name": "西門町", "description": "台北的潮流中心，充滿了年輕的氛圍，擁有眾多的購物、餐飲和娛樂場所。"},
        {"name": "淡水老街", "description": "著名的歷史街區，擁有古老的建築和美麗的河岸景觀，適合散步和購物。"},
        {"name": "中正紀念堂", "description": "紀念蔣中正的建築，擁有壯麗的園區和歷史背景。"}
    ]
    activities = [
        {"name": "夜市探索", "description": "在台灣各大夜市中享受地道的美食"},
        {"name": "登山健行", "description": "攀登台灣知名山脈，享受自然風光"},
        {"name": "溫泉放鬆", "description": "在陽明山或北投享受天然溫泉，放鬆身心"},
        {"name": "文化之旅", "description": "參觀台北的博物館與歷史遺址，了解台灣的文化與歷史"},
        {"name": "美食之旅", "description": "品嚐台灣各式傳統美食，如滷肉飯、蚵仔煎、珍珠奶茶等"},
        {"name": "夜景觀賞", "description": "前往象山、101大樓或其他觀景點欣賞台北的壯麗夜景"},
        {"name": "城市漫遊", "description": "在台北的各大商圈（如西門町、信義區）漫遊，探索街頭文化與購物"},
        {"name": "文創探索", "description": "探索台北的文創園區，如華山1914文化創意產業園區"},
        {"name": "自行車騎行", "description": "租借自行車騎行於淡水河岸或大稻埕河岸"},
        {"name": "水上活動", "description": "在淡水或基隆海域進行划獨木舟、潛水或浮潛"},
        {"name": "購物巡禮", "description": "在台北的各大購物中心與特色商店購物"},
        {"name": "宗教朝聖", "description": "參拜龍山寺、行天宮等地"},
        {"name": "日式庭園漫遊", "description": "走訪圓山附近的日式庭園，感受日式氛圍"},
        {"name": "攝影之旅", "description": "探索台北隱藏景點，捕捉街頭與自然風光"},
        {"name": "手作體驗", "description": "參加陶藝、木工等台灣特色手作工作坊"}
    ]

    # 3. 建立 prompt，加入「由命運骰子選出主題：{selected_theme}」
    prompt = build_prompt(destinations, activities, start_date, end_date, budget, selected_theme)

    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content(prompt)
        itinerary_text = response.text.strip()
        parsed_itinerary = parse_itinerary_to_json(itinerary_text)

        return JsonResponse({
            "success": True,
            "message": f"已為你擲出主題：{selected_theme}，以下是推薦行程 ✨",
            "theme": selected_theme,
            "data": parsed_itinerary
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": f"行程生成失敗：{str(e)}",
            "data": None
        }, status=500)
    
def build_prompt(destinations, activities, start_date, end_date, budget, preference):
    destination_list = "\n".join([f"- {d['name']}：{d['description']}" for d in destinations])
    activity_list = "\n".join([f"- {a['name']}：{a['description']}" for a in activities])

    prompt = f"""
你是一位台灣旅遊行程規劃師，請根據以下條件為我設計一份完整的行程。請用繁體中文生成並保證以下所有條件：

條件：
- 預算：{budget} 元
- 行程日期範圍：{start_date} ~ {end_date}
- 主題：{preference}
- 僅使用以下景點與活動：

景點：
{destination_list}

活動：
{activity_list}

請用文字生成以下行程（每天都包含早上、下午、晚上三個時段的活動安排），並按照以下範本來回覆：

範本：
第一天（2025/06/01）
- 早上：活動描述
- 下午：活動描述
- 晚上：活動描述

第二天（2025/06/02）
- 早上：活動描述
- 下午：活動描述
- 晚上：活動描述

請確保每一天都具體描述活動，不要只列出地點名稱，要講「做什麼、去哪裡、感受如何」。
"""
    return prompt

def parse_itinerary_to_json(itinerary_text):
    day_blocks = re.split(r'\n(?=第[一二三四五六七]天（\d{4}/\d{2}/\d{2}）)', itinerary_text)
    result = []

    for day_block in day_blocks:
        if not day_block.strip():
            continue

        day_match = re.search(r'(第[一二三四五六七]天（\d{4}/\d{2}/\d{2}）)', day_block)
        day_title = day_match.group(1) if day_match else "未知日期"

        morning = None
        afternoon = None
        evening = None

        morning_match = re.search(r'- 早上：(.*?)(?:- 下午：|- 晚上：|$)', day_block, re.S)
        if morning_match:
            morning = morning_match.group(1).strip()

        afternoon_match = re.search(r'- 下午：(.*?)(?:- 晚上：|$)', day_block, re.S)
        if afternoon_match:
            afternoon = afternoon_match.group(1).strip()

        evening_match = re.search(r'- 晚上：(.*)', day_block, re.S)
        if evening_match:
            evening = evening_match.group(1).strip()

        result.append({
            "day": day_title,
            "morning": morning,
            "afternoon": afternoon,
            "evening": evening
        })

    return result
