from django.views import View
from crm import models
from django.shortcuts import reverse, redirect, render, HttpResponse
from crm.plugins.pagination import Pagination
from django.db.models import Q
from crm.plugins.forms import ClassListForm,CourseRecordForm,StudyRecordForm
from django.forms import modelformset_factory


class ClassesList(View):
    def get(self, request, ):
        q, query = self.search([])
        classes_obj = models.ClassList.objects.all()
        title = '班级列表'
        page = Pagination(len(classes_obj), request.GET.get('page'), request.GET.copy())
        return render(request, 'teacher/classes_list.html',
                      {'cla_l': classes_obj[page.start:page.end], 'li_str': page.core, 'title': title,
                       'query': query, })

    def post(self, request):
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


def classes_change(request, edit_id=None):
    form_obj = ClassListForm()
    title = '添加班级' if edit_id else '编辑班级'
    obj = models.ClassList.objects.filter(id=edit_id).first()
    if edit_id:
        form_obj = ClassListForm(instance=obj)
    if request.method == 'POST':
        return_url = request.GET.get('return','')
        form_obj = ClassListForm(request.POST,instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            if return_url:
                return redirect(return_url)
            else:
                return redirect(reverse('classes_list'))


    return render(request, 'teacher/classes_change.html', {'form_obj': form_obj, 'title': title})



class CourseRecordList(View):
    def get(self, request, class_id):
        q, query = self.search([])
        all_cou_re = models.CourseRecord.objects.filter(re_class_id=class_id)
        title = '课程记录'
        page = Pagination(len(all_cou_re), request.GET.get('page'), request.GET.copy())
        return render(request, 'teacher/course_record_list.html',
                      {'all_cou_re': all_cou_re[page.start:page.end], 'li_str': page.core, 'title': title,
                       'query': query, 'class_id':class_id})

    def post(self, request,class_id):
        action = request.POST.get('action')
        if not hasattr(self, action):
            return HttpResponse('非法操作')
        getattr(self, action)()

        return self.get(request,class_id)

    def search(self, field_list):
        query = self.request.GET.get('search', '')
        q = Q()
        q.connector = 'OR'
        for field in field_list:
            q.children.append(Q(('%s__contains' % (field), query)))
        return q, query

    def multi_init(self):
        # 拿到课程记录的ID
        course_record_ids = self.request.POST.getlist('ids')  # [1,2 ]

        for course_record_id in course_record_ids:

            # 拿到所有的学生
            course_record = models.CourseRecord.objects.filter(pk=course_record_id).first()
            all_student = course_record.re_class.customer_set.filter(status='studying')

            for student in all_student:
                # models.StudyRecord.objects.create(course_record_id=course_record_id,student=student)
                models.StudyRecord.objects.get_or_create(course_record_id=course_record_id, student=student)

def course_recode_change(request,class_id=None,record_id=None):
    if class_id:
        obj = models.CourseRecord(re_class_id=class_id,teacher=request.user_obj)
        title = '添加课程记录'
    else:
        obj = models.CourseRecord.objects.filter(id=record_id).first()
        title = '编辑课程记录'
    form_obj = CourseRecordForm(instance=obj)
    if request.method == 'POST':
        return_url = request.GET.get('return','')
        form_obj = CourseRecordForm(request.POST,instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            if return_url:
                return redirect(return_url)
            else:
                return redirect(reverse('course_record_list',args=(class_id)))

    return render(request,'teacher/course_record_change.html',{'form_obj':form_obj,'title':title})


def study_record_list(request,record_id):
    FormSet = modelformset_factory(models.StudyRecord,StudyRecordForm,extra=0)
    all_study_record = models.StudyRecord.objects.filter(course_record_id=record_id)
    form_obj = FormSet(queryset=all_study_record)
    if request.method=='POST':
        form_obj = FormSet(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('study_record_list',args=(record_id,)))
    return render(request, 'teacher/study_record_list.html', {'form_obj': form_obj}, )