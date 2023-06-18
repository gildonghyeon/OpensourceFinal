from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question  # 사용할 모델
#         fields = ['subject', 'content']  # QuestionForm에서 사용할 Question 모델의 속성
#         labels = {
#             'subject': '제목',
#             'content': '내용',
#         }
#
# class AnswerForm(forms.ModelForm):
#     class Meta:
#         model = Answer
#         fields = ['content']
#         labels = {
#             'content': '답변내용',
#         }


class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(label="이메일")

class Meta:
    model = User
    fields = ("first_name", "last_name", "username", "password1", "password2", "email")