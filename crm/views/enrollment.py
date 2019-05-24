from django.views import View
from crm import models
from django.shortcuts import render,redirect,reverse,HttpResponse
from crm.plugins.pagination import Pagination
from django.db.models import Q
from crm.plugins.forms import EnrollmentForm



class EnrollmentList(View):

    def get(self, request,):
        user_obj = self.request.user_obj
        q, query = self.search([])
        enr_l = models.Enrollment.objects.filter(q,customer__in=[i for i in user_obj.customers.all()],delete_status=False)
        title = '报名记录'
        page = Pagination(len(enr_l), request.GET.get('page'), request.GET.copy())

        return render(request, 'enrollment/enrollment_list.html',
                      {'enr_l': enr_l[page.start:page.end], 'li_str': page.core, 'title': title, 'query': query})

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


def enrollment_change(request,customer_id=None,enrollment_id=None):
    if customer_id:
        obj = models.Enrollment(customer_id=customer_id)
        title = '添加报名'
        form_obj = EnrollmentForm(instance=obj)
    else:
        obj = models.Enrollment.objects.filter(id=enrollment_id).first()
        form_obj = EnrollmentForm(instance=obj)
        title = '编辑报名'
    if request.method == 'POST':
        form_obj = EnrollmentForm(request.POST,instance=obj)
        if form_obj.is_valid():
            enrollment_obj = form_obj.save()
            if enrollment_obj.contract_approved:
                cla = enrollment_obj.enrolment_class
                enrollment_obj.customer.class_list.add(cla)
                models.Customer.objects.filter(qq=enrollment_obj.customer.qq).update(status='signed')
            return redirect(reverse('enrollment_list'))

    return render(request,'enrollment/enrollment_change.html',{'form_obj':form_obj,'title':title})
