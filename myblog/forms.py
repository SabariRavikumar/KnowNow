from django import forms
from .models import Post, Category, Comment
from community.models import JoinUs


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'cat', 'post_tag', 'thumbnail', 'content','author']

        widgets = {
            'author': forms.TextInput(attrs={'class':'form-control','placeholder':'Author','value':'','id':'user','type':'hidden'}),

        }
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','body']

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','thumbnail']

class JoinUsForm(forms.ModelForm):
    class Meta:
        model = JoinUs
        fields = '__all__'
 
