import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def roll_dice(request):
    themes = {
        "自然探索": ["陽明山健行", "烏來瀑布探訪", "北投溫泉步道"],
        "在地文化": ["龍山寺參拜", "大稻埕古蹟巡禮", "艋舺剝皮寮歷史街區"],
        "美食之旅": ["士林夜市小吃巡禮", "永康街牛肉麵", "迪化街古早味探索"],
        "小眾秘境": ["象山秘境拍照", "深澳漁港日出", "青潭水庫步道"],
    }

    theme = random.choice(list(themes.keys()))
    itinerary = themes[theme]

    return JsonResponse({
        "success": True,
        "theme": theme,
        "recommendations": itinerary,
    })
