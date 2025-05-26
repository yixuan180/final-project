from planner.models import Destination
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
from django.shortcuts import render # 確保這裡有導入 render

def fate_dice_view(request):
    return render(request, 'fate_dice.html')

def emotion_view(request): # 如果情緒導向推薦也有獨立頁面，你需要這個
    return render(request, 'emotion.html')

def result_view(request): # **新增這個函式**，用於渲染 result.html
    return render(request, 'result.html')

@csrf_exempt
def roll_dice(request):
    if request.method != 'POST':
        return JsonResponse({
            "success": False,
            "message": "只接受 POST 請求",
            "data": None
        }, status=405)

    selected_theme = request.POST.get('theme')
    region = request.POST.get('region')

    if not selected_theme:
        return JsonResponse({
            "success": False,
            "message": "缺少旅遊主題資訊",
            "data": None
        }, status=400)
    
    if not region:
        return JsonResponse({
            "success": False,
            "message": "缺少縣市資訊",
            "data": None
        }, status=400)

    # 確保你的 Destination model 有 address 和 theme 字段
    filtered_destinations = Destination.objects.filter(
        address__icontains=region,
        theme__icontains=selected_theme
    )
    
    num_to_select = min(5, len(filtered_destinations))
    if num_to_select == 0:
        selected_destinations = []
        message_suffix = "，但該縣市此主題沒有相關景點。"
    else:
        selected_destinations = random.sample(list(filtered_destinations), num_to_select)
        message_suffix = f"！找到 {num_to_select} 個推薦景點。"
        if num_to_select < 5:
            message_suffix = f"！找到 {num_to_select} 個推薦景點 (不足 5 個)。"


    data = [{
        "id": d.id,
        "name": d.name,
        "description": d.description,
        "image_url": d.image_url.url if d.image_url else None, # 確保能獲取圖片 URL
        "address": d.address,
        "category": d.get_category(), # 假設 get_category() 函式存在於 Destination model
    } for d in selected_destinations]

    return JsonResponse({
        "success": True,
        "message": f"🎲 你擲出的主題是「{selected_theme}」，這是我們在「{region}」推薦的行程景點{message_suffix}",
        "theme": selected_theme, # 將主題也傳回前端
        "region": region, # 將縣市也傳回前端
        "data": data
    })