from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from music.models import UserProfile


def cold_boot(function):
    def \
            wrapper(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            profile = UserProfile.objects.filter(user=request.user)
            if profile.exists():
                profile_obj: UserProfile = profile.first()
                if profile_obj.first_run:
                    messages.warning(request, '首次登录请先订阅喜欢的音乐流派和语言')
                    return HttpResponseRedirect('/user')
            else:
                messages.error(request, '找不到用户资料，请重新登录')
                logout(request)
                return HttpResponseRedirect('/')

        return function(request, *args, **kwargs)

    return wrapper
