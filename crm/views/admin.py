from crm import models
from django.shortcuts import render,HttpResponse,redirect,reverse
from django.views import View
from crm.plugins.pagination import Pagination
from crm.plugins.forms import CampusesForm,DepartmentForm
from django.db.models import Q

class CampusesList(View):
    def get(self, request):
        user_obj = self.request.user_obj
        q, query = self.search([])
        all_campuses = models.Campuses.objects.all()
        title = '校区列表'
        page = Pagination(len(all_campuses), request.GET.get('page'), request.GET.copy())
        return render(request, 'admin/campuses_list.html',
                      {'camp_l': all_campuses[page.start:page.end], 'li_str': page.core, 'title': title, 'query': query,})


    def post(self,request):
        action = request.POST.get('action')
        if not hasattr(self, action):
            return HttpResponse('非法操作')
        getattr(self, action)()

        return self.get(request)

    def search(self, field_list):
        query = self.request.GET.get('search', '')
        q = Q()
        q.connector = 'OR'
        for field in field_list:
            q.children.append(Q(('%s__contains' % (field), query)))
        return q, query

def campuses_change(request,edit_id=None):
    obj = models.Campuses.objects.filter(id=edit_id).first()
    title = '编辑校区' if edit_id else '添加校区'
    form_obj = CampusesForm(instance=obj)
    if request.method == 'POST':
        return_url = request.GET.get('return')
        form_obj = CampusesForm(request.POST,instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            if return_url:
                return redirect(reverse(return_url))
            else:
                return redirect(reverse('campuses_list'))
    return render(request,'admin/campuses_change.html',{'form_obj':form_obj,'title':title})



class DepartmentList(View):
    def get(self, request):
        user_obj = self.request.user_obj
        q, query = self.search([])
        all_department = models.Department.objects.all()
        title = '部门列表'
        page = Pagination(len(all_department), request.GET.get('page'), request.GET.copy())
        return render(request, 'admin/department_list.html',
                      {'dep_l': all_department[page.start:page.end], 'li_str': page.core, 'title': title, 'query': query,})


    def post(self,request):
        action = request.POST.get('action')
        if not hasattr(self, action):
            return HttpResponse('非法操作')
        getattr(self, action)()

        return self.get(request)

    def search(self, field_list):
        query = self.request.GET.get('search', '')
        q = Q()
        q.connector = 'OR'
        for field in field_list:
            q.children.append(Q(('%s__contains' % (field), query)))
        return q, query


def department_change(request,edit_id=None):
    obj = models.Department.objects.filter(id=edit_id).first()
    title = '编辑部门' if edit_id else '添加部门'
    form_obj = DepartmentForm(instance=obj)
    if request.method == 'POST':
        return_url = request.GET.get('return')
        form_obj = DepartmentForm(request.POST,instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            if return_url:
                return redirect(reverse(return_url))
            else:
                return redirect(reverse('department_list'))
    return render(request,'admin/department_change.html',{'form_obj':form_obj,'title':title})