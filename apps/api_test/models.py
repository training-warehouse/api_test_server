from django.db import models
from apps.api_auth.models import User

HTTP_METHOD_CHOICE = (
    ('POST', 'POST'),
    ('GET', 'GET'),
    ('PUT', 'PUT'),
    ('DELETE', 'DELETE')
)


class Project(models.Model):
    project_type = (
        ('web', 'web'),
        ('app', 'app')
    )

    name = models.CharField(max_length=50, verbose_name='项目名称')
    type = models.CharField(max_length=50, verbose_name='项目类型', choices=project_type)
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='描述')
    last_update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='创建人')


class Host(models.Model):
    name = models.CharField(max_length=50, verbose_name='名称')
    host = models.CharField(max_length=1024, verbose_name='Host地址')
    description = models.CharField(max_length=1024, null=True, blank=True, verbose_name='描述')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='hosts', verbose_name='所属项目')


class Api(models.Model):
    """
    接口信息
    """
    STATUS_CODE_CHOICE = (
        ('200', '200'),
        ('201', '201'),
        ('202', '202'),
        ('203', '203'),
        ('204', '204'),
        ('301', '301'),
        ('302', '302'),
        ('400', '400'),
        ('401', '401'),
        ('403', '403'),
        ('404', '404'),
        ('405', '405'),
        ('406', '406'),
        ('407', '407'),
        ('408', '408'),
        ('500', '500'),
        ('502', '502')
    )

    name = models.CharField(max_length=50, verbose_name='接口名字')
    http_method = models.CharField(max_length=50, choices=HTTP_METHOD_CHOICE, verbose_name='请求方式')
    host = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name='host')
    path = models.CharField(max_length=1024, verbose_name='接口地址')
    headers = models.TextField(null=True, blank=True, verbose_name='请求头')
    data = models.TextField(null=True, blank=True, verbose_name='请求的数据')
    description = models.CharField(max_length=1024, null=True, blank=True, verbose_name='描述')
    expect_code = models.CharField(default=200, max_length=10, choices=STATUS_CODE_CHOICE, verbose_name='期望返回的code')
    expect_content = models.CharField(null=True, blank=True, max_length=255, verbose_name='期望返回的内容')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目', null=True, blank=True,
                                related_name='apis')


class ApiRunRecord(models.Model):
    url = models.CharField(max_length=200, verbose_name='请求的url')
    http_method = models.CharField(max_length=10, choices=HTTP_METHOD_CHOICE, verbose_name='请求方式')
    data = models.TextField(null=True, verbose_name='提交的数据')
    headers = models.TextField(null=True, verbose_name='提交的header')
    create_time = models.DateTimeField(auto_now=True, verbose_name='运行的时间')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='执行人')
    return_code = models.CharField(max_length=10, verbose_name='返回的code')
    return_content = models.TextField(null=True, verbose_name='返回的内容')
    api = models.ForeignKey(Api, on_delete=models.CASCADE, null=True, verbose_name='关联的api')

    class Meta:
        ordering = ['-create_time']


class Case(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='cases', verbose_name='所属项目')
    name = models.CharField(max_length=50, verbose_name='用例名称')
    apis = models.ManyToManyField(Api, related_name='cases')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='创建人')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    create_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')


class CaseArgument(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, null=True, related_name='arguments', verbose_name='用例')
    name = models.CharField(max_length=100, verbose_name='参数名称')
    value = models.CharField(max_length=100, verbose_name='参数值')


class ApiArgument(models.Model):
    ARGUMENT_ORIGIN_CHOICE = (
        ('HEADER', 'HEADER'),
        ('BODY', 'BODY'),
        ('COOKIE', 'COOKIE'),
    )

    api = models.ForeignKey(Api, on_delete=models.CASCADE, null=True, related_name='arguments', verbose_name='用例API')
    name = models.CharField(max_length=100, verbose_name='参数名字')
    origin = models.CharField(max_length=20, choices=ARGUMENT_ORIGIN_CHOICE, verbose_name='参数来源')
    format = models.CharField(max_length=100, verbose_name='参数获取格式')
