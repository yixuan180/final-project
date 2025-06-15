from planner.models import Destination
import json
import re
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render

def index_view(request):
    return render(request, 'index.html')

def planner_view(request):
    return render(request, 'planner.html')

def plannerResult_view(request):
    return render(request, 'plannerResult.html')

def loading_view(request):
    return render(request, 'loading.html')

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

    frontend_raw_region = data.get('region', 'taipei') 
    frontend_raw_theme = data.get('theme', 'food') 
    
    # 獲取其他參數
    budget = float(data.get('budget', 6000))
    start_date = data.get('start_date', '2025-06-01')
    end_date = data.get('end_date', '2025-06-04')

    region_mapping = {
        'keelung': '基隆',
        'taipei': '台北',
        'new_taipei': '新北',
        'taoyuan': '桃園',
        'hsinchu_city': '新竹',
        'miaoli': '苗栗',
        'taichung': '臺中',
        'changhua': '彰化',
        'nantou': '南投',
        'yunlin': '雲林',
        'chiayi_city': '嘉義',
        'tainan': '臺南',
        'kaohsiung': '高雄',
        'pingtung': '屏東',
        'yilan': '宜蘭',
        'hualien': '花蓮',
        'taitung': '臺東',
    }

    theme_mapping = {
        'food': '美食之旅',
        'nature': '自然風景',
        'culture': '文化歷史',
        'adventure': '冒險活動',
        'shopping': '購物娛樂',
        'relax': '休閒放鬆',
    }

    region_for_db_query = region_mapping.get(frontend_raw_region, frontend_raw_region) 
    theme_for_db_query = theme_mapping.get(frontend_raw_theme, frontend_raw_theme) 

    destinations = list(Destination.objects.filter(
        address__icontains=region_for_db_query, 
        theme__name__icontains=theme_for_db_query 
    ))
    
    print(f"前端傳遞的原始 region: {frontend_raw_region}, 原始 theme: {frontend_raw_theme}")
    print(f"轉換後用於資料庫查詢的 region: {region_for_db_query}, theme: {theme_for_db_query}") # 檢查這行！
    print(f"資料庫查詢條件：address__icontains='{region_for_db_query}', theme__name__icontains='{theme_for_db_query}'")
    print("📍找到景點數量：", len(destinations))
    for d in destinations:
        print("🔹", d.name, "-", d.address, "-", d.theme.name)

    prompt = build_prompt(destinations, region_for_db_query, start_date, end_date, budget, theme_for_db_query) 

    try:
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        response = model.generate_content(prompt)

        
        print("Gemini 原始回應:", response.text)

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
    result = []

    day_header_pattern = r'(?:\s*\*\*?)?[\s\*]*(第[一二三四五六七]天[（(]\s*\d{4}[/-]\d{2}[/-]\d{2}\s*[)）])[\s\*]*\n*'
    day_header_matches = list(re.finditer(day_header_pattern, itinerary_text))

    day_blocks = []
    if not day_header_matches:
        day_blocks.append(itinerary_text)
    else:
        for i, match in enumerate(day_header_matches):
            start_index = match.start()
            if i + 1 < len(day_header_matches):
                end_index = day_header_matches[i+1].start()
                day_blocks.append(itinerary_text[start_index:end_index])
            else:
                day_blocks.append(itinerary_text[start_index:])
    
    def clean_markdown(text):
        if text:
            text = re.sub(r'(\*\*|\*|__|_)', '', text) 
            text = re.sub(r'^[ \t]*[-*+]\s+', '', text, flags=re.MULTILINE)
            text = re.sub(r'\s+', ' ', text).strip()
        return text

    for day_block in day_blocks:
        if not day_block.strip():
            continue

        day_title = "未知日期"
        day_content_to_parse = day_block.strip()

        day_match_in_block = re.search(day_header_pattern, day_content_to_parse)
        if day_match_in_block:
            day_title = day_match_in_block.group(1).strip()
            day_content_to_parse = day_content_to_parse[day_match_in_block.end():].strip()
        
        morning = None
        afternoon = None
        evening = None
        
        # 早上：
        morning_match = re.search(
            r'(?:[\s\-\*]*?\s*)?(?:早上|上午)\s*(?:[\(（][^）)]*[\)）])?[：:]\s*([\s\S]*?)(?=\n*(?:(?:[\s\-\*]*?\s*)?(?:下午|晚上|中午|午間|黃昏|傍晚)[：:]|[\s\*]*(?:第[一二三四五六七]天[（(]\s*\d{4}[/-]\d{2}[/-]\d{2}\s*[)）])|\Z))',
            day_content_to_parse, re.DOTALL
        )
        if morning_match:
            morning = morning_match.group(1).strip()

        # 下午：
        afternoon_match = re.search(
            r'(?:[\s\-\*]*?\s*)?下午\s*(?:[\(（][^）)]*[\)）])?[：:]\s*([\s\S]*?)(?=\n*(?:(?:[\s\-\*]*?\s*)?(?:晚上|黃昏|傍晚)[：:]|[\s\*]*(?:第[一二三四五六七]天[（(]\s*\d{4}[/-]\d{2}[/-]\d{2}\s*[)）])|\Z))',
            day_content_to_parse, re.DOTALL
        )
        if afternoon_match:
            afternoon = afternoon_match.group(1).strip()

        # 晚上：
        evening_match = re.search(
            r'(?:[\s\-\*]*?\s*)?晚上\s*(?:[\(（][^）)]*[\)）])?[：:]\s*([\s\S]*?)(?=\n*(?:[\s\*]*(?:預算說明|預算分配|注意事項|備註)[：:]|[\s\*]*(?:第[一二三四五六七]天[（(]\s*\d{4}[/-]\d{2}[/-]\d{2}\s*[)）])|\Z))',
            day_content_to_parse, re.DOTALL
        )
        if evening_match:
            evening = evening_match.group(1).strip()
            
        # 統一清理所有時段的內容
        morning = clean_markdown(morning)
        afternoon = clean_markdown(afternoon)
        evening = clean_markdown(evening)

        result.append({
            "day": day_title,
            "morning": morning,
            "afternoon": afternoon,
            "evening": evening
        })

    return result