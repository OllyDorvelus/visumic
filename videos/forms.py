__author__ = 'OllyD'
from django import forms
from .models import CommentModel, VideoModel, ShareModel, GenreModel, PlaylistModel


class CommentModelForm(forms.ModelForm):
    comment = forms.CharField(label='',
                              widget=forms.Textarea
                              (attrs={'placeholder': "Comment", "class": "form-control"}))
    class Meta:
        model = CommentModel
        fields = ['comment']

class CommentEditForm(forms.ModelForm):
    comment = forms.CharField(label='',
                              widget=forms.Textarea
                              (attrs={"class": "form-control comment"}))
    class Meta:
        model = CommentModel
        fields = ['comment']

# class ReplyCommentModelForm(forms.ModelForm):
#     comment = forms.CharField(label='',
#                               widget=forms.Textarea
#                               (attrs={'placeholder': "Comment", "class": "form-control"}))
#     class Meta:
#         model = CommentModel
#         fields = ['comment']


class VideoModelForm(forms.ModelForm):
    class Meta:
        model = VideoModel
        fields = ['title', 'video', 'thumbnail', 'description', 'genre']




class ShareModelForm(forms.ModelForm):
    content = forms.CharField(label='',
                              widget=forms.Textarea
                              (attrs={'placeholder': "Why are you sharing?", "class": "form-control sharetext"}))
    class Meta:
        model = ShareModel
        fields = ['content']

class ShareEditForm(forms.ModelForm):
    content = forms.CharField(label='',
                              widget=forms.Textarea
                              (attrs={"class": "form-control content"}))
    class Meta:
        model = ShareModel
        fields = ['content']

class VideoEditForm(forms.ModelForm):
    title = forms.CharField(label='',
                              widget=forms.TextInput
                              (attrs={"class": "form-control title"}))




    class Meta:
        model = VideoModel
        fields = ['title', 'description', 'genre']

    def __init__(self, *args, **kwargs):
        super(VideoEditForm, self).__init__(*args, **kwargs)
        self.fields['genre'].required = False
      #  self.fields['thumbnail'].required = False

class PlaylistModelForm(forms.ModelForm):
    name = forms.CharField(label='',
                              widget=forms.TextInput
                              (attrs={'placeholder': "Playlist Name", "class": "form-control"}))
    class Meta:
        model = PlaylistModel
        fields = ['name']

class PlaylistEditForm(forms.ModelForm):
    name = forms.CharField(label='',
                              widget=forms.TextInput
                              (attrs={"class": "form-control name"}))




    class Meta:
        model = PlaylistModel
        fields = ['name', 'description']