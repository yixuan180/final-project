from django.db import models
from planner.models import Users
import json

class Emotion(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    emotion_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """返回情緒記錄的文字表示"""
        return f"{self.user.username}的{self.emotion_type}情緒 - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        """Meta 類別提供模型的額外屬性"""
        verbose_name = "使用者情緒"
        verbose_name_plural = "使用者情緒"
        ordering = ['-created_at']  # 預設按創建時間倒序排序
        
    def get_emotion_data(self):
        """獲取情緒數據的輔助方法"""
        return {
            'emotion_type': self.emotion_type,
            'timestamp': self.created_at.isoformat(),
            'user_id': self.user.id
        }