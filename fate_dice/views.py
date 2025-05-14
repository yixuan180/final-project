from planner.models import Destination, Activities
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random

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

    # 根據縣市＋主題篩選景點
    filtered_destinations = Destination.objects.filter(
        address__icontains=region,
        theme__name__icontains=selected_theme
    )
    
    # 隨機抽五個
    selected = random.sample(list(filtered_destinations), min(5, len(filtered_destinations)))

    # 建立包含活動的資料結構
    data = []
    for d in selected:
        # 找出這個景點的所有活動
        activity_list = Activities.objects.filter(destination=d)

        activity_data = [{
            "id": a.id,
            "name": a.name,
            "description": a.description,
            "image_url": a.image_url,
            "location": a.location,
            "price_range": f"{a.min_price} ~ {a.max_price}",
            "duration": a.duration
        } for a in activity_list]

        data.append({
            "id": d.id,
            "name": d.name,
            "description": d.description,
            "image_url": d.image_url,
            "address": d.address,
            "category": d.get_category(),
            "price_range": f"{d.min_price} ~ {d.max_price}",
            "activities": activity_data  # <-- 多這個欄位
        })

    return JsonResponse({
        "success": True,
        "message": f"🎲 你擲出的主題是「{selected_theme}」，這是我們在「{region}」推薦的行程景點！",
        "theme": selected_theme,
        "data": data
    })