from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import redirect,reverse,HttpResponse
import re

class RBACMiddleware(MiddlewareMixin):

    def process_request(self,request):

        #获取目标url
        url = request.path_info
        # 获取白名单
        white_list = settings.WHITE_LIST
        #判断目标url是否在白名单中,如果存在,不用校验,直接返回None
        for reg_url in white_list:
            ret = re.search(reg_url,url)
            if ret:
                return

        #获取当前登录用户已经存在session中的权限字典
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)

        # print(permissions_list)

        #如果用户未登录,跳转到登录页面
        if not permission_dict:
            return redirect(reverse('login'))

        #设置一个当前用户输入的目标url对应的id,动态生成菜单,和对应的类时要作比对用
        request.menu_current_id = None

        #设置一个路径导航的列表,索引为0的项写死成首页,后期通过遍历列表获取路径导航,动态生成
        request.breadcrumb_list = [
            {'title': '首页', 'url': '/index/'}
        ]

        # 需要登录但是不需要权限校验的url,例如首页
        for i in settings.NO_PERMISSION_LIST:
            if re.search(r'^%s$'%i,url):
                return



        #权限校验,循环权限字典的value,因为key为一级菜单的id,并不需要
        for sec_dic in permission_dict.values():
            #如果权限字典中有目标url,通过匹配
            if re.search('^%s$'%sec_dic['url'],url):
                pid = sec_dic.get('pid')
                id = sec_dic.get('id')
                pname = sec_dic.get('pname')
                if pid:     #如果有pid,说明是 [编辑,增加,删除] 中的权限
                    #设置目标url的id,设为request对象属性
                    request.menu_current_id = pid
                    #在路径导航的列表中先加入二级菜单的信息
                    request.breadcrumb_list.append({'title':permission_dict[pname]['title'],'url':permission_dict[pname]['url']})
                    #再把具体权限信息加到路径导航的列表中
                    request.breadcrumb_list.append({'title':sec_dic['title'],'url':sec_dic['url']})
                else:
                    #没有pid说明是二级菜单页面,直接在路径导航的列表中加入二级菜单信息即可
                    request.menu_current_id = id
                    request.breadcrumb_list.append({'title': sec_dic['title'], 'url': sec_dic['url']})
                return
        else:
            #没有通过匹配说明没有权限,直接通过中间件返回响应
            return HttpResponse('没有访问权限')

