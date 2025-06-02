from planner.models import Destination
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
from django.shortcuts import render, get_object_or_404

def emotion_view(request): # 如果情緒導向推薦也有獨立頁面，你需要這個
    return render(request, 'emotion.html')

def emotion_result_view(request):
    return render(request, 'emotionResult.html')

def emotion_detail(request, id):
    destination = get_object_or_404(Destination, pk=id)
    return render(request, 'emotionDetail.html', {'destination': destination})

@csrf_exempt
def generate_by_emotion(request):
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

    filtered_destinations = Destination.objects.filter(
        address__icontains=region,
        suitable_emotions__name__icontains=emotion
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
        "category": d.category,
        "opening_hours":d.opening_hours,
        "contact_info":d.contact_info
    } for d in selected]

    return JsonResponse({
        "success": True,
        "message": f"🎲 你選擇的情緒是「{emotion}」，這是我們在「{region}」推薦的行程景點！",
        "emotion": emotion,
        "data": data
    })
