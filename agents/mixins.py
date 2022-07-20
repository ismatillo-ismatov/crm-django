from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class OrganisorAndLoginMixin(AccessMixin):
    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_authenticated or not request.user.is_organisor:
            return redirect("app:list")
        return super().dispatch(request,*args,**kwargs)