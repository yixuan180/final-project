from django.db import models
from django.contrib.auth.models import User
from emotion.models import Emotion_Type  # 引入情緒類型
import json

class Travel_Themes(models.Model):
    name = models.CharField(max_length=100, verbose_name="主題名稱")
    description = models.TextField(verbose_name="主題描述")
    image_url = models.URLField(verbose_name="主題URL")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="創建時間")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "旅行主題"
        verbose_name_plural = "旅行主題"

class Destination(models.Model):
    name = models.CharField(max_length=200, verbose_name="景點名稱")
    description = models.TextField(verbose_name="景點描述")
    address = models.TextField(verbose_name="地址")
    latitude = models.FloatField(verbose_name="緯度")
    longitude = models.FloatField(verbose_name="經度")
    image_url = models.URLField(verbose_name="景點圖片URL")
    theme = models.ForeignKey(Travel_Themes, on_delete=models.CASCADE, related_name='destinations', verbose_name="旅行主題")
    category = models.TextField(verbose_name="類別")
    suitable_emotions = models.ManyToManyField(Emotion_Type, related_name='suitable_destinations', verbose_name="適合情緒類型", blank=True)
    opening_hours = models.TextField(verbose_name="營業時間")
    min_price = models.FloatField(verbose_name="最低費用")
    max_price = models.FloatField(verbose_name="最高費用") 
    duration = models.IntegerField(verbose_name="預計遊覽時間（分鐘）")
    contact_info = models.TextField(verbose_name="景點聯絡資訊")

    def __str__(self):
        return self.name
    
    def set_category(self, category_list):
        self.category = json.dumps(category_list)

    def get_category(self):
        return json.loads(self.category)
    
    class Meta:
        verbose_name = "景點"
        verbose_name_plural = "景點"

class Activities(models.Model):
    name = models.CharField(max_length=200, verbose_name="活動名稱")
    description = models.TextField(verbose_name="活動描述")
    location = models.CharField(max_length=200, verbose_name="活動地點")
    image_url = models.URLField(verbose_name="圖片網址")
    theme = models.ForeignKey(Travel_Themes, on_delete=models.CASCADE, related_name='activities', verbose_name="旅行主題")
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='activities', verbose_name="關聯景點")
    recommended_for = models.TextField(verbose_name="適合的旅行主題")  # 存儲JSON格式的推薦主題
    suitable_emotions = models.ManyToManyField(Emotion_Type, related_name='suitable_activities', verbose_name="適合情緒類型", blank=True)
    min_price = models.FloatField(verbose_name="最低費用")
    max_price = models.FloatField(verbose_name="最高費用")
    duration = models.IntegerField(verbose_name="活動時間(分鐘)")
    
    def __str__(self):
        return self.name
    
    def set_recommended_for(self, recommended_list):
        self.recommended_for = json.dumps(recommended_list)
    
    def get_recommended_for(self):
        return json.loads(self.recommended_for)
    
    class Meta:
        verbose_name = "活動"
        verbose_name_plural = "活動"


class Itinerary(models.Model):
    """行程模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='itineraries', verbose_name="使用者")
    theme = models.ForeignKey(Travel_Themes, on_delete=models.CASCADE, related_name='itineraries', verbose_name="行程主題")
    destination_ids = models.TextField(verbose_name="景點ID列表")  # 存儲JSON格式的目的地ID數組
    activity_ids = models.TextField(verbose_name="活動ID列表")  # 存儲JSON格式的活動ID數組
    start_date = models.DateField(verbose_name="行程開始日期")
    end_date = models.DateField(verbose_name="行程結束日期")
    min_budget = models.FloatField(verbose_name="最低預算")
    max_budget = models.FloatField(verbose_name="最高預算")
    
    def __str__(self):
        return f"{self.user.username}的行程 ({self.start_date} - {self.end_date})"
    
    def set_destination_ids(self, id_list):
        self.destination_ids = json.dumps(id_list)
    
    def get_destination_ids(self):
        return json.loads(self.destination_ids)
    
    def set_activity_ids(self, id_list):
        self.activity_ids = json.dumps(id_list)
    
    def get_activity_ids(self):
        return json.loads(self.activity_ids)
    
    class Meta:
        verbose_name = "行程"
        verbose_name_plural = "行程"