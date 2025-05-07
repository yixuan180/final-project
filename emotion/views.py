# 在 emotion/views.py 裡加這段：

from django.http import JsonResponse

def generate_by_emotion(request):
    return JsonResponse({'message': '這是根據情緒生成的行程！'})
