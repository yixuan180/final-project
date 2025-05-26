from planner.models import Destination, Travel_Themes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
from django.shortcuts import render

def fate_dice_view(request):
    return render(request, 'fate_dice.html')

@csrf_exempt
def roll_dice(request):
    if request.method != 'POST':
        return JsonResponse({
            "success": False,
            "message": "只接受 POST 請求",
            "data": None
        }, status=405)

    # 這裡幫我接前端骰子的結果）
    themes = ["美食之旅", "自然風景", "文化歷史", "冒險活動", "購物娛樂", "休閒放鬆"]
    selected_theme = random.choice(themes)

    # 這裡接前端使用者給的縣市
    region = request.POST.get('region', '台北')

    region_mapping = {
        "keelung": "基隆",
        "taipei": "台北",
        "new_taipei": "新北",
        "taoyuan": "桃園",
        "hsinchu_city": "新竹", # 假設新竹市的 value 是這個
        "miaoli": "苗栗",
        "taichung": "臺中", # 注意前端是臺中
        "changhua": "彰化",
        "nantou": "南投",
        "yunlin": "雲林",
        "chiayi_city": "嘉義", # 假設嘉義市的 value 是這個
        "tainan": "臺南", # 注意前端是臺南
        "kaohsiung": "高雄",
        "pingtung": "屏東",
        "yilan": "宜蘭",
        "hualien": "花蓮",
        "taitung": "臺東", # 注意前端是臺東
    }

    actual_region_name = region_mapping.get(region, region)

    # 根據縣市＋主題篩選景點
    try:
        filtered_destinations = Destination.objects.filter(
            address__icontains=actual_region_name, # address 是 TextField，直接使用 icontains
            theme__name__icontains=selected_theme # theme 是 ForeignKey，透過 __name 訪問 Travel_Themes 的 name 欄位
        )
    except Exception as e:
        print(f"篩選目的地時發生錯誤: {e}")
        return JsonResponse({
            "success": False,
            "message": "數據庫查詢錯誤，請確認模型關係和字段名稱。",
            "data": None
        }, status=500)

    # 隨機抽五個
    if not filtered_destinations.exists(): # 使用 .exists() 檢查 queryset 是否為空
        return JsonResponse({
            "success": False,
            "message": f"在「{actual_region_name}」中找不到主題為「{selected_theme}」的景點。請嘗試其他選項。",
            "theme": selected_theme,
            "data": []
        })

    
    # 隨機抽五個
    selected = random.sample(list(filtered_destinations), min(5, len(filtered_destinations)))

    data = [{
        "id": d.id,
        "name": d.name,
        "description": d.description,
        "image_url": d.image_url,
        "address": d.address,
        "category": d.get_category(),
        "theme": d.theme.name,
    } for d in selected]

    return JsonResponse({
        "success": True,
        "message": f"🎲 你擲出的主題是「{selected_theme}」，這是我們在「{region}」推薦的行程景點！",
        "theme": selected_theme,
        "data": data
    })