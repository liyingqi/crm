from django.conf.urls import url
from rbac import views
urlpatterns = [
    url(r'role/list/$', views.role_list,name='rbac/role_list'),
    url(r'role/add/$', views.role_change,name='rbac/role_add'),
    url(r'role/edit/(\d+)/$', views.role_change,name='rbac/role_edit'),
    url(r'role/del/(\d+)/$', views.role_del,name='rbac/role_del'),


    url(r'menu/list/$', views.menu_list,name='rbac/menu_list'),
    url(r'menu/add/$', views.menu_change,name='rbac/menu_add'),
    url(r'menu/edit/(\d+)/$', views.menu_change,name='rbac/menu_edit'),
    url(r'menu/del/(\d+)/$', views.menu_del,name='rbac/menu_del'),
    url(r'permission/add/$', views.permission_change,name='rbac/permission_add'),
    url(r'permission/edit/(\d+)/$', views.permission_change,name='rbac/permission_edit'),
    url(r'permission/del/(\d+)/$', views.permission_del,name='rbac/permission_del'),

    url(r'^multi/permissions/$', views.multi_permissions, name='multi_permissions'),

    url(r'^distribute/permissions/$', views.distribute_permissions, name='distribute_permissions'),
]
