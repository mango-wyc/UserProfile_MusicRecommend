from django.contrib import admin
from .models import Music, UserProfile


# Register your models here.
@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ['song_name', 'song_length', 'genre_ids', 'artist_name', 'composer', 'lyricist', 'language']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user_id', 'user', 'first_run', 'genre_subscribe', 'language_subscribe']

    def user_id(self, obj: UserProfile):
        return obj.user.id
