from django.contrib import admin
from .models import VideoModel, CommentModel, ShareModel, ShareCommentModel, PlaylistModel, GenreModel
# Register your models here.


class VideoModelAdmin(admin.ModelAdmin):
    # form = TweetModelForm
    list_display = ["id", "title", 'description', 'user', 'genre']
    list_filter = ['id']
    class Meta:
        model = VideoModel

class CommentModelAdmin(admin.ModelAdmin):
    # form = TweetModelForm
    list_display = ["id", "comment", 'parent', 'reply', 'video', 'user', 'timestamp']
    list_filter = ['id']
    class Meta:
        model = CommentModel

class ShareModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", 'video', 'content', 'timestamp']
    list_filter = ['id']
    class Meta:
        model = ShareModel


class PlaylistModelAdmin(admin.ModelAdmin):
    list_display = ["id", 'name', "user", 'timestamp']
    list_filter = ['id']
    class Meta:
        model = PlaylistModel

class GenreModelAdmin(admin.ModelAdmin):
    list_display = ["genrename", 'parent']
    list_filter = ['id']
    class Meta:
        model = GenreModel


admin.site.register(VideoModel, VideoModelAdmin)
admin.site.register(CommentModel, CommentModelAdmin)
admin.site.register(ShareModel, ShareModelAdmin)
admin.site.register(ShareCommentModel)
admin.site.register(PlaylistModel, PlaylistModelAdmin)
admin.site.register(GenreModel)