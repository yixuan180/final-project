from django.db import models
from django.contrib.auth.models import User
from planner.models import Travel_Themes 
import json

# Create your models here.

class Theme_Random_Dice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dice_rolls', verbose_name="使用者")
    theme = models.ForeignKey(Travel_Themes, on_delete=models.CASCADE, related_name='dice_rolls', verbose_name="旅行主題")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="擲骰時間")

    def __str__(self):
        return f"{self.user.username}的骰子結果 ({self.theme.name}) - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        verbose_name = "主題隨機骰子"
        verbose_name_plural = "主題隨機骰子"
        ordering = ['-created_at']

