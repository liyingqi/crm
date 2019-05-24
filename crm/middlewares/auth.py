from django.utils.deprecation import MiddlewareMixin
from crm import models
from django.shortcuts import redirect,reverse

class Auth_Session(MiddlewareMixin):
    def process_request(self,request):
        if request.path in [reverse('login'),reverse('reg')]:
            return None
        user_id = request.session.get('user_id')

        ret = models.UserProfile.objects.filter(id=user_id).first()
        if ret:
            request.user_id = user_id
            request.user_obj = ret
            return None
        else:
            return redirect(reverse('login'))