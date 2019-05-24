from django.conf import settings


def init_permission(request, user_obj):
    #通过登录的用户对象查询该对象所具有的权限,和权限相关菜单信息
    permission_query = user_obj.roles.all().filter(permissions__url__isnull=False).values('permissions__url',
                                                                                          'permissions__title',
                                                                                          'permissions__name',
                                                                                          'permissions__parent__name',
                                                                                          'permissions__id',
                                                                                          'permissions__parent__id',
                                                                                          'permissions__menu__name',
                                                                                          'permissions__menu__icon',
                                                                                          'permissions__menu__weight',
                                                                                          'permissions__menu__id').distinct()

    # 存放权限信息的字典
    permission_dic = {}
    # 存放菜单信息的字典
    menu_dict = {}


    #循环QuerySet,创建权限字典的目录结构
    #用权限的名字当做第字典的KEY,权限表的所有信息以键值对形式作为value
    for dic in permission_query:
        #dic为每条记录的字典
        permission_dic[dic['permissions__name']] = {
            'id': dic['permissions__id'],
            'pid': dic['permissions__parent__id'],
            'name': dic['permissions__name'],
            'pname': dic['permissions__parent__name'],
            'url': dic['permissions__url'],
            'title':dic['permissions__title']
        }

        # 只有二级菜单才有关联的permissions__menu__id,None代表此条记录为普通权限
        menu_id = dic.get('permissions__menu__id')
        if not menu_id:     #如果值为None的话跳过这条记录
            continue

        if menu_id not in menu_dict:
            #如果menu_dict中没有这个key对应的数据,在字典中创建一个key为menu_id,value为一个一级菜单信息的字典
            # children列表中的字典是二级菜单的信息
            menu_dict[menu_id] = {
                'name': dic['permissions__menu__name'],
                'icon': dic['permissions__menu__icon'],
                'weight': dic['permissions__menu__weight'],
                'children': [
                    {
                        'id': dic['permissions__id'],
                        'title': dic['permissions__title'],
                        'url': dic['permissions__url']
                    }
                ]
            }
            #如果menu_id在字典中,说明一级菜单存在,只在children列表中添加二级菜单信息
        else:
            menu_dict.get(menu_id).get('children').append({
                'id': dic['permissions__id'],
                'title': dic['permissions__title'],
                'url': dic['permissions__url']
            })

    # 权限信息放入session
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dic
    # 菜单信息放入session
    request.session[settings.MENU_SESSION_KEY] = menu_dict
