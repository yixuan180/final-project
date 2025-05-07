import re
import json
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# 設定 API 金鑰
genai.configure(api_key="AIzaSyCABin-XMUmwI2eZvqG39nICM49dCvx-nE")

@csrf_exempt
def generate_itinerary(request):
    if request.method == 'POST':
        # 定義目的地與活動
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
            {"name": "文創探索", "description": "探索台北的文創園區，如華山1914文化創意產業園區，體驗藝術和創意產品"},
            {"name": "自行車騎行", "description": "租借自行車騎行於淡水河岸或大稻埕河岸，享受台北的美麗風光"},
            {"name": "水上活動", "description": "在淡水或基隆海域進行水上活動，如划獨木舟、潛水或浮潛"},
            {"name": "購物巡禮", "description": "在台北的各大購物中心與特色商店尋找手信與時尚商品"},
            {"name": "宗教朝聖", "description": "參拜台北的著名寺廟，如龍山寺、行天宮，感受台灣的宗教氛圍"},
            {"name": "日式庭園漫遊", "description": "走訪台北的日式庭園，如圓環附近的日式花園，感受悠閒的日式氛圍"},
            {"name": "攝影之旅", "description": "探索台北的隱藏景點，捕捉美麗的街頭風光與自然景色"},
            {"name": "手作體驗", "description": "參加台北的陶藝、木工或手工藝體驗工作坊，學習製作台灣特色手工藝品"}
        ]


        # 接收用戶輸入
        start_date = request.POST.get('start_date', '2025-06-01')
        end_date = request.POST.get('end_date', '2025-06-02')
        budget = request.POST.get('budget', 30000)
        preference = request.POST.get('preference', 'Adventure')

        # 建立提示語
        prompt = build_prompt(destinations, activities, start_date, end_date, budget, preference)

        try:
            # 設置模型
            model = genai.GenerativeModel(
                model_name="gemini-1.5-pro",  # 使用 gemini-1.5-pro 模型
            )

            # 生成回應內容
            response = model.generate_content(prompt)

            # 取得生成的行程文字
            itinerary = response.text.strip()

            return JsonResponse({'itinerary': itinerary})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

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

請用文字生成以下行程（每天都包含上午、下午、晚上三個時段的活動安排），並按照以下範本來回覆：

範本：
第一天（2025/06/01）
- 早上：活動描述
- 下午：活動描述
- 晚上：活動描述

第二天（2025/06/02）
- 早上：活動描述
- 下午：活動描述
- 晚上：活動描述

...

請保證每一天都包括具體活動和時間段，不要簡單的列出景點或活動名稱，要提供具體的活動描述。
"""

    return prompt



