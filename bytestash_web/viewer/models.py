# app/models.py

from django.db import models

# 전체 추가 바꾸기전 빈칸
class Comment(models.Model):
    snippet_id = models.IntegerField()  # FastAPI 스니펫 ID 참조용
    author = models.CharField(max_length=100, default="익명")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.content[:20]}"

class ResolvedSnippet(models.Model):
    snippet_id = models.IntegerField(unique=True)
    marked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"해결됨 스니펫 ID: {self.snippet_id}"