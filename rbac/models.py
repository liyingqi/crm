from django.db import models

# Create your models here.


class Menu(models.Model):
    '''
    菜单表     一级菜单
    '''
    name = models.CharField(max_length=32,verbose_name='一级菜单')
    icon = models.CharField(max_length=64,verbose_name='图标',blank=True,null=True)
    weight = models.IntegerField(verbose_name='权重',default=1)

    def __str__(self):
        return self.name


class Permission(models.Model):
    """
    权限表
    menu_id
        有   表示当前的权限是二级菜单  也是父权限
        没有  就是一个普通的权限

    parent_id
        有    表示当前的权限是一个子权限
        没有  父权限
    """
    url = models.CharField(max_length=255,verbose_name='权限',unique=True)
    name = models.CharField(max_length=32,verbose_name='别名',unique=True)
    title = models.CharField(max_length=32,verbose_name='标题')
    menu = models.ForeignKey('Menu',blank=True,null=True,verbose_name='一级菜单')
    parent = models.ForeignKey('Permission',blank=True,null=True,verbose_name='父级菜单')

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色表
    """
    name = models.CharField(max_length=32,verbose_name='角色名称')
    permissions = models.ManyToManyField('Permission',blank=True)

    def __str__(self):
        return self.name

class User(models.Model):
    # name = models.CharField(max_length=32,verbose_name='用户名')
    # pwd = models.CharField(max_length=32,verbose_name='密码')
    roles = models.ManyToManyField(Role,blank=True)

    # def __str__(self):
    #     return self.name
    class Meta:
        abstract = True