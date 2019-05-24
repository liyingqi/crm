from django.test import TestCase

# Create your tests here.

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CRM_PJ.settings")
import django
django.setup()
from crm import models


# user_obj = models.UserProfile.objects.filter(id=1).first()
# print(user_obj)

# ret = models.Enrollment.objects.filter(customer__in=[i for i in user_obj.customers.all() ])
#


#
# obj = models.Enrollment.objects.filter(id=1).first()
# cla = obj.enrolment_class
# print(obj.customer.class_list.all())
# obj.customer.class_list.add(cla)
# print(obj.customer.class_list.all())

#
# obj = models.UserProfile.objects.filter(id=2).first()
# ret = obj.department
# print(ret)