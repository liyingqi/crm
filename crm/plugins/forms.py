from django import forms
from crm import models
from django.core.exceptions import ValidationError
from crm.plugins.md5 import encryption


class BSForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if  not isinstance(field,forms.BooleanField):
                field.widget.attrs.update({'class': 'form-control'})


class RegForm(BSForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
        label='密码',
        error_messages={
            'required': '此项为必填项',
            'min_length': '密码至少8位'
        }
    )
    re_pwd = forms.CharField(
        widget=forms.PasswordInput,
        label='确认密码',
        error_messages={
            'required': '此项为必填项',
            'min_length': '密码至少8位'
        }
    )

    class Meta:
        model = models.UserProfile
        fields = '__all__'
        exclude = ['memo', 'is_active']
        error_messages = {
            'username': {
                'required': '此项为必填项',
                'invalid': '用户名必须为邮箱'
            },
            'name': {
                'required': '此项为必填项'
            }
        }
        labels = {
            'department': '部门名称'
        }

    def clean_username(self):
        value = self.cleaned_data.get('username')
        if len(value) > 8:
            return value
        else:
            raise ValidationError('用户名长度不能少于8位')

    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_pwd')
        if pwd == re_pwd:
            user = self.cleaned_data.get('username')
            pwd = encryption(user, pwd)
            self.cleaned_data['password'] = pwd
            return self.cleaned_data
        else:
            self.add_error('re_pwd', '两次密码不一致')
            raise ValidationError('两次密码不一致')


class CustomerForm(BSForm):
    class Meta:
        model = models.Customer
        fields = '__all__'
        error_messages = {
            'qq': {
                'required': '不能为空'
            },
            'course': {
                'required': '此选项必填'
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get('course').widget.attrs.pop('class')


class ConsultRecordForm(BSForm):
    class Meta:
        model = models.ConsultRecord
        fields = '__all__'
        exclude = ['delete_status']
        error_messages = {
            'customer': {'required': '不能为空'},
            'note': {'required': '不能为空'},
            'status': {'required': '不能为空'}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].choices = [ (i.pk,i.qq) for i in self.instance.consultant.customers.all()]
        self.fields['customer'].choices.insert(0,('','---------'))
        self.fields['consultant'].choices = [(self.instance.consultant.pk,self.instance.consultant.name)]


class EnrollmentForm(BSForm):
    class Meta:
        model = models.Enrollment
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['customer'].choices = [(self.instance.customer.id,self.instance.customer.qq)]


class ClassListForm(BSForm):
    class Meta:
        model = models.ClassList
        fields = '__all__'


class CourseRecordForm(BSForm):
    class Meta:
        model = models.CourseRecord
        fields = '__all__'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['re_class'].choice = [(self.instance.re_class.id,self.instance.re_class)]
        self.fields['teacher'].choice = [(self.instance.teacher.id,self.instance.teacher)]


class StudyRecordForm(BSForm):
    class Meta:
        model = models.StudyRecord
        fields = '__all__'


class CampusesForm(BSForm):
   class Meta:
       model = models.Campuses
       fields = '__all__'



class DepartmentForm(BSForm):
   class Meta:
       model = models.Department
       fields = '__all__'