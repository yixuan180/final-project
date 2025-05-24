from planner.models import Destination
import json
import re
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# 設定 Gemini API 金鑰
genai.configure(api_key="AIzaSyAGsPf8khZvCh6g_4PIhQ1ltUJKV-11lu0")

@csrf_exempt
def generate_itinerary(request):
    if request.method != 'POST':
        return JsonResponse({
            "success": False,
            "message": "只接受 POST 請求",
            "data": None
        }, status=405)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "success": False,
            "message": "JSON 格式錯誤",
            "data": None
        }, status=400)

    # 這裡要串前端的接收用戶的輸入
    region = data.get('region', '台中')
    budget = float(data.get('budget', 6000))
    theme = data.get('theme', '美食之旅')
    start_date = data.get('start_date', '2025-06-01')
    end_date = data.get('end_date', '2025-06-04')



    # 過濾符合主題與地區的景點
    destinations = list(Destination.objects.filter(
        address__icontains=region,
        theme__name__icontains=theme
    ))

    print("📍找到景點數量：", len(destinations))
    for d in destinations:
        print("🔹", d.name, "-", d.address, "-", d.theme.name)


    prompt = build_prompt(destinations, region, start_date, end_date, budget, theme)

    try:
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        response = model.generate_content(prompt)

        itinerary_text = response.text.strip()

        parsed_itinerary = parse_itinerary_to_json(itinerary_text)

        return JsonResponse({
            "success": True,
            "message": "行程生成成功",
            "data": parsed_itinerary
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": f"行程生成失敗：{str(e)}",
            "data": None
        }, status=500)

def build_prompt(destinations, region, start_date, end_date, budget, theme):
    destination_list = "\n".join([f"- {d.name}：{d.description}" for d in destinations])

    prompt = f"""
你是一位台灣旅遊行程規劃師，請根據以下條件為我設計一份完整的行程。請用繁體中文生成並保證以下所有條件：

條件：
- 地區：{region}
- 預算：{budget} 元
- 行程日期範圍：{start_date} ~ {end_date}
- 主題：{theme}
- 僅使用以下景點與活動：

景點：
{destination_list}

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