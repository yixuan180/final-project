from django.db import models
from django.contrib.auth.models import User
from emotion.models import Emotion_Type  # 引入情緒類型
import json

class Travel_Themes(models.Model):
    name = models.CharField(max_length=100, verbose_name="主題名稱")
    description = models.TextField(verbose_name="主題描述") #AI讀的時候可能還是會用到，所以留著

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "旅行主題"
        verbose_name_plural = "旅行主題"

class Destination(models.Model):
    name = models.CharField(max_length=200, verbose_name="景點名稱")
    description = models.TextField(verbose_name="景點描述")
    address = models.TextField(verbose_name="地址")
    image_url = models.URLField(verbose_name="景點圖片URL")
    theme = models.ForeignKey(Travel_Themes, on_delete=models.CASCADE, related_name='destinations', verbose_name="旅行主題")
    category = models.TextField(verbose_name="類別")
    suitable_emotions = models.ManyToManyField(Emotion_Type, related_name='suitable_destinations', verbose_name="適合情緒類型", blank=True)
    opening_hours = models.TextField(verbose_name="營業時間")
    min_price = models.FloatField(verbose_name="最低費用", blank=True, null=True)
    max_price = models.FloatField(verbose_name="最高費用", blank=True, null=True)
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