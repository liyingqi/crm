from django import template
from django.shortcuts import redirect, reverse
from django.utils.safestring import mark_safe

register = template.Library()  # register的名字是固定的,不可改变


@register.simple_tag
def url_reversr(request, name,*args,**kwargs):
    base_url = reverse(name,args=args,kwargs=kwargs)
    old_url = request.get_full_path()
    dic = request.GET.copy()
    dic['return'] = old_url
    return '%s?%s'%(base_url,dic.urlencode())
