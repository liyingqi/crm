from django.shortcuts import render, redirect, reverse,HttpResponse
from rbac import models
from rbac.forms import RoleForm,MenuForm,PermissionForm,MultiPermissionForm
from django.db.models import Q
from django.forms import modelformset_factory, formset_factory
from rbac.service.routes import get_all_url_dict
from crm.models import UserProfile


# Create your views here.

def role_list(request):
    roles_l = models.Role.objects.all()
    return render(request, 'rbac/role_list.html', {'roles_l': roles_l})


def role_change(request, edit_id=None):
    obj = models.Role.objects.filter(id=edit_id).first()
    if edit_id:
        form_obj = RoleForm(instance=obj)
        title = '编辑角色'
    else:
        form_obj = RoleForm()
        title = '添加角色'
    if request.method == 'POST':
        form_obj = RoleForm(request.POST,instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('rbac:rbac/role_list'))

    return render(request, 'rbac/role_change.html', {'form_obj': form_obj, 'title': title})


def role_del(request,del_id):
    models.Role.objects.filter(id=del_id).delete()
    return redirect(reverse('rbac:rbac/role_list'))



def menu_list(request):
    menus_l = models.Menu.objects.all()
    mid = request.GET.get('mid')
    if  not mid:
        permissions_dic = models.Permission.objects.all().values(
            'id',
            'url',
            'name',
            'title',
            'menu_id',
            'menu__name',
            'parent_id'
        )
    else:
        permissions_dic = models.Permission.objects.filter(Q(menu_id=mid)|Q(parent__menu_id=mid)).values(
            'id',
            'url',
            'name',
            'title',
            'menu_id',
            'menu__name',
            'parent_id'
        )
    per_dic = {}
    for i in permissions_dic:
        menu_id = i.get('menu_id')
        pid = i.get('id')
        if menu_id:
            per_dic[pid] = i
            i['menu__name'] = i['menu__name']
            i['children'] = []
    for i in permissions_dic:
        pid = i.get('parent_id')
        if pid:
            per_dic[pid]['children'].append(i)


    return render(request,'rbac/menu_list.html',{'menus_l':menus_l,'permissions_dic':per_dic,'mid':mid})


def menu_change(request,edit_id=None):
    obj = models.Menu.objects.filter(id=edit_id).first()
    if not edit_id:
        form_obj = MenuForm()
        title = '添加菜单'
    else:
        form_obj = MenuForm(instance=obj)
        title = '编辑菜单'
    if request.method == 'POST':
        form_obj = MenuForm(request.POST,instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('rbac:rbac/menu_list'))

    return render(request,'rbac/menu_change.html',{'form_obj':form_obj,'title':title})



def menu_del(request,del_id):
    models.Menu.objects.filter(id=del_id).delete()
    return redirect(reverse('rbac:rbac/menu_list'))


def permission_change(request,edit_id=None):
    obj = models.Permission.objects.filter(id=edit_id).first()
    if edit_id:
        form_obj = PermissionForm(instance=obj)
        title = '编辑权限'

    else:
        form_obj = PermissionForm()
        title = '添加权限'

    if request.method == 'POST':
        form_obj = PermissionForm(request.POST,instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('rbac:rbac/menu_list'))


    return render(request,'rbac/permission_change.html',{'form_obj':form_obj,'title':title})


def permission_del(request,del_id):
    models.Permission.objects.filter(id=del_id).delete()
    return redirect(reverse('rbac:rbac/menu_list'))


def multi_permissions(request):
    """
    批量操作权限
    :param request:
    :return:
    """
    post_type = request.GET.get('type')

    # 编辑和删除
    FormSet = modelformset_factory(models.Permission, MultiPermissionForm, extra=0)
    # 新增
    AddFormSet = formset_factory(MultiPermissionForm, extra=0)

    # 数据库中所有的权限
    permissions = models.Permission.objects.all()
    # 路由系统中所有的URL  权限
    router_dict = get_all_url_dict(ignore_namespace_list=['admin', ])

    # 数据库中所有的权限的别名的集合
    permissions_name_set = set([i.name for i in permissions])

    # 路由系统中所有的权限的别名的集合
    router_name_set = set(router_dict.keys())
    # 新增权限的name_set
    add_name_set = router_name_set - permissions_name_set

    add_formset = AddFormSet(initial=[row for name, row in router_dict.items() if name in add_name_set])

    if request.method == 'POST' and post_type == 'add':
        add_formset = AddFormSet(request.POST)
        if add_formset.is_valid():
            permission_obj_list = [models.Permission(**i) for i in add_formset.cleaned_data]
            query_list = models.Permission.objects.bulk_create(permission_obj_list)
            add_formset = AddFormSet()
            for i in query_list:
                permissions_name_set.add(i.name)

    # 要删除的权限
    del_name_set = permissions_name_set - router_name_set
    del_formset = FormSet(queryset=models.Permission.objects.filter(name__in=del_name_set))

    update_name_set = permissions_name_set & router_name_set
    update_formset = FormSet(queryset=models.Permission.objects.filter(name__in=update_name_set))

    if request.method == 'POST' and post_type == 'update':
        update_formset = FormSet(request.POST)
        if update_formset.is_valid():
            update_formset.save()
            update_formset = FormSet(queryset=models.Permission.objects.filter(name__in=update_name_set))

    return render(
        request,
        'rbac/multi_permissions.html',
        {
            'del_formset': del_formset,
            'update_formset': update_formset,
            'add_formset': add_formset,
        }
    )


def distribute_permissions(request):
    """
    分配权限
    :param request:
    :return:
    """
    uid = request.GET.get('uid')
    rid = request.GET.get('rid')

    if request.method == 'POST' and request.POST.get('postType') == 'role':
        user = UserProfile.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        user.roles.set(request.POST.getlist('roles'))

    if request.method == 'POST' and request.POST.get('postType') == 'permission' and rid:
        role = models.Role.objects.filter(id=rid).first()
        if not role:
            return HttpResponse('角色不存在')
        role.permissions.set(request.POST.getlist('permissions'))

    # 所有的用户
    user_list = UserProfile.objects.all()

    # 当前用户所拥有角色
    user_has_roles = UserProfile.objects.filter(id=uid).values('id', 'roles')

    """
    用户所拥有的角色id
    user_has_roles_dict =  { 角色id : None  }
    """
    user_has_roles_dict = {item['roles']: None for item in user_has_roles}

    # 所有的角色
    role_list = models.Role.objects.all()

    if rid:
        role_has_permissions = models.Role.objects.filter(id=rid, permissions__id__isnull=False).values('id',
                                                                                                        'permissions')
    elif uid and not rid:
        # 当前的用户
        user = UserProfile.objects.filter(id=uid).first()
        if not user:
            return HttpResponse('用户不存在')
        # 当前用户 所有有的角色和所有权限的id
        role_has_permissions = user.roles.filter(permissions__id__isnull=False).values('id', 'permissions')
        role_has_permissions = user.roles.filter(permissions__id__isnull=False).values('id', 'permissions')
    else:
        role_has_permissions = []

    # 当前用户所有的权限id
    """
    role_has_permissions_dict =  {    权限的ID ：None}
    """

    role_has_permissions_dict = {item['permissions']: None for item in role_has_permissions}

    all_menu_list = []

    queryset = models.Menu.objects.values('id', 'name')  # 【   {id   name   }】
    menu_dict = {}

    """
    all_menu_list = [   {id   name  children:[
        {  'id', 'title', 'menu_id'  children : [
             {'id', 'title', 'parent_id' }
        ]  }
    ]  } 

    ,{'id': None, 'title': '其他', 'children': [
         {'id', 'title', 'parent_id' }
    ]}]


    menu_dict = { 
            菜单的id:  {id   name  children:[
                {  'id', 'title', 'menu_id'  children : [
                     {'id', 'title', 'parent_id' }
                ]  }
            ]  } ,
            None:  {'id': None, 'title': '其他', 'children': [
             {'id', 'title', 'parent_id' }
            ]}
    }
    """

    for item in queryset:  # {id   name   }
        item['children'] = []  # {id   name  children:[]   }
        menu_dict[item['id']] = item
        all_menu_list.append(item)

    other = {'id': None, 'title': '其他', 'children': []}
    all_menu_list.append(other)
    menu_dict[None] = other

    # 所有的父权限
    root_permission = models.Permission.objects.filter(menu__isnull=False).values('id', 'title', 'menu_id')
    root_permission_dict = {}
    """
      root_permission_dict = {
            父权限的id :  {  'id', 'title', 'menu_id'  children : [  {'id', 'title', 'parent_id' } ]  }
      }
    """

    for per in root_permission:  # {  'id', 'title', 'menu_id' }
        per['children'] = []  # {  'id', 'title', 'menu_id'  children : []  }
        nid = per['id']
        menu_id = per['menu_id']
        root_permission_dict[nid] = per
        menu_dict[menu_id]['children'].append(per)

    # 可能是子权限
    node_permission = models.Permission.objects.filter(menu__isnull=True).values('id', 'title', 'parent_id')

    for per in node_permission:  # {'id', 'title', 'parent_id' }
        pid = per['parent_id']
        if not pid:
            menu_dict[None]['children'].append(per)
            continue
        root_permission_dict[pid]['children'].append(per)

    return render(
        request,
        'rbac/distribute_permissions.html',
        {
            'user_list': user_list,
            'role_list': role_list,
            'all_menu_list': all_menu_list,
            'user_has_roles_dict': user_has_roles_dict,
            'role_has_permissions_dict': role_has_permissions_dict,
            'uid': uid,
            'rid': rid
        }
    )