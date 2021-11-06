from django.forms import ModelForm
from .models import Post, User
from django.contrib.auth.forms import UserCreationForm


class PostForm(ModelForm):
    class Meta:
        model = Post
        fiedlds = "__all__"
        exclude = ["owner", "likes"] 

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

class EditUserform(ModelForm):
    class Meta:
        model = User
        fields = ["avatar", "username", "bio"]