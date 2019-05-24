from django import template
from collections import OrderedDict
from django.conf import settings

register = template.Library()


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    '''
    动态生成菜单的自定义过滤器
    :param request: template传过来的request对象,用于获取中间件封装的属性或者session中的值
    :return:
    '''
    #获取菜单字典
    menu_dic = request.session.get(settings.MENU_SESSION_KEY)
    #通过collections模块的OrderedDict类实例化一个有序空字典
    order_dic = OrderedDict()
    #通过menu_dic中对应的权重字段用sorted函数排序,拿到通过权重拍完序的原字典的key
    for key in sorted(menu_dic, key=lambda k: menu_dic[k]['weight'], reverse=True):
        #循环排好序的字典的数据初始化有序字典
        dic = order_dic[key] = menu_dic[key]        #dic等价于for dic in order_dic.values()的第一次循环出的第一级菜单的信息
        #把每个一级菜单中添加一个class='hide'的属性
        dic['class'] = 'hide'
        for sec_dic in dic['children']:
            #循环出每个二级菜单的信息
            if sec_dic['id'] == request.menu_current_id:
                # 如果二级菜单的id等于用户输入的目标url的id,在这个二级菜单中添加一个class='active'的属性
                # 把他对应的一级菜单中class属性置空
                sec_dic['class'] = 'active'
                dic['class'] = ''
    #最后返回字典的values,每个值对应的是一个字典
    return {'menu_list': order_dic.values()}


@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    '''
    动态生成路径导航的自定义过滤器
    :param request:
    :return:
    '''
    breadcrumb_list = request.breadcrumb_list
    return {'breadcrumb_list': breadcrumb_list}

@register.filter
def has_permission(request,name):
    '''
    基于按钮的权限控制
    :param request:
    :param name:
    :return:
    '''
    #取出权限字典,每个key为url反向解析的名字
    permission_dic = request.session.get(settings.PERMISSION_SESSION_KEY)
    #如果template传过来的name在权限字典中,说明有权限,返回True
    if name in permission_dic:
        return True



@register.simple_tag
def gen_role_url(request, rid):
    params = request.GET.copy()
    params['rid'] = rid
    return params.urlencode()
