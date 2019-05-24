from django.conf.urls import url
from crm.views import customer
from crm.views import consult
from crm.views import enrollment
from crm.views import teacher
from crm.views import admin

urlpatterns = [
    url(r'customer/list/', customer.CustomerList.as_view(), name='customer_list'),
    url(r'mycustomer/list/', customer.CustomerList.as_view(), name='mycustomer_list'),
    url(r'customer/add/', customer.customer_change, name='customer_add'),
    url(r'customer/edit/(\d+)/', customer.customer_change, name='customer_edit'),

    url(r'consult/list/(0)/', consult.ConsultList.as_view(), name='all_consult_list'),
    url(r'consult/list/(?P<customer_id>\d+)/', consult.ConsultList.as_view(), name='consult_list'),
    url(r'consult/add/', consult.change_consult, name='consult_add'),
    url(r'consult/edit/(?P<consult_id>\d+)', consult.change_consult, name='consult_edit'),

    url(r'enrollment/list/', enrollment.EnrollmentList.as_view(), name='enrollment_list'),
    url(r'enrollment/add/(?P<customer_id>\d+)', enrollment.enrollment_change, name='enrollment_add'),
    url(r'enrollment/edit/(?P<enrollment_id>\d+)', enrollment.enrollment_change, name='enrollment_edit'),

    url(r'classes/list/', teacher.ClassesList.as_view(), name='classes_list'),
    url(r'classes/add/', teacher.classes_change, name='classes_add'),
    url(r'classes/edit/(\d+)', teacher.classes_change, name='classes_edit'),

    url(r'course_record/list/(?P<class_id>\d+)', teacher.CourseRecordList.as_view(), name='course_record_list'),
    url(r'course_record/add/(?P<class_id>\d+)', teacher.course_recode_change, name='course_recode_add'),
    url(r'course_record/edit/(?P<record_id>\d+)', teacher.course_recode_change, name='course_recode_edit'),

    url(r'study_record/list/(?P<record_id>\d+)', teacher.study_record_list, name='study_record_list'),


    url(r'campuses/list/', admin.CampusesList.as_view(), name='campuses_list'),
    url(r'campuses/add/', admin.campuses_change, name='campuses_add'),
    url(r'campuses/edit/(\d+)/', admin.campuses_change, name='campuses_edit'),


    url(r'department/list/', admin.DepartmentList.as_view(), name='department_list'),
    url(r'department/add/', admin.department_change, name='department_add'),
    url(r'department/edit/(\d+)/', admin.department_change, name='department_edit'),

]
