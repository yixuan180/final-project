from django.db import models

# 定義景點（Destination）模型
class Destination(models.Model):
    name = models.CharField(max_length=100)  # 景點名稱
    description = models.TextField()  # 景點描述
    location = models.CharField(max_length=100, blank=True)  # 地點

    def __str__(self):
        return self.name

# 定義活動（Activity）模型
class Activity(models.Model):
    name = models.CharField(max_length=100)  # 活動名稱
    description = models.TextField()  # 活動描述
    theme = models.ForeignKey('Theme', on_delete=models.CASCADE)  # 活動主題，與 Theme 表建立關聯
    destination = models.ManyToManyField(Destination, related_name='activities')  # 與景點的多對多關聯

    def __str__(self):
        return self.name

# 定義活動主題（Theme）模型
class Theme(models.Model):
    name = models.CharField(max_length=50)  # 主題名稱
    description = models.TextField()  # 主題描述

    def __str__(self):
        return self.name
