from planner.models import Destination
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

    # 這裡接前端使用者給的情緒
    emotion = request.POST.get('emotion', '放鬆')

    # 這裡接前端使用者給的縣市
    region = request.POST.get('region', '台北')

    # 根據縣市與主題篩選景點
    filtered_destinations = Destination.objects.filter(
        address__icontains=region,
        emotion_type__icontains=emotion
    )
    
    # 隨機抽三個景點
    selected = random.sample(list(filtered_destinations), min(3, len(filtered_destinations)))

    # 建立包含活動的資料結構
    data = [{
        "id": d.id,
        "name": d.name,
        "description": d.description,
        "image_url": d.image_url,
        "address": d.address,
        "category": d.get_category(),
        "price_range": f"{d.min_price} ~ {d.max_price}"
    } for d in selected]

    return JsonResponse({
        "success": True,
        "message": f"🎲 你選擇的情緒是「{emotion}」，這是我們在「{region}」推薦的行程景點！",
        "emotion": emotion,
        "data": data
    })
