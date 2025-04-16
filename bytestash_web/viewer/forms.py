# app/forms.py
# 새로 추가한 파일 바꾸기전 없는 파일
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'content']
        widgets = {
            'author': forms.TextInput(attrs={'placeholder': '작성자'}),
            'content': forms.Textarea(attrs={'placeholder': '댓글을 입력하세요'}),
        }
