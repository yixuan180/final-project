from planner.models import Destination, Travel_Themes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
from django.shortcuts import render
from django.conf import settings 

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

    # 這裡接前端骰子的結果）
    selected_theme = request.POST.get('theme')

    # 這裡接前端使用者給的縣市
    region = request.POST.get('region', '台北')

    region_mapping = {
        "keelung": "基隆",
        "taipei": "台北",
        "new_taipei": "新北",
        "taoyuan": "桃園",
        "hsinchu_city": "新竹",
        "miaoli": "苗栗",
        "taichung": "臺中",
        "changhua": "彰化",
        "nantou": "南投",
        "yunlin": "雲林",
        "chiayi_city": "嘉義",
        "tainan": "臺南",
        "kaohsiung": "高雄",
        "pingtung": "屏東",
        "yilan": "宜蘭",
        "hualien": "花蓮",
        "taitung": "臺東",
    }

    actual_region_name = region_mapping.get(region, region)

    # 根據縣市＋主題篩選景點
    try:
        # 1. 先根據名稱取得 Travel_Themes 物件
        theme_obj = Travel_Themes.objects.get(name=selected_theme)

        # 2. 使用 theme 物件進行精確篩選
        filtered_destinations = Destination.objects.filter(
            address__icontains=actual_region_name,
            theme=theme_obj  # <--- 將這裡改為精確匹配！
        )

    except Travel_Themes.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": f"選定的主題 '{selected_theme}' 不存在。",
            "data": [],
        }, status=500)
    except Exception as e:
        print(f"篩選目的地時發生錯誤: {e}")
        return JsonResponse({
            "success": False,
            "message": "數據庫查詢錯誤，請確認模型關係和字段名稱。",
            "data": None
        }, status=500)

    if not filtered_destinations.exists():
        return JsonResponse({
            "success": False,
            "message": f"在「{actual_region_name}」中找不到主題為「{selected_theme}」的景點。請嘗試其他選項。",
            "theme": selected_theme,
            "data": []
        })

    selected = random.sample(list(filtered_destinations), min(6, len(filtered_destinations)))

    data = [{
        "id": d.id,
        "name": d.name,
        "description": d.description,
        "image_url": d.image_url,
        "address": d.address,
        "category": d.category,
        "opening_hours":d.opening_hours,
        "contact_info":d.contact_info,
        "theme": d.theme.name # 這個是從資料庫取出的景點主題
    } for d in selected]

    return JsonResponse({
        "success": True,
        "message": f"🎲 你擲出的主題是「{selected_theme}」，這是我們在「{region}」推薦的行程景點！",
        "theme": selected_theme, # 這個是隨機骰出的主題
        "data": data
    })