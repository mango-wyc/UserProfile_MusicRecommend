# 去除language空字符

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from music.models import UserProfile, Music

if __name__ == '__main__':
    music_set = Music.objects.all()
    total = len(music_set)
    for index, music in enumerate(music_set):
        music.language = music.language.replace('\n', '')
        music.save()

        print(f'{index + 1}/{total}: {music.song_name}')
