# -.- coding:utf-8 -.-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=200, unique=True)
    create_time = models.DateTimeField(auto_now=True)
    pro_user = models.CharField(max_length=200)
    pro_status = models.CharField(max_length=200)
    url = models.CharField(max_length=500)
    test_type = models.CharField(max_length=20,default="Web测试")

    # def __unicode__(self):
    #     return self.name


class Case(models.Model):
    name = models.CharField(max_length=200, unique=True)
    browser = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now=True)
    case_nature = models.CharField(max_length=500)
    category = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    features = models.CharField(max_length=200)
    project = models.ForeignKey(Project)
    #
    # def __unicode__(self):
    #     return self.name


class Method(models.Model):
    name = models.CharField(max_length=200)
    #
    # def __unicode__(self):
    #     return self.name


class Action(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=1000)

    # def __unicode__(self):
    #     return self.name


class Business(models.Model):
    name = models.CharField(max_length=200, unique=True)
    date = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=200)
    creator = models.CharField(max_length=300)
    Project = models.ForeignKey(Project)

    # def __unicode__(self):
    #     return self.name

class Businessaction(models.Model):
    actor = models.CharField(max_length=300)
    actiondate = models.DateTimeField(auto_now=True)
    action = models.CharField(max_length=300)
    edit_field = models.CharField(max_length=300)
    old_field_value = models.CharField(max_length=300)
    new_field_value = models.CharField(max_length=300)
    case_name = models.CharField(max_length=300)
    Business = models.ForeignKey(Business)

    # def __unicode__(self):
    #     return self.name

class Projectaction(models.Model):
    actor = models.CharField(max_length=300)
    actiondate = models.DateTimeField(auto_now=True)
    action = models.CharField(max_length=300)
    edit_field = models.CharField(max_length=300)
    old_field_value = models.CharField(max_length=300)
    new_field_value = models.CharField(max_length=300)
    envName = models.CharField(max_length=300)
    Project = models.ForeignKey(Project)

    # def __unicode__(self):
    #     return self.name

class Caseaction(models.Model):
    actor = models.CharField(max_length=300)
    action = models.CharField(max_length=300)
    actiondate = models.DateTimeField(auto_now=True)
    edit_field = models.CharField(max_length=300)
    old_field_value = models.CharField(max_length=300)
    new_field_value = models.CharField(max_length=300)
    step_desc = models.CharField(max_length=300)
    step_action = models.CharField(max_length=300)
    step_value = models.CharField(max_length=300)
    step_e_name = models.CharField(max_length=300)
    case = models.ForeignKey(Case)

    # def __unicode__(self):
    #     return self.name



class Business_stp(models.Model):
    name = models.CharField(max_length=200)
    case_id = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    category= models.CharField(max_length=200)
    case_nature = models.CharField(max_length=200)
    business = models.ForeignKey(Business)

    # def __unicode__(self):
    #     return self.name


class Test_execution(models.Model):
    """用例执行名称表"""
    name = models.CharField(max_length=200, unique=True, error_messages={"msg": "重复"})
    date = models.DateTimeField(auto_now=True)
    creator = models.CharField(max_length=200)
    user = models.ForeignKey(User)

    # def __unicode__(self):
    #     return self.name


class Execution_detail(models.Model):
    """用例执行名称下面的测试用例和测试业务流，Perform_Case外链表"""
    name = models.CharField(max_length=200)
    case_nature = models.CharField(max_length=500)
    category = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    case_id = models.CharField(max_length=100)
    perform = models.ForeignKey(Test_execution)

    # def __unicode__(self):
    #     return self.name

class Executionaction(models.Model):
    actor = models.CharField(max_length=300)
    actiondate = models.DateTimeField(auto_now=True)
    action = models.CharField(max_length=300)
    edit_field = models.CharField(max_length=500)
    old_field_value = models.CharField(max_length=500)
    new_field_value = models.CharField(max_length=500)
    case_name = models.CharField(max_length=500)
    Execution = models.ForeignKey(Test_execution)

    # def __unicode__(self):
    #     return self.name


class Test_report(models.Model):
    name = models.CharField(max_length=200)
    Execution_id = models.CharField(max_length=20)
    date = models.CharField(max_length=200)
    path = models.CharField(max_length=200)

    # def __unicode__(self):
    #     return self.name


class element(models.Model):
    name = models.CharField(max_length=200)
    fun = models.CharField(max_length=200)
    values = models.CharField(max_length=500)
    desc = models.CharField(max_length=500)
    page_url = models.CharField(max_length=500)
    creator = models.CharField(max_length=300)
    project = models.ForeignKey(Project, null=True)

    # def __unicode__(self):
    #     return self.name

class Elementaction(models.Model):
    actor = models.CharField(max_length=300)
    actiondate = models.DateTimeField(auto_now=True)
    action = models.CharField(max_length=300)
    edit_field = models.CharField(max_length=500)
    old_field_value = models.CharField(max_length=500)
    new_field_value = models.CharField(max_length=500)
    element = models.ForeignKey(element)
    # def __unicode__(self):
    #     return self.name

class case_process(models.Model):
    desc = models.CharField(max_length=500)
    action = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    ele_id = models.CharField(max_length=20)
    ele_name = models.CharField(max_length=200)
    case = models.ForeignKey(Case)

    # def __unicode__(self):
    #     return self.desc


# 项目环境列表
class ProTemp(models.Model):
    """模板表"""
    tempName = models.CharField(max_length=200, unique=True)
    createTime = models.DateTimeField(auto_now=True)
    last_time = models.CharField(max_length=100)
    createUser = models.CharField(max_length=40)
    template_type = models.CharField(max_length=100)
    proName = models.ForeignKey(Project)

    # def __unicode__(self):
    #     return self.tempName


# 接口测试用例列表，caseType区分jms报文或者开放平台用例,diffType区分数据比对方式
class InCaseList(models.Model):
    tempId = models.CharField(max_length=10)
    caseName = models.CharField(max_length=200, unique=True)
    creator = models.CharField(max_length=300)
    createDate = models.DateTimeField(auto_now_add=True)
    modifyDate = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    nature = models.CharField(max_length=300)
    category = models.CharField(max_length=300)
    project = models.ForeignKey(Project)

    # def __unicode__(self):
    #     return self.caseName

class InCaseAction(models.Model):
    actor = models.CharField(max_length=300)
    actiondate = models.DateTimeField(auto_now=True)
    action = models.CharField(max_length=300)
    edit_field = models.CharField(max_length=500)
    old_field_value = models.CharField(max_length=500)
    new_field_value = models.CharField(max_length=500)
    add_objId = models.CharField(max_length=300)
    add_diffType = models.CharField(max_length=300)
    add_value = models.CharField(max_length=300)
    add_fieldname = models.CharField(max_length=300)
    add_ex = models.CharField(max_length=300)
    inCaseList = models.ForeignKey(InCaseList)

    # def __unicode__(self):
    #     return self.name


class InCaseDetail(models.Model):
    case = models.ForeignKey(InCaseList)
    objId = models.CharField(max_length=20)
    value = models.CharField(max_length=1000)

    # def __unicode__(self):
    #     return self.objId


class Diff(models.Model):
    case = models.ForeignKey(InCaseList)
    objId = models.CharField(max_length=20)
    field_name = models.CharField(max_length=200)
    diffType = models.CharField(max_length=20)
    value = models.CharField(max_length=200)
    ex = models.CharField(max_length=2000)

    # def __unicode__(self):
    #     return self.objId


class TempDetail(models.Model):
    objName = models.CharField(max_length=120)
    part = models.CharField(max_length=40)
    list = models.CharField(max_length=40)
    key = models.CharField(max_length=40)
    key2 = models.CharField(max_length=40)
    type = models.CharField(max_length=40)
    temp = models.ForeignKey(ProTemp)

    # def __unicode__(self):
    #     return self.objName


class ProSetting(models.Model):
    envName = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    port = models.CharField(max_length=20)
    connectType = models.CharField(max_length=40)
    connectData = models.CharField(max_length=40)
    userName = models.CharField(max_length=30)
    passWord = models.CharField(max_length=30)
    interfaceType = models.CharField(max_length=20)
    is_used = models.CharField(max_length=10,default=False)
    proName = models.ForeignKey(Project)

    # def __unicode__(self):
    #     return self.envName


class api_business(models.Model):
    """接口业务流表"""
    name = models.CharField(max_length=200)
    create_date = models.DateTimeField(auto_now=True)
    edit_date = models.CharField(max_length=100)
    project = models.ForeignKey(Project, name="pro")

    # def __unicode__(self):
    #     return self.name

    class Meta:
        unique_together = ("name",)


class api_detail(models.Model):
    """接口业务流详细表"""
    name = models.CharField(max_length=200)
    create_date = models.DateTimeField(auto_now=True)
    case = models.ForeignKey(InCaseList, null=True)
    api = models.ForeignKey(api_business)

    # def __unicode__(self):
    #     return self.name


class Ap(models.Model):
    """接口执行表"""
    name = models.CharField(max_length=200, unique=True)
    create_date = models.DateTimeField(auto_now=True)
    edit_date = models.CharField(max_length=200)
    user = models.ForeignKey(User)

    # def __unicode__(self):
    #     return self.name


class ap_detail(models.Model):
    """接口执行详细表"""
    name = models.CharField(max_length=500)
    case_type = models.CharField(max_length=200)
    create_date = models.DateTimeField(auto_now=True)
    edit_date = models.CharField(max_length=200)
    case = models.ForeignKey(InCaseList, null=True)
    api = models.ForeignKey(api_business, null=True)
    ap = models.ForeignKey(Ap)
