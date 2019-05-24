from django.views import View
from crm import models
from django.shortcuts import reverse, redirect, render, HttpResponse
from crm.plugins.pagination import Pagination
from django.db.models import Q
from crm.plugins.forms import ConsultRecordForm


class ConsultList(View):

    def get(self, request, customer_id):
        user_obj = self.request.user_obj
        form_obj = ConsultRecordForm(instance=models.ConsultRecord(consultant=user_obj))
        q, query = self.search([])
        if customer_id == '0':
            consult_obj = models.ConsultRecord.objects.filter(q, consultant=request.user_obj,
                                                              delete_status=False).order_by('-date')
        else:
            consult_obj = models.ConsultRecord.objects.filter(q, consultant=request.user_obj, delete_status=False,
                                                              customer_id=customer_id).all()
        title = '跟进记录'
        page = Pagination(len(consult_obj), request.GET.get('page'), request.GET.copy())
        return render(request, 'consult/consult_list.html',
                      {'con_l': consult_obj[page.start:page.end], 'li_str': page.core, 'title': title, 'query': query,
                       'from_obj': form_obj})


    def post(self,request,customer_id):
        action = request.POST.get('action')
        if not hasattr(self, action):
            return HttpResponse('非法操作')
        getattr(self, action)()

        return self.get(request, customer_id)

    def search(self, field_list):
        query = self.request.GET.get('search', '')
        q = Q()
        q.connector = 'OR'
        for field in field_list:
            q.children.append(Q(('%s__contains' % (field), query)))
        return q, query



def change_consult(request,consult_id=None):
    title = '编辑跟进记录' if consult_id else '添加跟进记录'
    return_url = request.GET.get('return','')
    if not consult_id:
        obj = models.ConsultRecord(consultant = request.user_obj)
        form_obj = ConsultRecordForm(instance=obj)
    else:
        obj = models.ConsultRecord.objects.filter(id = consult_id).first()
        form_obj = ConsultRecordForm(instance=obj)


    if request.method == 'POST':
        form_obj = ConsultRecordForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            if return_url:
                ret = redirect(return_url)
            else:
                ret = redirect(reverse('consult_list', args=('0',)))
            return ret

    return render(request, 'consult/consult_change.html', {'form_obj': form_obj,'title':title})


