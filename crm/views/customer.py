from django.shortcuts import render, HttpResponse, redirect, reverse
from crm import models
from crm.plugins.forms import CustomerForm
from crm.plugins.pagination import Pagination
from django.views import View
from django.db.models import Q
from django.db import transaction


def customer_change(request, nid=None):
    return_url = request.GET.get('return','')
    ret = models.Customer.objects.filter(id=nid).first()
    form_obj = CustomerForm(instance=ret)
    title = '编辑用户' if ret else '添加用户'
    if request.method == 'POST':
        form_obj = CustomerForm(request.POST, instance=ret)
        if form_obj.is_valid():
            form_obj.save()
            if return_url:
                return redirect(return_url)
            else:
                return redirect(reverse('customer_list'))
    return render(request, 'customer/customer_change.html', {'form_obj': form_obj, 'title': title})


class CustomerList(View):
    def get(self, request):
        q, query = self.search(['qq', 'name'])
        if request.path == reverse('mycustomer_list'):
            cus_l_obj = models.Customer.objects.filter(q, consultant=request.user_id)
            title = '我的客户'
        else:
            cus_l_obj = models.Customer.objects.filter(q, consultant__isnull=True)
            title = '客户列表'
        page = Pagination(len(cus_l_obj), request.GET.get('page'), request.GET.copy())
        return render(request, 'customer/customer_list.html',
                      {'cus_l': cus_l_obj[page.start:page.end], 'li_str': page.core, 'title': title, 'query': query})

    def post(self, request):
        action = request.POST.get('action')
        id_list = self.request.POST.getlist('ids')
        if hasattr(self, action):
            ret = getattr(self, action)(id_list)
            if ret:
                return ret
        else:
            return HttpResponse('非法操作')
        return self.get(request)

    def multi_pub2pri(self, id_list):
        # models.Customer.objects.filter(pk__in=id_list).update(consultant=self.request.user_id)
        with transaction.atomic():
            obj = models.Customer.objects.filter(pk__in=id_list,consultant__isnull=True).select_for_update()
            if len(id_list) == obj.count():
                obj.update(consultant=self.request.user_id)
            else:
                return HttpResponse('当前用户已经不存在')

    def multi_pri2pub(self, id_list):
        models.Customer.objects.filter(pk__in=id_list).update(consultant=None)

    def search(self, field_list):
        query = self.request.GET.get('search', '')
        q = Q()
        q.connector = 'OR'
        for field in field_list:
            q.children.append(Q(('%s__contains' % (field), query)))
        return q, query
