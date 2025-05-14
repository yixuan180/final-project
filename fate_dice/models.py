from django.db import models
from django.contrib.auth.models import User
from planner.models import Travel_Themes, Destination, Activities, Itinerary
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

class Destination(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dice_destinations', verbose_name="使用者")
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='dice_entries', verbose_name="隨機景點")
    theme_dice = models.ForeignKey(Theme_Random_Dice, on_delete=models.CASCADE, related_name='destinations', verbose_name="關聯主題擲骰")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="擲骰時間")
    
    def __str__(self):
        return f"{self.user.username}的景點骰子結果: {self.destination.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        verbose_name = "景點骰子"
        verbose_name_plural = "景點骰子"
        ordering = ['-created_at']

class Activities(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dice_activities', verbose_name="使用者")
    activity = models.ForeignKey(Activities, on_delete=models.CASCADE, related_name='dice_entries', verbose_name="隨機活動")
    destination_dice = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='activities', verbose_name="關聯景點擲骰")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="擲骰時間")
    
    def __str__(self):
        return f"{self.user.username}的活動骰子結果: {self.activity.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        verbose_name = "活動骰子"
        verbose_name_plural = "活動骰子"
        ordering = ['-created_at']

class Itinerary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dice_itineraries', verbose_name="使用者")
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='dice_source', verbose_name="生成的行程", null=True, blank=True)
    theme_dice = models.ForeignKey(Theme_Random_Dice, on_delete=models.CASCADE, related_name='itineraries', verbose_name="使用的主題骰子")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="生成時間")
    
    def __str__(self):
        return f"{self.user.username}的骰子生成行程 - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        verbose_name = "骰子行程"
        verbose_name_plural = "骰子行程"
        ordering = ['-created_at']