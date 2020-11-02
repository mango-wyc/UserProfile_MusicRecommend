import pandas as pd
from django.contrib import messages
from django.http import HttpRequest
from surprise import SVD, KNNBasic
from surprise import Dataset, Reader, Prediction

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from django.contrib.auth.models import User
from music.models import UserProfile, Music

current_request = None


def build_df():
    data = []
    for user_profile in UserProfile.objects.all():
        for like_music in user_profile.likes.all():
            data.append([user_profile.user.id, like_music.pk, 1])
        for dislike_music in user_profile.dislikes.all():
            data.append([user_profile.user.id, dislike_music.pk, 0])

    return pd.DataFrame(data, columns=['userID', 'itemID', 'rating'])


def build_predictions(df: pd.DataFrame, user: User):
    userId = user.id
    profile = UserProfile.objects.filter(user=user)
    if profile.exists():
        profile_obj: UserProfile = profile.first()
    else:
        return []

    # 先构建训练集，用SVD训练，再把所有评分过的歌曲放到测试集里，
    # 接着把测试集的数据通过训练的算法放到结果集里
    reader = Reader(rating_scale=(0, 1))
    data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)
    # 构建训练集
    trainset = data.build_full_trainset()
    # 构建算法并训练  e.g有限邻算法
    algo = SVD()
    # 数据拟合
    algo.fit(trainset)

    # 取出当前所有有人评分过的歌曲
    subsets = df[['itemID']].drop_duplicates()
    # 测试集
    testset = []
    for row in subsets.iterrows():
        testset.append([userId, row[1].values[0], 0])
#通过测试集构建预测集
    predictions = algo.test(testset, verbose=True)
    result_set = []

    user_like = profile_obj.likes.all()
    user_dislike = profile_obj.dislikes.all()

    for item in predictions:
        prediction: Prediction = item
        if prediction.est > 0.99:
            music = Music.objects.get(pk=prediction.iid)
            # 去重，不推荐用户已经喜欢的 或不喜欢的音乐
            if music in user_like:
                continue
            if music in user_dislike:
                continue
            result_set.append(music)

    if len(result_set) == 0:
        messages.error(current_request, '你听的歌太少了，多听点歌再来吧~')

    return result_set


def build_genre_predictions(user: User):
    predictions = []
    profile = UserProfile.objects.filter(user=user)
    if profile.exists():
        profile_obj: UserProfile = profile.first()
    else:
        return predictions

    genre_subscribe = profile_obj.genre_subscribe.split(',')
    user_like = profile_obj.likes.all()
    user_dislike = profile_obj.dislikes.all()

    for music in Music.objects.filter(genre_ids__in=genre_subscribe):
        if music in user_like:
            continue
        if music in user_dislike:
            continue
        predictions.append(music)

    return predictions


def build_language_predictions(user: User):
    predictions = []
    profile = UserProfile.objects.filter(user=user)
    if profile.exists():
        profile_obj: UserProfile = profile.first()
    else:
        return predictions

    language_subscribe = profile_obj.language_subscribe.split(',')
    user_like = profile_obj.likes.all()
    user_dislike = profile_obj.dislikes.all()

    for music in Music.objects.filter(language__in=language_subscribe):
        if music in user_like:
            continue
        if music in user_dislike:
            continue
        predictions.append(music)

    return predictions


def build_recommend(request: HttpRequest, user: User):
    global current_request
    current_request = request
    predictions = []
    predictions.extend(build_predictions(build_df(), user))
    predictions.extend(build_genre_predictions(user))
    predictions.extend(build_language_predictions(user))

    return predictions


if __name__ == '__main__':
    # print(build_df())
    # print(build_predictions(build_df(), User.objects.get(pk=4)))
    # print(build_genre_predictions(User.objects.get(pk=2)))
    # print(build_language_predictions(User.objects.get(pk=2)))
    print(build_recommend(User.objects.get(pk=2)))
