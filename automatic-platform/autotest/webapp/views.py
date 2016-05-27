# -.- coding:utf-8 -.-
import sys, time, os
reload(sys)
sys.setdefaultencoding("utf-8")
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import *
from models import *
from runTest import runTest
import logging, os
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.http import Http404
from django.db import connection, transaction, IntegrityError
from django.contrib import auth
import threading, json
from django.contrib.auth import login, logout, authenticate      #Django 在 django.contrib.auth 提供了2个函数: authenticate() 和 login() 。如果通过给定的用户名和密码做认证，请使用 authenticate() 函数。他接收2个参数，一个是 username 一个是 password 。如果认证成功，它返回一个 User 对象。如果密码无效，它返回一个 None
from django.contrib.auth.decorators import login_required
from django.db import transaction
@transaction.autocommit


def get_time():
    now = time.strftime("%Y年%m月%d日 %H:%M", time.localtime(time.time()))
    return now

def login_view(request):
    if request.method == "POST":
        user_name = request.POST.get("username")
        pass_word = request.POST.get("password")
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            login(request, user)
            return HttpResponse("验证成功")
        else:
            return HttpResponse("用户名或密码错误")
    if request.method == "GET":
        return render_to_response("login.html")


def logout_page(request):  # 没有HTML文件
    """注销页面"""
    logout(request)
    return HttpResponseRedirect("/")


def sql_commend(sql):
    # 封装的自定义sql语句
    cursor = connection.cursor()
    ret=" "
    try:
        cursor.execute(sql)
        if "select" in sql.lower():
            # 如果是查询，就返回值
            print u"当前SQL语句为查询，SQL语句为：%s" % sql
            def dictfechall():
                desc = cursor.description
                return [
                    dict(zip([col[0] for col in desc], row))
                    for row in cursor.fetchall()
                    ]
            row = dictfechall()
            return row
        else:
            # 否则就是增 删 改 语句，提交操作
            print u"当前SQL语句为执行，SQL语句为：%s" % sql
            transaction.commit_unless_managed() # 提交事务到数据库
    except Exception,e:
        ret=str(e)


def get_client_ip(request):
    try:
        real_ip = request.META['HTTP_X_FORWARDED_FOR']
        regip = real_ip.split(",")[0]
    except:
        try:
            regip = request.META['REMOTE_ADDR']
        except:
            regip = ""
    return regip



@login_required
def get_project_name(request):
    # 通过模糊查询project的用户名得到相应的项目
    login_username = request.user
    project = Project.objects.all()
    project_query = Project.objects.filter(pro_user__contains=login_username) #__contains相当于模糊查询like
    project_name = []
    #项目列表
    pro={}
    for i in project_query:
        project_name.append(i.name)
        case_count=Case.objects.filter(project_id=i.id).count()
        pro[i.id]={}
        pro[i.id]["pro_name"]=i.name
        pro[i.id]["case_count"]=case_count
        pro[i.id]["create_time"]=i.create_time
        pro[i.id]["test_type"]=i.test_type

    #场景列表
    #执行列表

    #获取auth表中的first_name和是否为管理员
    user_object = User.objects.get(username=login_username)
    first_name = user_object.first_name
    is_superuser = user_object.is_superuser

    return project_name, is_superuser, first_name, pro


@login_required
def index(request):
    function_object = get_project_name(request)
    project_name = function_object[0]
    is_superuser = function_object[1]
    first_name = function_object[2]
    pro_detail=function_object[3]
    return render_to_response("index.html", {"project_name": project_name, "is_superuser": is_superuser,
                                             "first_name": first_name,"pro_detail":pro_detail})

@login_required
def case_list(request):
    if request.method == 'POST':
        action = request.POST.get("action")
        if action == u"页面跳转":
            pro_name = request.POST.get("redirect")
            case_list = Project.objects.get(name=pro_name).case_set.all()
            return render_to_response("case_list.html", {"pro_name": pro_name, "case_list": case_list})

        if action == u"删除用例":
            try:
                case_id = request.POST.get("case_id")

                filter_business_stp = Business_stp.objects.filter(case_id=case_id)
                fileter_Execution_detail = Execution_detail.objects.filter(case_id=case_id)

                if bool(filter_business_stp) and bool(fileter_Execution_detail):
                    case_name = filter_business_stp[0].name
                    business_name = Business.objects.get(pk=(filter_business_stp[0].business_id)).name
                    execution_name = Test_execution.objects.get(pk=(fileter_Execution_detail[0].perform_id)).name
                    return HttpResponse(u"1、用例:‘%s’存在与业务流:‘%s’中\n2、存在与测试执行:‘%s’中\n3、请先在业务流和测试执行中删除该用例" % (
                        case_name, business_name, execution_name))

                elif bool(filter_business_stp) == True and bool(fileter_Execution_detail) == False:
                    case_name = filter_business_stp[0].name
                    business_name = Business.objects.get(pk=(filter_business_stp[0].business_id)).name
                    return HttpResponse(u"1、用例:‘%s’存在与业务流:'%s'中\n2、请先在业务流中删除该用例" % (case_name, business_name))

                elif bool(fileter_Execution_detail) == True and bool(filter_business_stp) == False:
                    case_name = fileter_Execution_detail[0].name
                    execution_name = Test_execution.objects.get(pk=(fileter_Execution_detail[0].perform_id)).name
                    return HttpResponse(u"1、用例:‘%s’存在与测试执行:'%s'中\n2、请先在测试执行中删除该用例" % (case_name, execution_name))

                else:
                    try:
                        Case.objects.get(id=case_id).delete()
                        print u"删除步骤成功，当前用例ID是%s" % case_id
                        return HttpResponse("删除成功")
                    except:
                        print u"删除步骤失败，当前用例ID是%s" % case_id
                        return HttpResponse("删除失败")
            except Exception,e:
                print str(e)

        if action == u"测试调试":
            try:
                # 取ID
                case_id = request.POST.get("case_id")  # 点击测试调试，返回用例的ID
                # 取名称
                get_name = Case.objects.get(pk=case_id)
                case_name = str(get_name.name)
                # 取IP
                regip = get_client_ip(request)
                runTest(regip, 'case', case_id, case_name)
                # 取当前用户名
                username=request.POST.get("username")
                Caseaction.objects.create(actor=username,action="debug",case_id=case_id)

                return HttpResponse("开始调试")
            except:
                return HttpResponse("调试失败")

        if action == u"查看用例详细信息":
            try:
                # 获取用例ID
                case_id = request.POST.get("case_id")
                # 获取用例
                case_obj = Case.objects.get(id=case_id)
                # 获取用例细节
                case_detail = case_obj.case_process_set.all()
                # 获取项目名称
                pro_obj = Project.objects.get(id=Case.objects.get(id=case_id).project_id)
                pro_name = pro_obj.name


                # 获取用例的操作历史数据
                history_list=case_obj.caseaction_set.all().order_by('-actiondate')
                return render_to_response("show_case_history.html", {"current_pro_name": pro_name,
                                                            "case_obj": case_obj,"case_detail": case_detail,"history_list":history_list})

            except Exception,e:
                print str(e)





@login_required
def add_business(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == u"页面跳转":
            pro_name = request.POST.get("redirect")
            print "获取该用户下所有项目的所有用例"
            pro_list = Project.objects.filter(pro_user__contains=request.user)

            case_list = []
            incase_list = []
            for i in pro_list:
                case_list.extend(i.case_set.filter(status="有效"))
                incase_list.extend(i.incaselist_set.filter(status="有效"))

            return render_to_response("add_business.html", {"current_pro_name": pro_name, "pro_list":pro_list ,"case_list": case_list ,"incase_list": incase_list})

        if action == u"维护业务流":
            """业务流列表点击维护业务流载入数据"""
            bus_id = request.POST.get("bus_id")

            bus_obj = Business.objects.get(id=bus_id)
            bus_detail = bus_obj.business_stp_set.all()

            current_pro_name = Project.objects.get(id=bus_obj.Project_id).name

            pro_list = Project.objects.filter(pro_user__contains=request.user)
            case_list = []
            incase_list = []
            for i in pro_list:
                case_list.extend(i.case_set.filter(status="有效"))
                incase_list.extend(i.incaselist_set.filter(status="有效"))
            return render_to_response("add_business.html",
                                      {"bus_obj": bus_obj, "bus_detail": bus_detail, "case_list": case_list,
                                       "incase_list": incase_list,"current_pro_name": current_pro_name})

        if action == u"添加用例":
            """添加用例的应用按钮,ajax回传"""
            caseid_list = request.POST.getlist("caseid_list[]")
            incaseid_list = request.POST.getlist("incaseid_list[]")
            case_list = []
            incase_list = []
            for i in caseid_list:
                case_list.extend(Case.objects.filter(id=i))

            for i in incaseid_list:
                incase_list.extend(InCaseList.objects.filter(id=i))

            return render_to_response("business_ajax.html", {"case_list": case_list ,"incase_list": incase_list})

        if action == u"保存业务流":
            bus_name = request.POST.get("ywlname")
            case_id = request.POST.getlist("case_id")
            category = request.POST.getlist("category")
            case_name = request.POST.getlist("case_name")
            case_date = request.POST.getlist("case_date")
            case_nature = request.POST.getlist("case_nature")
            pro_name = request.POST.get("current_pro_name")
            bool_name = Business.objects.filter(name=bus_name)
            user_name=request.user

            if bool_name:
                return HttpResponse("名称重复")
            else:
                try:
                    bus_obj = Project.objects.get(name=pro_name).business_set.create(name=bus_name, category="业务流用例",creator=request.user)
                    for i in range(len(case_id)):
                        bus_obj.business_stp_set.create(name=case_name[i], case_id=case_id[i], date=case_date[i],
                                                        case_nature=case_nature[i],category=category[i])

                    # 将创建业务流加入历史操作表
                    bus_obj.businessaction_set.create(actor=user_name,action="create")
                    return HttpResponse("保存成功")
                except Exception,e:
                    print str(e)
                    return HttpResponse("保存失败")

        if action == u"修改业务流":
            bus_id = request.POST.get("bus_id")
            bus_name = request.POST.get("ywlname")
            case_id = request.POST.getlist("case_id")
            category = request.POST.getlist("category")
            case_name = request.POST.getlist("case_name")
            case_nature = request.POST.getlist("case_nature")
            pro_name = request.POST.get("current_pro_name")
            user_name=request.user
            try:
                bus_obj=Business.objects.get(id=bus_id)
                bus_stp_obj=bus_obj.business_stp_set.all()

                old_case_id=[]
                for m in bus_stp_obj:
                    old_case_id.append(m.case_id)
                print old_case_id

                Project.objects.get(name=pro_name).business_set.filter(id=bus_id).update(name=bus_name)
                # 修改业务流名称
                if bus_obj.name != bus_name:
                    bus_obj.businessaction_set.create(actor=user_name,action="edit",edit_field="name",old_field_value=bus_obj.name,new_field_value=bus_name)


                # 修改业务流的name以后要在 execution_detail 中也做修改
                Execution_detail.objects.filter(case_id=bus_id).update(name=bus_name)

                add = list(set(case_id).difference(set(old_case_id)))
                delete = list(set(old_case_id).difference(set(case_id)))
                update = list(set(case_id).intersection(set(old_case_id)))

                print "新增的用例ID---",add
                print "删除的用例ID---",delete
                print "既不是新增也没被删除的用例ID---",update

                for j in add:
                    i=0
                    for a in case_id:
                        if a == j:
                            print "增加用例的ID是：",a
                            print "增加用例的名称是：",case_name[i]
                            bus_obj.businessaction_set.create(actor=request.user,action="addcase",case_name=case_name[i])
                        i=i+1

                for k in delete:
                    d=bus_obj.business_stp_set.get(case_id=k)
                    bus_obj.businessaction_set.create(actor=request.user,action="delcase",case_name=d.name)

                Project.objects.get(name=pro_name).business_set.filter(id=bus_id).update(name=bus_name)
                bus_stp_obj = Business.objects.get(id=bus_id).business_stp_set.all()

                for i in range(len(case_id)):
                    try:
                        Business.objects.get(id=bus_id).business_stp_set.filter(id=bus_stp_obj[i].id).update(
                            name=case_name[i], case_id=case_id[i], case_nature=case_nature[i])
                    except:
                        Business.objects.get(id=bus_id).business_stp_set.create(name=case_name[i], case_id=case_id[i],
                                                                                case_nature=case_nature[i])

                if len(case_id) < len(bus_stp_obj):
                    del_step = bus_stp_obj[len(case_id):len(bus_stp_obj)]
                    for i in del_step:
                        i.delete()

                return HttpResponse("保存成功")
            except Exception,e:
                print str(e)
                return HttpResponse("保存失败")


@login_required
def business_list(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == u"页面跳转":
            pro_name = request.POST.get("redirect")
            business_list = Project.objects.get(name=pro_name).business_set.all()
            return render_to_response("business_list.html",
                                      {"business_list": business_list, "current_pro_name": pro_name})

        if action == u"删除业务流":
            get_id = request.POST.get("bu_id")
            filter_bus = Execution_detail.objects.filter(category="业务流用例", case_id=get_id)

            if filter_bus:
                perform_id = Execution_detail.objects.get(category="业务流用例", case_id=get_id).perform_id
                return HttpResponse(u"1、ID为%s的业务流存在测试执行中,测试执行ID是%s\n2、请现在执行中删除该业务流" % (get_id, perform_id))
            else:
                Business.objects.get(pk=get_id).delete()
                Business_stp.objects.filter(business_id=get_id).delete()

        if action == u"调试业务流":
            try:
                bus_id = request.POST.get("dbg_id")
                bus_obj=Business.objects.get(id=bus_id)
                bus_name = bus_obj.name
                regip = get_client_ip(request)
                runTest(regip, "business", bus_id, bus_name)
                # 记录调试操作
                bus_obj.businessaction_set.create(actor=request.user,action="debug")
                return HttpResponse("开始调试")
            except:
                return HttpResponse("调试失败")

        if action == u"复制业务流":
            try:
                bus_id = request.POST.get("bus_id")
                copybus_obj = Business.objects.get(id=bus_id)
                bus_detail = copybus_obj.business_stp_set.all()

                current_pro_name = Project.objects.get(id=copybus_obj.Project_id).name

                pro_list = Project.objects.filter(pro_user__contains=request.user)
                case_list = []
                for i in pro_list:
                    case_list.extend(i.case_set.filter(status="有效"))
                return render_to_response("add_business.html",
                                          {"copybus_obj": copybus_obj, "bus_detail": bus_detail, "case_list": case_list,
                                           "current_pro_name": current_pro_name})

                return HttpResponse("开始调试")
            except:
                return HttpResponse("调试失败")

        if action == u"查看业务流详细信息":
            try:
                # 获取业务流的id
                bus_id = request.POST.get("bus_id")

                # 业务流对象
                bus_obj = Business.objects.get(id=bus_id)

                # 获取业务流所有用例信息
                bus_detail = bus_obj.business_stp_set.all()

                # 获取项目名称
                pro_obj = Project.objects.get(id=Business.objects.get(id=bus_id).Project_id)
                pro_name = pro_obj.name

                # 获取历史记录
                history_list=Businessaction.objects.filter(Business_id=bus_id).order_by('-actiondate')

                return render_to_response("show_business_detail.html",{"current_pro_name": pro_name, "bus_obj":bus_obj,
                                                                       "bus_detail":bus_detail, "history_list":history_list})
            except Exception,e:
                print str(e)



@login_required
def case_ajax(request):
    if request.method == "POST":
        stp_list = []
        case_id = request.POST.getlist("id[]")
        for i in case_id:
            case_stp = Case.objects.get(pk=i).case_process_set.all()
            stp_list.extend(case_stp)
        return render_to_response("add_case_ajax.html", {"case_stp": stp_list})

    return render_to_response("add_case_ajax.html")





@login_required
def add_perform(request):
    # 增加测试执行
    if request.method == "POST":
        action = request.POST.get("action")

        if action == u"新增执行":
            print u"新增执行"
            # 获取用户名，取用户表对象
            user_obj = User.objects.get(username=request.user)
            try:
                # 通过用户表对象创建执行表
                exe_name = request.POST.get('perform_n')
                bool_name = Test_execution.objects.filter(name=exe_name)
                if bool_name:
                    return HttpResponse("名称重复")
                else:
                    user_obj.test_execution_set.create(name=exe_name,creator=request.user)
                    # 获取执行表对象
                    perform_detail = Test_execution.objects.get(name=exe_name)

                    # 获取长度
                    date_len = len(request.POST.getlist("date"))

                    # 根据长度循环写入到执行详细表中
                    for i in range(date_len):
                        name_list = request.POST.getlist("name")
                        case_nature_list = request.POST.getlist("case_nature")
                        category_list = request.POST.getlist("category")
                        case_id = request.POST.getlist("case_id")
                        perform_detail.execution_detail_set.create(name=name_list[i],
                                                                   case_nature=case_nature_list[i],
                                                                   category=category_list[i],
                                                                   case_id=case_id[i])
                    # 创建执行写入历史操作表
                    per_obj=Test_execution.objects.get(name=exe_name)
                    per_obj.executionaction_set.create(actor=request.user,action="create")
                    return HttpResponse("保存成功")
            except:
                return HttpResponse("保存失败")

        if action == u"复制执行":
            execution_id = request.POST.get("per_id")
            execution_obj = Test_execution.objects.get(id=execution_id)
            exe_detail = execution_obj.execution_detail_set.all()
            project_obj = Project.objects.filter(pro_user__contains=request.user)

            return render_to_response("add_perform.html",
                                      { "redirect": "复制执行","copy_execution_obj": execution_obj, "exe_detail": exe_detail,
                                       "project_obj": project_obj})

        if action == u"维护执行":
            """点击维护执行跳转页面"""
            execution_id = request.POST.get("per_id")
            execution_obj = Test_execution.objects.get(id=execution_id)
            exe_detail = execution_obj.execution_detail_set.all()
            project_obj = Project.objects.filter(pro_user__contains=request.user)

            return render_to_response("add_perform.html",
                                      {"redirect": "维护执行", "execution_obj": execution_obj, "exe_detail": exe_detail,
                                       "project_obj": project_obj})
        if action == u"修改执行":
            per_id = request.POST.get("per_id")
            per_name = request.POST.get("perform_n")
            category = request.POST.getlist("category")
            name = request.POST.getlist("name")
            case_nature = request.POST.getlist("case_nature")
            case_id = request.POST.getlist("case_id")
            print case_id

            ex_obj=Test_execution.objects.get(id=per_id)
            ex_detail_obj = ex_obj.execution_detail_set.all()
            old_case_id=[]
            for m in ex_detail_obj:
                old_case_id.append(m.case_id)
            print old_case_id

            try:
                exe_obj=Test_execution.objects.get(id=per_id)

                Test_execution.objects.filter(id=per_id).update(name=per_name)

                # 记录操作--修改执行名称
                if exe_obj.name != per_name:
                    exe_obj.executionaction_set.create(actor=request.user,action="edit",edit_field="name",
                                                       old_field_value=exe_obj.name,new_field_value=per_name)
            except Exception,e:
                print str(e)
                return HttpResponse("名称重复")

            try:
                add = list(set(case_id).difference(set(old_case_id)))
                delete = list(set(old_case_id).difference(set(case_id)))
                update = list(set(case_id).intersection(set(old_case_id)))

                print "新增的用例ID---",add
                print "删除的用例ID---",delete
                print "既不是新增也没被删除的用例ID---",update

                for j in add:
                    i=0
                    for a in case_id:
                        if a == j:
                            print "增加用例的ID是：",a
                            print "增加用例的名称是：",name[i]
                            exe_obj.executionaction_set.create(actor=request.user,action="addcase",case_name=name[i])
                        i=i+1

                for k in delete:
                    d=exe_obj.execution_detail_set.get(case_id=k)
                    exe_obj.executionaction_set.create(actor=request.user,action="delcase",case_name=d.name)


                exe_obj = Test_execution.objects.get(id=per_id)
                exe_detail_obj = exe_obj.execution_detail_set.all()
                for i in range(len(case_id)):
                    try:
                        exe_obj.execution_detail_set.filter(id=exe_detail_obj[i].id).update(name=name[i],
                                                                                            case_nature=case_nature[i],
                                                                                            category=category[i],
                                                                                            case_id=case_id[i])
                    except:
                        exe_obj.execution_detail_set.create(name=name[i], case_nature=case_nature[i],
                                                            category=category[i], case_id=case_id[i])

                if len(case_id) < len(exe_detail_obj):
                    del_obj = exe_detail_obj[len(case_id):len(exe_detail_obj)]
                    for i in del_obj:
                        i.delete()

                return HttpResponse("保存成功")
            except Exception,e:
                print str(e)
                return HttpResponse("保存失败")

    if request.method == "GET":
        """新增执行"""
        # 获取当前登录用户名，筛选改用户下所有项目中的所有用例和业务流
        project_obj = Project.objects.filter(pro_user__contains=request.user)

        return render_to_response("add_perform.html", {"project_obj": project_obj})


@login_required
def perform_ajax(request):
    # 测试执行A-Jax页面，为新增提供ajax动态
    if request.method == "POST":
        try:
            action = request.POST.get("action")
            tr_list = []
            if action == "添加用例":
                case_id_list = request.POST.getlist("case[]")
                for i in case_id_list:
                    case_obj = Case.objects.filter(pk=i)
                    tr_list.extend(case_obj)

                incase_list = request.POST.getlist("incase[]")
                for i in incase_list:
                    incase_obj = InCaseList.objects.filter(pk=i)
                    tr_list.extend(incase_obj)

                bus_list = request.POST.getlist("bus[]")
                for i in bus_list:
                    bus_obj = Business.objects.filter(pk=i)
                    tr_list.extend(bus_obj)

            return render_to_response("perform_ajax.html", {"tr_list": tr_list})
        except Exception,e:
            print str(e)



@login_required
def perform_list(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == u"删除执行":
            try:
                get_id = request.POST.get("get_id")
                # 删除执行中的用例和业务流
                # del_step = "DELETE from webapp_execution_detail where perform_id= %s" % get_id
                # sql_commend(del_step)
                # 删除执行
                # del_case = "DELETE from webapp_test_execution where id= %s" % get_id
                # sql_commend(del_case)
                Test_execution.objects.get(id=get_id).delete()
                return HttpResponse("删除成功")
            except Exception,e:
                print str(e)
                return HttpResponse("删除失败")


        if action == u"运行执行":
            try:
                # 取ID
                case_id = request.POST.get("case_id")
                exe_obj=Test_execution.objects.get(pk=case_id)
                # 将调试操作写入操作记录表
                exe_obj.executionaction_set.create(actor=request.user,action="debug")
                # 取名称
                get_name = Test_execution.objects.get(pk=case_id)
                case_name = str(get_name.name)

                # 取客户端IP
                regip = get_client_ip(request)

                # 多线程启动客户端和服务端代码
                def run_key():
                    print "开始运行服务端自动化框架"
                    # os.system(r"D:\Project\autotest\webapp\run_automation.bat")

                threads = []
                t1 = threading.Thread(target=run_key)
                threads.append(t1)
                t2 = threading.Thread(runTest(regip, "perform", case_id, case_name))
                threads.append(t2)

                for i in threads:
                    print "start threading"
                    i.setDaemon(True)
                    i.start()
                i.join()
                return HttpResponse("开始运行")
            except:
                return HttpResponse("运行失败")

        if action == u"查看执行详细信息":
            try:
                # 获取执行的id
                per_id = request.POST.get("per_id")

                # 执行对象
                per_obj = Test_execution.objects.get(id=per_id)

                # 获取执行所有用例信息
                per_detail = per_obj.execution_detail_set.all()

                # 获取历史记录
                history_list=Executionaction.objects.filter(Execution_id=per_id).order_by('-actiondate')

                return render_to_response("show_perform_detail.html",{ "execution_obj":per_obj,
                                                                       "exe_detail":per_detail, "history_list":history_list})
            except Exception,e:
                print str(e)


    if request.method == "GET":
        # ---GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变-----

        function_object = get_project_name(request)
        project_name = function_object[0]
        is_superuser = function_object[1]
        first_name = function_object[2]

        # 获取所有执行
        user_perform = Test_execution.objects.all()

        return render_to_response("perform_list.html", {"user_perform": user_perform, "project_name": project_name,
                                                        "is_superuser": is_superuser, "first_name": first_name},
                                  context_instance = RequestContext(request))



@login_required
def user_management(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == u"新增用户":
            add_user = request.POST["add_user"]
            password = request.POST["password"]
            first_name = request.POST["first_name"]
            status = request.POST["chest"]
            make_pw = make_password(password, None, hasher="default")
            try:
                User.objects.create(username=add_user, password=password, first_name=first_name, is_staff=status,
                                    is_active=status)
                return HttpResponse("保存成功")
            except:
                return HttpResponse("保存失败")

        if action == u"维护用户":
            id = request.POST["id"]
            name = request.POST["name"]
            first_name = request.POST["first_name"]
            password = request.POST["password"]
            status = int(request.POST["chest"])  # 数据库中该字段为int
            make_pw = make_password(password, None, hasher="default")
            user_ob = User.objects.get(id=id)
            old_first_name = user_ob.first_name
            username = request.POST["username"]
            # print "="*30,status

            if(password):
                try:
                    user_ob.username, user_ob.first_name, user_ob.is_active ,user_ob.password= name,first_name,status,make_pw
                    user_ob.save()
                    if(old_first_name == username):
                         return HttpResponse("保存成功，用户需要重新登录")
                    else:
                         return HttpResponse("保存成功")
                except:
                    return HttpResponse("保存失败")

            # 如果密码空，说明用户没有修改密码，则不需要保存密码的值
            else:
                try:
                    user_ob.username, user_ob.first_name, user_ob.is_active = name, first_name, status
                    user_ob.save()
                    return HttpResponse("保存成功")
                except:
                    return HttpResponse("保存失败")



        if action == u"删除用户":
            user_id = request.POST.get("user_id")
            print user_id
            try:
                del_user = "DELETE from auth_user where id= %s" % user_id
                sql_commend(del_user)
                return HttpResponse("删除成功")
            except:
                return HttpResponse("删除失败")

        if action == u"重置密码":
            user_name = request.POST.get("user_name")
            passwd = request.POST.get("passwd")
            try:
                user_obj = User.objects.get(username=user_name)
                user_obj.set_password(passwd)
                user_obj.save()
                return HttpResponse("修改成功")
            except:
                return HttpResponse("修改失败")

    if request.method == "GET":
        # 获取用户表auth_user对象,并做分页功能
        user = User.objects.all()
        return render_to_response("user_management.html",{"user": user})



@login_required
def project_management(request):
    if request.POST:
        action = request.POST.get("action")

        if action == u"编辑项目":
            # 获取项目ID
            pro_id=request.POST.get("pro_id")
            pro_obj=Project.objects.get(id=pro_id)
            print pro_id
            # 获取项目成员
            user = User.objects.all()

            db_obj=ProSetting.objects.filter(proName_id=pro_id).all()
            return render_to_response("add_project.html",{"userlist": user,"pro_obj":pro_obj,"db_obj":db_obj})

        if action == u"删除项目":
            # 获取待删除项目的id
            pro_id = request.POST.get("pro_id")
            try:
                Project.objects.get(pk=pro_id).delete()
                return HttpResponse("删除成功")
            except Exception,e:
                print e
                return HttpResponse("删除失败")

        if action == u"查看项目详细信息":
            pro_id=request.POST.get("pro_id")
            pro_obj=Project.objects.get(id=pro_id)
            print "查看项目历史操作的项目ID是：",pro_id
            history_list=Projectaction.objects.filter(Project_id=pro_id).order_by('-actiondate')

            db_obj=ProSetting.objects.filter(proName_id=pro_id)
            return render_to_response("show_project_detail.html", {"pro_obj":pro_obj ,"history_list":history_list,"db_obj": db_obj})


    if request.method == "GET":
        # 获取所有用户列表
        user_list = User.objects.all()
        # 获取所有项目列表，并做分页
        project_list = Project.objects.all()
        return render_to_response("project_management.html", {"project_list": project_list,
                                                              "user_list": user_list})


@login_required
def add_project(request):
    if request.POST:
        action = request.POST.get("action")
        if action == u"页面跳转":
            user = User.objects.all()
            return render_to_response("add_project.html",{"userlist": user})

        if action == u"保存修改":
            try:
                pro_id = request.POST.get("project_id")
                pro_name = request.POST.get("pro_name")
                pro_url = request.POST.get("pro_url")
                pro_status = request.POST.get("pro_status")
                test_type = request.POST.get("test_type")
                memberlist = request.POST.get("memberlist")
                print pro_name

                db_name_list = request.POST.getlist("db_name")
                db_address_list = request.POST.getlist("db_address")
                db_port_list = request.POST.getlist("db_port")
                db_connecttype_list = request.POST.getlist("db_connecttype")
                db_connectdata_list = request.POST.getlist("db_connectdata")
                db_username_list = request.POST.getlist("db_username")
                db_password_list = request.POST.getlist("db_password")
                db_status_list = request.POST.getlist("db_status")

                if test_type != "Web测试" :
                    for i in range(len(db_status_list)):
                        if db_status_list[i] == "True":
                            if db_name_list[i] ==""  or db_address_list[i] =="" or db_port_list[i] =="" or db_connecttype_list[i] =="" or db_connectdata_list[i] =="" or db_username_list[i] =="" or db_password_list[i] =="":
                                return HttpResponse("项目的测试类型含有接口测试，数据库信息为必填")

                flag = 0;
                for i in db_status_list:
                    if i == "True" and flag == 0:
                        flag = 1;
                    elif i == "True" and flag == 1:
                        return HttpResponse("一个项目不能有两个数据库同时启用")


                # 更新数据库信息，有的则update，没有则create
                db_obj = Project.objects.get(id=pro_id).prosetting_set.all()

                for i in range(len(db_name_list)):
                    try:
                        obj=ProSetting.objects.get(id=db_obj[i].id)

                        print obj
                        print "数据库详细信息*****ID:%s   name:%s " % (db_obj[i].id, db_name_list[i])

                        ProSetting.objects.filter(id=db_obj[i].id).update(envName=db_name_list[i],
                            address=db_address_list[i],port=db_port_list[i],connectType=db_connecttype_list[i],connectData=db_connectdata_list[i],
                            userName=db_username_list[i],passWord=db_password_list[i],is_used=db_status_list[i])

                        if obj.envName != db_name_list[i]:
                            Projectaction.objects.create(actor=request.user,action="editDB",Project_id=pro_id,edit_field="envName",envName=obj.envName,
                                                         old_field_value=obj.envName,new_field_value=db_name_list[i])
                        if obj.address != db_address_list[i]:
                            Projectaction.objects.create(actor=request.user,action="editDB",Project_id=pro_id,edit_field="address",envName=obj.envName,
                                                         old_field_value=obj.address,new_field_value=db_address_list[i])
                        if obj.port != db_port_list[i]:
                            Projectaction.objects.create(actor=request.user,action="editDB",Project_id=pro_id,edit_field="port",envName=obj.envName,
                                                         old_field_value=obj.port,new_field_value=db_port_list[i])
                        if obj.connectType != db_connecttype_list[i]:
                            Projectaction.objects.create(actor=request.user,action="editDB",Project_id=pro_id,edit_field="connectType",envName=obj.envName,
                                                         old_field_value=obj.connectType,new_field_value=db_connecttype_list[i])
                        if obj.connectData != db_connectdata_list[i]:
                            Projectaction.objects.create(actor=request.user,action="editDB",Project_id=pro_id,edit_field="connectData",envName=obj.envName,
                                                         old_field_value=obj.connectData,new_field_value=db_connectdata_list[i])
                        if obj.userName != db_username_list[i]:
                            Projectaction.objects.create(actor=request.user,action="editDB",Project_id=pro_id,edit_field="userName",envName=obj.envName,
                                                         old_field_value=obj.userName,new_field_value=db_username_list[i])
                        if obj.passWord != db_password_list[i]:
                            Projectaction.objects.create(actor=request.user,action="editDB",Project_id=pro_id,edit_field="passWord",envName=obj.envName,
                                                         old_field_value=obj.passWord,new_field_value = db_password_list[i])
                        if obj.is_used != db_status_list[i]:
                            Projectaction.objects.create(actor=request.user,action="editDB",Project_id=pro_id,edit_field="status",envName=obj.envName,
                                                         old_field_value=obj.status,new_field_value=db_status_list[i])
                    except Exception,e:
                        print str(e)
                        print "POST长度大于数据库长度,开始创建"
                        ProSetting.objects.create(envName=db_name_list[i],
                                address=db_address_list[i],port=db_port_list[i],connectType=db_connecttype_list[i],connectData=db_connectdata_list[i],
                                userName=db_username_list[i],passWord=db_password_list[i],is_used=db_status_list[i],proName_id=pro_id)
                        # 数据库信息
                        Projectaction.objects.create(actor=request.user,action="addDB",Project_id=pro_id,edit_field="envName",new_field_value=db_name_list[i])
                        Projectaction.objects.create(actor=request.user,action="addDB",Project_id=pro_id,edit_field="address",new_field_value=db_address_list[i])
                        Projectaction.objects.create(actor=request.user,action="addDB",Project_id=pro_id,edit_field="port",new_field_value=db_port_list[i])
                        Projectaction.objects.create(actor=request.user,action="addDB",Project_id=pro_id,edit_field="connectType",new_field_value=db_connecttype_list[i])
                        Projectaction.objects.create(actor=request.user,action="addDB",Project_id=pro_id,edit_field="connectData",new_field_value=db_connectdata_list[i])
                        Projectaction.objects.create(actor=request.user,action="addDB",Project_id=pro_id,edit_field="userName",new_field_value=db_username_list[i])
                        Projectaction.objects.create(actor=request.user,action="addDB",Project_id=pro_id,edit_field="passWord",new_field_value=db_password_list[i])
                        Projectaction.objects.create(actor=request.user,action="addDB",Project_id=pro_id,edit_field="is_used",new_field_value=db_status_list[i])

                post_length = len(db_name_list)
                db_len = Project.objects.get(id=pro_id).prosetting_set.all().count()

                try:
                    if post_length < db_len:
                        print "POST数据长度小于数据库中长度"
                        del_obj = Project.objects.get(id=pro_id).prosetting_set.all()[post_length:db_len]

                        print "获取到要删除的数据库对象:%s,开始循环删除多余的数据" % del_obj
                        for i in del_obj:
                            print i.id
                            Project.objects.get(id=pro_id).projectaction_set.create(actor=request.user,action="delDB",envName=i.envName)
                            i.delete()
                        print "删除成功"
                except:
                    return HttpResponse("删除数据库信息失败")

                # 更新项目基本信息
                project_ob = Project.objects.get(pk=pro_id)
                project_ob2=Project.objects.get(pk=pro_id)

                project_ob.name, project_ob.pro_user, project_ob.pro_status, project_ob.url ,project_ob.test_type = pro_name, memberlist, pro_status , pro_url ,test_type
                project_ob.save()
                 # 添加项目操作记录
                if(pro_url!=project_ob2.url):
                    Projectaction.objects.create(actor=request.user,action="edit",Project_id=pro_id,edit_field="url",old_field_value=project_ob2.url,new_field_value= pro_url)
                if(pro_name!=project_ob2.name):
                    Projectaction.objects.create(actor=request.user,action="edit",Project_id=pro_id,edit_field="name",old_field_value=project_ob2.name,new_field_value= pro_name)
                if(memberlist!=project_ob2.pro_user):
                    Projectaction.objects.create(actor=request.user,action="edit",Project_id=pro_id,edit_field="pro_user",old_field_value=project_ob2.pro_user,new_field_value= memberlist)
                if(pro_status!=project_ob2.pro_status):
                    Projectaction.objects.create(actor=request.user,action="edit",Project_id=pro_id,edit_field="pro_status",old_field_value=project_ob2.pro_status,new_field_value= pro_status)
                if(test_type!=project_ob2.test_type):
                    Projectaction.objects.create(actor=request.user,action="edit",Project_id=pro_id,edit_field="test_type",old_field_value=project_ob2.test_type,new_field_value=test_type)
                return HttpResponse("保存成功")

            except Exception,e:
                print str(e)
                return HttpResponse("保存失败")


        if action == u"保存新增":
            try:
                pro_name = request.POST.get("pro_name")
                bool_name = Project.objects.filter(name=pro_name)
                pro_url = request.POST.get("pro_url")
                pro_status = request.POST.get("pro_status")
                test_type = request.POST.get("test_type")
                memberlist = request.POST.get("memberlist")

                db_name_list = request.POST.getlist("db_name")
                db_address_list = request.POST.getlist("db_address")
                db_port_list = request.POST.getlist("db_port")
                db_connecttype_list = request.POST.getlist("db_connecttype")
                db_connectdata_list = request.POST.getlist("db_connectdata")
                db_username_list = request.POST.getlist("db_username")
                db_password_list = request.POST.getlist("db_password")
                db_status_list = request.POST.getlist("db_status")

                if bool_name:
                    return HttpResponse("名称重复")

                if test_type != "Web测试" :
                    for i in range(len(db_status_list)):
                        if db_status_list[i] == "True":
                            if db_name_list[i] ==""  or db_address_list[i] =="" or db_port_list[i] =="" or db_connecttype_list[i] =="" or db_connectdata_list[i] =="" or db_username_list[i] =="" or db_password_list[i] =="":
                                return HttpResponse("项目的测试类型含有接口测试，数据库信息为必填")

                flag = 0
                for i in db_status_list:
                    if i == "True" and flag == 0:
                        flag = 1
                    elif i == "True" and flag == 1:
                        return HttpResponse("一个项目不能有两个数据库同时启用")

                # 创建项目基本信息
                Project.objects.create(name=pro_name, url=pro_url, pro_user=memberlist,
                                       pro_status=pro_status,test_type=test_type)
                pro_id=Project.objects.get(name=pro_name).id
                # 添加项目操作记录
                Projectaction.objects.create(actor=request.user,action="create",Project_id=pro_id)

                # 更新数据库信息，有的则update，没有则create
                db_obj = Project.objects.get(id=pro_id).prosetting_set.all()

                for i in range(len(db_name_list)):
                    ProSetting.objects.create(envName=db_name_list[i],
                            address=db_address_list[i],port=db_port_list[i],connectType=db_connecttype_list[i],connectData=db_connectdata_list[i],
                            userName=db_username_list[i],passWord=db_password_list[i],is_used=db_status_list[i],proName_id=pro_id)
                    # 数据库信息
                    Projectaction.objects.create(actor=request.user,action="addDB",Project_id=pro_id,edit_field="envName",new_field_value=db_name_list[i])
                    Projectaction.objects.create(actor=request.user,action="addDB",Project_id=pro_id,edit_field="address",new_field_value=db_address_list[i])
                    Projectaction.objects.create(actor=request.user,action="addDB",Project_id=pro_id,edit_field="port",new_field_value=db_port_list[i])
                    Projectaction.objects.create(actor=request.user,action="addDB",Project_id=pro_id,edit_field="connectType",new_field_value=db_connecttype_list[i])
                    Projectaction.objects.create(actor=request.user,action="addDB",Project_id=pro_id,edit_field="connectData",new_field_value=db_connectdata_list[i])
                    Projectaction.objects.create(actor=request.user,action="addDB",Project_id=pro_id,edit_field="userName",new_field_value=db_username_list[i])
                    Projectaction.objects.create(actor=request.user,action="addDB",Project_id=pro_id,edit_field="passWord",new_field_value=db_password_list[i])
                    Projectaction.objects.create(actor=request.user,action="addDB",Project_id=pro_id,edit_field="is_used",new_field_value=db_status_list[i])
                return HttpResponse("保存成功")
            except Exception,e:
                print str(e)
                return HttpResponse("保存失败")


def method_ajax(request):
    # 加载定位方法，用于维护页面的jquery页面加载事件。
    method_by = Method.objects.all()
    return render_to_response("method_ajax.html", {"method": method_by})


def action_ajax(request):
    # 加载定位方法，用于维护页面的jquery页面加载事件。
    Action_fun = Action.objects.all()
    return render_to_response("action_ajax.html", {"action": Action_fun})


def base(request):
    if request.method == "POST":
        print request.POST
        return HttpResponse("你现在给的是一个POST请求")

    fun_list = Action.objects.all()
    return render_to_response("Base.html", {"fun_list": fun_list})


@login_required
def report(request):
    if request.method == "GET":
        result_list = Test_report.objects.all()
        return render_to_response("result.html", {"result_list": result_list})


def report_html(request, html_name):
    if html_name.endswith(".png"):
        # 通过url获取到的动态参数，如果为png则打开图片
        img_path = os.getcwd() + "\\templates\\result\\" + html_name
        ime_date = open(img_path, "rb").read()
        return HttpResponse(ime_date, content_type="image/png")
    else:
        # 否则获取到的就是.html文件，则渲染html
        return render_to_response(u"result\%s" % html_name)


def perform_case_ajax(request):
    """新增执行中添加用例的ajax"""
    if request.method == "POST":
        pro_id = request.POST.get("pro_id")
        case_list = Case.objects.filter(project_id=pro_id, status="有效", features="独立用例")
        incase_list = InCaseList.objects.filter(project_id=pro_id, status="有效")
        business_list = Business.objects.filter(Project_id=pro_id)
        return render_to_response("case_list_ajax.html", {"case_list": case_list, "incase_list": incase_list, "business_list": business_list})

@login_required
def add_element(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == u"页面跳转":
            pro_name = request.POST.get("redirect")

            fun = Method.objects.all()
            element_list = Project.objects.get(name=pro_name).element_set.all()
            return render_to_response("add_element.html",
                                      {"current_pro_name": pro_name, "fun": fun, "element_list": element_list})


        # 取POST的值
        e_name = request.POST.get("name")
        e_function = request.POST.get("function")
        e_value = request.POST.get("value")
        e_page_url = request.POST.get("page_url")
        e_desc = request.POST.get("desc")

        if action == u"删除元素":
            ele_id = request.POST.get("ele_id")
            print "%"*20,ele_id
            try:
                element.objects.get(pk=ele_id).delete()
                return HttpResponse("删除成功")
            except:
                return HttpResponse("删除失败")

        if action == u"修改元素":
            # 取当前项目为对象
            pro_name = request.POST.get("pro_name").strip()
            ele_id = request.POST.get("ele_id")
            username = request.POST.get("username")

            # 新的字段值
            ele_name = request.POST.get("ele_name")
            ele_fun = request.POST.get("ele_fun")
            ele_url = request.POST.get("ele_url")
            ele_value = request.POST.get("ele_value")
            ele_desc = request.POST.get("ele_desc")

            # e=element.objects.filter(name=ele_name, fun=ele_fun, values=ele_value)[0]
            # print "^"*30,e.id
            # print "-"*30,ele_id

            if not ele_name or not ele_fun or not ele_value:
                return HttpResponse("名称、定位方法、元素值为必填项")

            # elif   str(e.id) != str(ele_id):
            #     return HttpResponse("该元素已经存在")
            else:
                try:
                    element_obj=element.objects.get(id=ele_id)
                    element_obj2=element.objects.get(id=ele_id)
                    element_obj.name, element_obj.fun,element_obj.values,element_obj.desc,element_obj.page_url= ele_name,ele_fun,ele_value,ele_desc,ele_url
                    element_obj.save()

                    # Project.objects.get(name=pro_name).element_set.get(id=ele_id).update(name=ele_name, fun=ele_fun,
                    #                                                                     values=ele_value,
                    #                                                                     page_url=ele_url).save()

                    if(element_obj2.name!=ele_name):
                        Elementaction.objects.create(actor=username,action="edit",edit_field="name",old_field_value=element_obj2.name,new_field_value=ele_name,element_id=ele_id)

                    if(element_obj2.fun!=ele_fun):
                        Elementaction.objects.create(actor=username,action="edit",edit_field="fun",old_field_value=element_obj2.fun,new_field_value=ele_fun,element_id=ele_id)

                    if(element_obj2.page_url!=ele_url):
                        Elementaction.objects.create(actor=username,action="edit",edit_field="page_url",old_field_value=element_obj2.page_url,new_field_value=ele_url,element_id=ele_id)

                    if(element_obj2.values!=ele_value):
                        Elementaction.objects.create(actor=username,action="edit",edit_field="values",old_field_value=element_obj2.values,new_field_value=ele_value,element_id=ele_id)

                    if(element_obj2.desc!=ele_desc):
                        Elementaction.objects.create(actor=username,action="edit",edit_field="desc",old_field_value=element_obj2.desc,new_field_value=ele_desc,element_id=ele_id)

                    return HttpResponse("修改成功")

                except Exception,e:
                    print e
                    return HttpResponse("修改失败")

        if action == u"添加元素":
            try:
                pro_name = request.POST.get("pro_name").strip()
                pro_obj = Project.objects.get(name=pro_name)

                ele_name = request.POST.get("ele_name")
                ele_fun = request.POST.get("ele_fun")
                ele_url = request.POST.get("ele_url")
                ele_value = request.POST.get("ele_value")
                ele_desc = request.POST.get("ele_desc")
                username = request.POST.get("username")

                ele=element.objects.filter(name=ele_name, fun=ele_fun, values=ele_value)
                if not ele_name or not ele_fun or not ele_value:
                    return HttpResponse("名称、定位方法、元素值为必填项")
                elif ele:
                    return HttpResponse("该元素已经存在")
                else:
                    pro_obj.element_set.create(name=ele_name, fun=ele_fun, values=ele_value, desc=ele_desc,
                                                   page_url=ele_url, creator=username)
                    ele_id = element.objects.get(name=ele_name, fun=ele_fun, values=ele_value, desc=ele_desc,
                                                   page_url=ele_url, creator=username).id
                    Elementaction.objects.create(actor=username,action="create",element_id=ele_id)
                    return HttpResponse("添加成功")
            except Exception,e:
                print e
                return HttpResponse("添加失败")

        if action == u"查看元素详细信息":
            pro_name = request.POST.get("pro_name")
            ele_id = request.POST.get("ele_id")

            fun = Method.objects.all()
            element_list = Project.objects.get(name=pro_name).element_set.all()
            history_list=Elementaction.objects.filter(element_id=ele_id).order_by('-actiondate')

            return render_to_response("add_element.html",
                                      {"current_pro_name": pro_name, "fun": fun, "element_list": element_list,"history_list": history_list})
            # return render_to_response("add_element.html", {"history_list": history_list})




def process_ajax(request):
    """增加步骤"""
    return render_to_response("process_ajax.html")


def element_msg(request):
    ele_id = request.POST.get("ele_id")
    element_obj = element.objects.get(pk=ele_id)
    return render_to_response("element_msg.html", {"element_obj": element_obj})


def element_list_ajax(request):
    cur_pro_name = request.POST.get("current_pro_name")
    pro_id = Project.objects.get(name=cur_pro_name).id
    tag = request.POST.get("tag")
    sec_id = request.POST.get("sec_id")
    sec_name = request.POST.get("sec_name")
    sec_url = request.POST.get("sec_url")
    sec_val = request.POST.get("sec_val")
    ele_id = request.POST.get("ele_id")
    if tag == u"查询":
        print u"开始查询元素列表功能"
        if sec_id:
            ele_list = element.objects.filter(project_id=pro_id, pk=sec_id)
        else:
            ele_list = element.objects.filter(project_id=pro_id, name__contains=sec_name, page_url__contains=sec_url,
                                              values__contains=sec_val)

        return render_to_response("element_list_ajax.html", {"ele_list": ele_list})

    else:
        # if(ele_id):
        #     # 根据不同的项目获取该项目下所有的元素列表
        #     ele_list = element.objects.filter(project_id=pro_id)
        #     return render_to_response("element_list_ajax.html", {"ele_list": ele_list,"ele_id":ele_id})
        # else:
            # 根据不同的项目获取该项目下所有的元素列表
            ele_list = element.objects.filter(project_id=pro_id)
            return render_to_response("element_list_ajax.html", {"ele_list": ele_list ,"ele_id":ele_id })


@login_required
def case_process(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == u"页面跳转":
            pro_name = request.POST.get("pro_name")
            pro_obj = Project.objects.get(name=pro_name)
            case_list = pro_obj.case_set.filter(status="有效")
            element_list = pro_obj.element_set.all()
            fun = Method.objects.all()
            fun_list = Action.objects.all()
            return render_to_response("case_process.html", {"current_pro_name": pro_name,
                                                            "element_list": element_list,
                                                            "fun": fun, "case_list": case_list, "fun_list": fun_list})


        if action==u"复制用例":
            # 获取用例ID
            case_id = request.POST.get("case_id")

            # 获取该用例的所有字段数据
            copycase_obj = Case.objects.get(id=case_id)
            case_detail = copycase_obj.case_process_set.all()

            pro_obj = Project.objects.get(id=Case.objects.get(id=case_id).project_id)
            pro_name = pro_obj.name
            case_list = pro_obj.case_set.filter(status="有效")
            element_list = pro_obj.element_set.all()
            fun = Method.objects.all()
            fun_list = Action.objects.all()

            return render_to_response("case_process.html", {"current_pro_name": pro_name,
                                                            "element_list": element_list,
                                                            "fun": fun, "case_list": case_list, "copycase_obj": copycase_obj,
                                                            "case_detail": case_detail, "fun_list": fun_list})


        if action==u"刷新列表":
            case_id = request.POST.get("case_id")
            case_obj = Case.objects.get(id=case_id)
            project_id=case_obj.project_id
            pro_name=Project.objects.get(id=project_id).name
            case_list = Case.objects.all()
            return render_to_response("case_list.html", {"pro_name": pro_name, "case_list": case_list})

        if action == u"保存用例":
            """保存新增的用例"""
            current_name = request.POST.get("current_name")
            case_name = request.POST.get("casename")
            case_nature = request.POST.get("nature")
            browser = request.POST.get("browser")
            status = request.POST.get("status")
            features = request.POST.get("features")
            desc = request.POST.getlist("desc")
            action = request.POST.getlist("fun")
            value = request.POST.getlist("value")
            ele_id = request.POST.getlist("ele_id")



            # 写入用例
            try:
                Project.objects.get(name=current_name).case_set.create(name=case_name, browser=browser, category="测试用例",
                                                                       features=features,
                                                                       case_nature=case_nature, status=status)
            except:
                return HttpResponse("名称重复")



            for i in range(len(action)):
                if ele_id[i]:
                    ele_name = element.objects.get(pk=ele_id[i]).name
                    Case.objects.get(name=case_name).case_process_set.create(desc=desc[i], action=action[i],
                                                                             value=value[i],
                                                                             ele_id=ele_id[i], ele_name=ele_name)
                else:
                    Case.objects.get(name=case_name).case_process_set.create(desc=desc[i], action=action[i],
                                                                             value=value[i], ele_id=ele_id[i],
                                                                             ele_name="元素为空")
            # 获取当前用户名
            username=request.POST.get("username")
            # 获取新增用例的id
            case_id=Case.objects.get(name=case_name).id

            # 添加操作记录--创建用例
            try:
                Case.objects.get(id=case_id).caseaction_set.create(actor=username,action="create")
            except Exception,e:
                print str(e)

            return HttpResponse("保存成功")

        if action == u"添加元素":
            pro_name = request.POST.get("pro_name")
            ele_name = request.POST.get("name")
            ele_fun = request.POST.get("function")
            ele_value = request.POST.get("value")
            ele_desc = request.POST.get("desc")
            ele_url = request.POST.get("page_url")
            Project.objects.get(name=pro_name).element_set.create(name=ele_name, fun=ele_fun, values=ele_value,
                                                                  desc=ele_desc, page_url=ele_url)
            return HttpResponse("添加元素成功")

        if action == u"修改元素":
            pro_name = request.POST.get("pro_name")
            ele_id = request.POST.get("ele_id")
            ele_name = request.POST.get("name")
            ele_fun = request.POST.get("function")
            ele_value = request.POST.get("value")
            ele_desc = request.POST.get("desc")
            ele_url = request.POST.get("page_url")

            element_obj = Project.objects.get(name=pro_name).element_set.get(pk=ele_id)

            element_obj.name = ele_name
            element_obj.fun = ele_fun
            element_obj.values = ele_value
            element_obj.desc = ele_desc
            element_obj.page_url = ele_url
            element_obj.save()
            return HttpResponse("修改成功")

        if action == u"维护用例":
            """从用例列表点击维护用例,载入新的页面"""
            case_id = request.POST.get("case_id")

            case_obj = Case.objects.get(id=case_id)

            case_detail = case_obj.case_process_set.all()

            pro_obj = Project.objects.get(id=Case.objects.get(id=case_id).project_id)
            pro_name = pro_obj.name
            case_list = pro_obj.case_set.filter(status="有效")
            element_list = pro_obj.element_set.all()
            fun = Method.objects.all()
            fun_list = Action.objects.all()

            return render_to_response("case_process.html", {"current_pro_name": pro_name,
                                                            "element_list": element_list,
                                                            "fun": fun, "case_list": case_list, "case_obj": case_obj,
                                                            "case_detail": case_detail, "fun_list": fun_list})

        if action == u"修改用例":
            """保存修改的用例"""
            case_name = request.POST.get("casename")
            case_nature = request.POST.get("nature")
            browser = request.POST.get("browser")
            status = request.POST.get("status")
            features = request.POST.get("features")
            desc = request.POST.getlist("desc")
            action = request.POST.getlist("fun")
            value = request.POST.getlist("value")
            ele_id = request.POST.getlist("ele_id")
            case_id = request.POST.get("process_id")
            username=request.POST.get("username")
            obj=Case.objects.get(id=case_id)

            try:
                # 更新用例基本信息
                Case.objects.filter(pk=case_id).update(name=case_name, case_nature=case_nature, browser=browser,
                                                       status=status, features=features)
            except:
                return HttpResponse('名称重复')

            # 修改用例的name和case_nature以后要在 business_stp 中也做修改
            Business_stp.objects.filter(case_id=case_id).update(name=case_name, case_nature=case_nature)
            # 修改用例的name和case_nature以后要在 execution_detail 中也做修改
            Execution_detail.objects.filter(case_id=case_id).update(name=case_name, case_nature=case_nature)

            # 用例操作历史
            try:
                if(obj.name != case_name):
                    Case.objects.get(id=case_id).caseaction_set.create(actor=username,action="edit",edit_field="name",old_field_value=obj.name,new_field_value=case_name)
                if(obj.case_nature != case_nature):
                    Case.objects.get(id=case_id).caseaction_set.create(actor=username,action="edit",edit_field="case_nature",old_field_value=obj.case_nature,new_field_value=case_nature)
                if(obj.browser != browser):
                    Case.objects.get(id=case_id).caseaction_set.create(actor=username,action="edit",edit_field="browser",old_field_value=obj.browser,new_field_value=browser)
                if(obj.status != status):
                    Case.objects.get(id=case_id).caseaction_set.create(actor=username,action="edit",edit_field="status",old_field_value=obj.status,new_field_value=status)
                if(obj.features != features):
                    Case.objects.get(id=case_id).caseaction_set.create(actor=username,action="edit",edit_field="name",old_field_value=obj.features,new_field_value=features)
            except Exception,e:
                print str(e)

            case_obj = Case.objects.get(pk=case_id)
            case_process_obj = Case.objects.get(pk=case_id).case_process_set.all()

            # 获取post过来的步骤id


            print "按照POST过来的数据长度为%s开始循环写入数据" % len(action)
            try:
                for i in range(len(action)):
                    try:
                        ele_name = element.objects.get(pk=ele_id[i]).name
                    except:
                        ele_name = u"添加元素"
                    try:
                        # 修改用例步骤
                        old_e=Case.objects.get(pk=case_id).case_process_set.get(pk=case_process_obj[i].id)

                        case_process_obj.filter(pk=case_process_obj[i].id).update(desc=desc[i], action=action[i],
                                                                                  value=value[i], ele_id=ele_id[i],
                                                                                  ele_name=ele_name)
                        try:
                            if(old_e.desc != desc[i]):
                                Case.objects.get(id=case_id).caseaction_set.create(actor=username,action="editstep",edit_field="desc",old_field_value=old_e.desc,new_field_value=desc[i],step_desc=desc[i])
                            if(old_e.action != action[i]):
                                Case.objects.get(id=case_id).caseaction_set.create(actor=username,action="editstep",edit_field="action",old_field_value=old_e.action,new_field_value=action[i],step_desc=desc[i])
                            if(old_e.value != value[i]):
                                Case.objects.get(id=case_id).caseaction_set.create(actor=username,action="editstep",edit_field="value",old_field_value=old_e.value,new_field_value=value[i],step_desc=desc[i])
                            if(old_e.ele_name != ele_name):
                                Case.objects.get(id=case_id).caseaction_set.create(actor=username,action="editstep",edit_field="ele_name",old_field_value=old_e.ele_name,new_field_value=ele_name,step_desc=desc[i])
                        except Exception,e:
                            print str(e)

                    except:
                        # 增加用例步骤
                        case_obj.case_process_set.create(desc=desc[i], action=action[i], value=value[i],
                                                         ele_id=ele_id[i],
                                                         ele_name=ele_name)

                        Case.objects.get(id=case_id).caseaction_set.create(actor=username,action="addstep",step_desc=desc[i],step_action=action[i],
                                                                           step_value=value[i],step_e_name=ele_name)
                # 删除用例步骤
                if len(action) < case_process_obj.count():
                    print "POST数据小于数据库长度，开始删除数据库中多余的数据"
                    del_obj = case_process_obj[len(action):case_process_obj.count()]
                    for i in del_obj:
                        print "开始删除步骤:%s" % i.desc
                        i.delete()
                        Case.objects.get(id=case_id).caseaction_set.create(actor=username,action="delstep",step_desc=i.desc)
                return HttpResponse("修改成功")
            except Exception,e:
                print str(e)
                return HttpResponse("用例过程修改失败")

    if request.method == "GET":
        # ---- GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变 -----
        function_object = get_project_name(request)
        project_name = function_object[0]
        is_superuser = function_object[1]
        first_name = function_object[2]

        pro_name = request.GET.get("pro_name").strip()
        case_list = Project.objects.get(name=pro_name).case_set.all()
        element_list = element.objects.all()
        fun = Method.objects.all()

        return render_to_response("case_process.html", {"project_name": project_name, "is_superuser": is_superuser,
                                                        "first_name": first_name,
                                                        "current_pro_name": pro_name,
                                                        "element_list": element_list,
                                                        "fun": fun, "case_list": case_list})


@login_required
def interface_caselist(request):
    if request.method == 'POST':
        btn_name = request.POST.get("btn_name")
        action = request.POST.get("action")
        if action == u"页面跳转":
            # -----当前项目名称----------
            pro_name = request.POST.get("redirect").strip()
            # ------获取关联项目id--------
            project_id = Project.objects.get(name=pro_name).id
            # 通过关联项目id获取所有的用例列表
            case_list = InCaseList.objects.filter(project_id=project_id)
            return render_to_response("modify_inter_case_list.html",
                                      {"case_list": case_list, "current_project": pro_name})

        if action == u"删除用例":
            print "删除用例"
            get_id = request.POST.get("get_id")
            try:
                for i in get_id:
                    InCaseDetail.objects.filter(case_id=get_id).delete()
                    Diff.objects.filter(case_id=get_id).delete()
                    InCaseList.objects.filter(id=get_id).delete()
                return HttpResponse("删除用例成功")
            except:
                return HttpResponse("删除用例失败")

        elif action == u"测试调试":
            try:
                in_id = request.POST.get("in_id")  # 点击测试调试，返回用例的ID
                print u"执行的用例是： %s" % in_id

                # 取名称
                get_name = InCaseList.objects.get(pk=in_id)

                case_name = str(get_name.caseName)

                # 取IP
                regip = get_client_ip(request)
                runTest(regip, 'interface', in_id, case_name)

                return HttpResponse("请确认开启调试客户端")
            except:
                return HttpResponse("调试错误")


@login_required
def interfaceParamManager(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == u"删除模板":
            tmp_id = request.POST.get("tmp_id")
            try:
                ProTemp.objects.filter(id=tmp_id).delete()
                TempDetail.objects.filter(temp_id=tmp_id).delete()
                return HttpResponse("删除成功")
            except:
                return HttpResponse("删除失败")

        if action == u"页面跳转":
             # -----当前项目名称----------
            pro_name = request.POST.get("redirect").strip()
            # print ","*30,pro_name

            # ------获取关联项目id和测试类型--------
            project_id = Project.objects.get(name=pro_name).id
            project_type = Project.objects.get(name=pro_name).test_type

            # 通过关联项目id获取所有的用例列表
            protemp_list = ProTemp.objects.filter(proName_id=project_id)
            return render_to_response("interfaceParamManager.html",
                                      {"protemp_list": protemp_list, "current_project": pro_name,"project_type":project_type})




def data_base_manager(request):
    """环境管理"""
    # ---GET 请求处理,获取母模板上的变量以获取到相应的值，名称不可变-----
    function_object = get_project_name(request)
    project_name = function_object[0]
    is_superuser = function_object[1]
    first_name = function_object[2]
    if request.method == "POST":
        print str(request.POST)
        action = request.POST.get("action")

        if action == u"页面跳转":
             # -----当前项目名称----------
            pro_name = request.POST.get("redirect").strip()
            print pro_name
            # ------获取关联项目id--------
            project_id = Project.objects.get(name=pro_name).id
            print project_id
            # 通过关联项目id获取项目接口环境配置信息
            prosetting = ProSetting.objects.filter(proName_id=project_id)
            proInfo = []
            for j in prosetting:
                proId = j.id
                envName = j.envName
                address = j.address
                port = j.port
                connectType = j.connectType
                connectData = j.connectData
                uName = j.userName
                pWord = j.passWord
                iType = j.interfaceType
                is_used = str(j.is_used)
                proSetList = {'proName': pro_name,
                            'proId': proId,
                            'address': address,
                            'port': port,
                            'connectType': connectType,
                            'connectData': connectData,
                            'uName': uName,
                            'pWord': pWord,
                            'iType': iType,
                            'is_used': is_used,
                            'envName': envName
                            }
            print proSetList
            proInfo.append(proSetList)

            return render_to_response("DataBaseManager.html",
                                      {"proInfo": proInfo, "current_project": pro_name})

        elif request.POST.get('subBtn') == 'addNewEnv':
            print u"参数保存"
            proName = request.POST.get('proName')
            address = request.POST.get('address')
            port = request.POST.get('port')
            connectType = request.POST.get('connectType')
            connectData = request.POST.get('connectData')
            username = request.POST.get('username')
            password = request.POST.get('password')
            interFaceType = request.POST.get('interFaceType')
            chest = request.POST.get('radiobutton')
            if str(chest) == '1':
                is_used = 1
            else:
                is_used = 0
            envName = request.POST.get('envName')
            try:
                project_obj = Project.objects.get(name=proName)
                if is_used == 1:
                    project_obj.prosetting_set.update(is_used=0)
                project_obj.prosetting_set.create(
                    address=str(address),
                    port=str(port),
                    connectType=str(connectType),
                    connectData=str(connectData),
                    userName=str(username),
                    passWord=str(password),
                    interfaceType=str(interFaceType),
                    is_used=is_used,
                    envName=str(envName)
                )
                return HttpResponse("保存环境参数成功")
            except:
                return HttpResponse("保存环境参数失败")

        elif request.POST.get('subBtn') == '删除环境配置':
            print u"delete envSetting"
            pid = request.POST.get('pro_id')
            print pid, "is pid"
            po = ProSetting.objects.get(pk=str(pid))
            try:
                po.delete()
                return HttpResponse('删除环境参数成功')
            except:
                return HttpResponse('删除环境参数失败')

        elif request.POST.get('subBtn') == 'mdyEnv':
            pid = request.POST.get('pro_id1')
            proName = request.POST.get('proName')
            address = request.POST.get('address')
            port = request.POST.get('port')
            connectType = request.POST.get('connectType')
            connectData = request.POST.get('connectData')
            username = request.POST.get('username')
            password = request.POST.get('password')
            interFaceType = request.POST.get('interFaceType')
            chest = request.POST.get('radiobutton')
            if str(chest) == '1':
                is_used = 1
            else:
                is_used = 0
            envName = request.POST.get('envName')
            project_obj = Project.objects.get(name=proName)
            if is_used == 1:
                project_obj.prosetting_set.update(is_used=0)
            po = ProSetting.objects.get(pk=str(pid))
            proId = project_obj.id
            try:
                po.address = str(address)
                po.proName_id = str(proId)
                po.port = str(port)
                po.connectType = str(connectType)
                po.connectData = str(connectData)
                po.userName = str(username)
                po.passWord = str(password)
                po.interfaceType = str(interFaceType)
                po.is_used = is_used
                po.envName = str(envName)
                po.save()
                return HttpResponse('修改环境参数成功')
            except:
                return HttpResponse('修改环境参数失败')

    # if request.method == "GET":
    #     project = Project.objects.all()
    #     proInfo = []
    #     for i in project:
    #
    #         proName = i.name
    #         proSet = i.prosetting_set.all()
    #         for j in proSet:
    #             proId = j.id
    #             envName = j.envName
    #             address = j.address
    #             port = j.port
    #             connectType = j.connectType
    #             connectData = j.connectData
    #             uName = j.userName
    #             pWord = j.passWord
    #             iType = j.interfaceType
    #             is_used = str(j.is_used)
    #             proSetList = {'proName': proName,
    #                           'proId': proId,
    #                           'address': address,
    #                           'port': port,
    #                           'connectType': connectType,
    #                           'connectData': connectData,
    #                           'uName': uName,
    #                           'pWord': pWord,
    #                           'iType': iType,
    #                           'is_used': is_used,
    #                           'envName': envName
    #                           }
    #             proInfo.append(proSetList)


        # -----通过用例ID获取项目ID,并传到html中隐藏的button的value值----------
        # return render_to_response("DataBaseManager.html",
        #                           {"project_name": project_name, "is_superuser": is_superuser,
        #                            "first_name": first_name,
        #
        #                            })


def addNewEnvAjax(request):
    if request.method == "POST":
        mo = Project.objects.all()
        return render_to_response("add_new_env.html", {"mo": mo})


def envListAjax(request):
    if request.method == "POST":
        return render_to_response("env_list_ajax.html")


def search_ajax(request):
    if request.method == "POST":
        pid = request.POST.get('proName')
        po = Project.objects.get(name=pid)
        mo = po.messageobject_set.all()
        return render_to_response("search_ajax.html",
                                  {"mo": mo})


def add_new_messageObj_ajax(request):
    if request.method == "POST":
        return render_to_response("add_new_messageObj_ajax.html")


def add_new_diffObj_ajax(request):
    if request.method == "POST":
        return render_to_response("add_new_diffObj_ajax.html")


def chsTemp_ajax(request):
    if request.method == "POST":
        proName = request.POST.get('proName')
        print proName
        if proName:
            po = Project.objects.get(name=proName)
            mo = po.protemp_set.all()
        else:
            mo = ProTemp.objects.all()
        return render_to_response("chsTemp_ajax.html", {'mo': mo})


def mdy_Temp_ajax(request):
    if request.method == "POST":
        tid = request.POST.get('tempId')
        to = ProTemp.objects.get(id=str(tid))
        mo = to.tempdetail_set.all()
        return render_to_response("mdy_Temp_ajax.html", {'mo': mo})


def importTemp_ajax(request):
    if request.method == "POST":
        tid = request.POST.get('tempId')
        to = ProTemp.objects.get(id=str(tid))
        mo = to.tempdetail_set.all()
        return render_to_response("importTemp_ajax.html", {'mo': mo})


def serchTemp_ajax(request):
    if request.method == "POST":
        tid = request.POST.get('tempId')
        tname = request.POST.get('tempName')
        if request.POST.get('proName'):
            proName = request.POST.get('proName')
            pid = Project.objects.get(name=proName).id
            mo = ProTemp.objects.filter(proName_id=str(pid), tempName__contains=str(tname), id__contains=str(tid))
        else:
            mo = ProTemp.objects.filter(tempName__contains=str(tname), id__contains=str(tid))
        return render_to_response("chsTemp_ajax.html", {'mo': mo})


def add_template(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == u"新增json模版":
            pro_name = request.POST.get("pro_name")
            json_list = ProTemp.objects.filter(template_type="JSON")
            return render_to_response("template_manage.html",
                                      {"pro_name": pro_name, "temp_type": "JSON", "ac": "保存模板", "json_list": json_list})
        if action == u"新增jms模版":
            pro_name = request.POST.get("pro_name")
            jms_list = ProTemp.objects.filter(template_type="JMS")
            return render_to_response("template_manage.html",
                                      {"pro_name": pro_name, "temp_type": "JMS", "ac": "保存模板", "jms_list": jms_list})

        if action == u"保存模板":
            pro_id = request.POST.get("project_name")

            template_name = request.POST.get("template_name")
            get_list = request.POST.getlist("list")
            get_part = request.POST.getlist("part")
            get_objname = request.POST.getlist("objname")
            get_key = request.POST.getlist("key")
            get_type = request.POST.getlist("type")
            template_type = request.POST.get("template_type")
            print pro_id
            boo_name = ProTemp.objects.filter(tempName=template_name)
            if boo_name:
                return HttpResponse("名称重复,请修改模版名称")
            else:
                try:
                    print u"开始创建模版对象"
                    temp_obj = Project.objects.get(name=pro_id).protemp_set.create(tempName=template_name,
                                                                                 createUser=request.user.first_name,
                                                                                 template_type=template_type)
                    print u"创建成功,模版对象是:", temp_obj

                    print u"开始创建模版详细内容."
                    for i in range(len(get_type)):
                        temp_obj.tempdetail_set.create(part=get_part[i],
                                                       objName=get_objname[i],
                                                       list=get_list[i],
                                                       key=get_key[i],
                                                       type=get_type[i])
                    return HttpResponse("保存成功")
                except Exception,e:
                    print str(e)
                    return HttpResponse("保存模版失败")

        if action == u"编辑模板":
            temp_id = request.POST.get("temp_id")
            get_type = request.POST.get("tmp_type")
            pro_name = request.POST.get("pro_name")

            if get_type == "JSON":
                temp_obj = ProTemp.objects.get(id=temp_id)
                temp_detail = temp_obj.tempdetail_set.all()
                json_list = ProTemp.objects.filter(template_type="JSON")
                return render_to_response("template_manage.html",
                                          {"temp_type": "编辑JSON", "temp_obj": temp_obj, "temp_detail": temp_detail,
                                           "pro_name": pro_name, "json_list": json_list, "ac": "修改模板",
                                           "temp_id": temp_id})
            if get_type == "JMS":
                temp_obj = ProTemp.objects.get(id=temp_id)
                temp_detail = temp_obj.tempdetail_set.all()
                jms_list = ProTemp.objects.filter(template_type="JMS")
                return render_to_response("template_manage.html",
                                          {"temp_type": "编辑JMS", "temp_obj": temp_obj, "temp_detail": temp_detail,
                                           "pro_name": pro_name, "jms_list": jms_list, "ac": "修改模板",
                                           "temp_id": temp_id})


        if action == u"修改模板":
            pro_id = request.POST.get("project_name")
            template_name = request.POST.get("template_name")
            temp_id = request.POST.get("temp_id")
            get_list = request.POST.getlist("list")
            get_part = request.POST.getlist("part")
            get_objname = request.POST.getlist("objname")
            get_key = request.POST.getlist("key")
            get_type = request.POST.getlist("type")
            try:
                ProTemp.objects.filter(id=temp_id).update(tempName=template_name,createUser=request.user.first_name)
            except:
                return HttpResponse("名称重复")
            try:
                protem_obj = ProTemp.objects.get(id=temp_id)
                detail_obj = protem_obj.tempdetail_set.all()
                for i in range(len(get_objname)):
                    try:
                        print "Begin update"
                        protem_obj.tempdetail_set.filter(id=detail_obj[i].id).update(objName=get_objname[i],part=get_part[i],list=get_list[i],key=get_key[i],type=get_type[i])
                    except:
                        print "Begin create"
                        protem_obj.tempdetail_set.create(objName=get_objname[i],part=get_part[i],list=get_list[i],key=get_key[i],type=get_type[i])

                if len(get_objname) < detail_obj.count():
                    del_obj = detail_obj[len(get_objname):detail_obj.count()]
                    for i in del_obj:
                        print "Begin delete",i.objName
                        i.delete()
                return HttpResponse("保存成功")
            except:
                return HttpResponse("修改失败")

        if action == u"复制接口模板":
            temp_id = request.POST.get("temp_id")
            get_type = request.POST.get("tmp_type")
            pro_name = request.POST.get("pro_name")

            if get_type == "JSON":
                temp_obj = ProTemp.objects.get(id=temp_id)
                temp_detail = temp_obj.tempdetail_set.all()
                json_list = ProTemp.objects.filter(template_type="JSON")
                return render_to_response("template_manage.html",
                                          {"temp_type": "JSON", "copy_type":"复制JSON", "copy_temp_obj": temp_obj, "temp_detail": temp_detail,
                                           "pro_name": pro_name, "json_list": json_list,"ac": "保存模板",
                                           "temp_id": temp_id})
            if get_type == "JMS":
                temp_obj = ProTemp.objects.get(id=temp_id)
                temp_detail = temp_obj.tempdetail_set.all()
                jms_list = ProTemp.objects.filter(template_type="JMS")
                return render_to_response("template_manage.html",
                                          {"temp_type": "JMS", "copy_type":"复制JMS" ,"copy_temp_obj": temp_obj, "temp_detail": temp_detail,
                                           "pro_name": pro_name, "jms_list": jms_list,"ac": "保存模板",
                                           "temp_id": temp_id})






def add_template_ajax(request):
    if request.method == "POST":
        tmp_type = request.POST.get("template_type")
        #add_head = request.POST.get("add_head")
        if tmp_type:
            print "新增JSON模板"
            tempplate_type = True
            return render_to_response("add_template_ajax.html", {"tempplate_type": tempplate_type})
        # if add_head:
        #     add_head = True
        #     return render_to_response("add_template_ajax.html", {"add_head": add_head})

        else:
            # 导入模板功能，编辑模板功能
            tem_id = request.POST.get("tmp_id")
            tempplate_type = ProTemp.objects.get(id=tem_id).template_type

            tr_list = ProTemp.objects.get(id=tem_id).tempdetail_set.all()
            return render_to_response("importtmp_ajax.html", {"tr_list": tr_list, "tempplate_type": tempplate_type})

    return render_to_response("add_template_ajax.html")


def add_inter_face(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == u"新增接口用例":
            current_name = request.POST.get("redirect")
            # 当前项目下的用例列表
            case_list = InCaseList.objects.filter(project_id=Project.objects.get(name=current_name).id)
            # 当前项目下的模板列表
            template_list = Project.objects.get(name=current_name).protemp_set.all()
            return render_to_response("add_inter_face.html",
                                      {"current_name": current_name, "template_list": template_list,
                                       "case_list": case_list})

        if action == u"维护接口用例":
            get_id = request.POST.get("get_id")
            # 维护用例--取项目值可导入的模板列表
            current_name = Project.objects.get(id=InCaseList.objects.get(id=get_id).project_id).name
            template_list = Project.objects.get(name=current_name).protemp_set.all()

            # 用例对象
            case_obj = InCaseList.objects.get(id=get_id)
            # 通过用例中的模板ID查询模板详细
            template_obj = ProTemp.objects.get(id=case_obj.tempId).tempdetail_set.all()
            # 查询报文
            content_obj = InCaseList.objects.get(id=get_id).incasedetail_set.all()
            # 查询断言
            diff_obj = InCaseList.objects.get(id=get_id).diff_set.all()

            conten_dict = []
            # 利用字典把模板和报文 模板和断言结合
            for i in template_obj:
                if i.type == u"响应报文":
                    pass
                else:
                    conten_dict.append(i.__dict__)

            for i in range(len(conten_dict)):
                """使用Try的方式防止模板增加字段导致修改用例失败"""
                try:
                    conten_dict[i].update(content_obj[i].__dict__)
                except:
                    pass
            case_list = InCaseList.objects.filter(project_id=Project.objects.get(name=current_name).id)


            return render_to_response("add_inter_face.html",
                                      {"current_name": current_name, "template_list": template_list,
                                       "diff_obj": diff_obj,
                                       "conten_dict": conten_dict, "get_id": get_id,
                                       "case_obj": case_obj, "case_list": case_list})

        pro_name = request.POST.get("current_name")
        # 报文内容
        interface_name = request.POST.get("interface_name")
        template_id = request.POST.get("template_id")
        user_name = request.user
        content_objName = request.POST.getlist("content_objName")
        val = request.POST.getlist("val")
        # 断言内容
        assert_objName = request.POST.getlist("assert_objName")
        field_name = request.POST.getlist("field_name")
        assert_method = request.POST.getlist("assert_method")
        expected_val = request.POST.getlist("expected_val")
        sql_str = request.POST.getlist("sql_str")
        get_id = request.POST.get("get_id")


        if action == u"修改用例":
            print "修改用例", "-" * 80
            status = request.POST.get("status")
            nature = request.POST.get("nature")
            case_obj = InCaseList.objects.get(id=get_id)
            try:
                print "更新用例的名称,但不更新表中的模板ID。用例ID:%s,模板名称为:%s" % (get_id, interface_name)
                InCaseList.objects.filter(id=get_id).update(caseName=interface_name, modifyDate=get_time(),status=status,nature=nature)

                # 将操作记录写入表
                if(case_obj.caseName != interface_name):
                     InCaseList.objects.get(id=get_id).incaseaction_set.create(actor=user_name,action="edit",edit_field="caseName",
                                                                            old_field_value=case_obj.caseName,new_field_value=interface_name)
                if(case_obj.status != status):
                     InCaseList.objects.get(id=get_id).incaseaction_set.create(actor=user_name,action="edit",edit_field="status",
                                                                            old_field_value=case_obj.status,new_field_value=status)
                if(case_obj.nature != nature):
                     InCaseList.objects.get(id=get_id).incaseaction_set.create(actor=user_name,action="edit",edit_field="nature",
                                                                            old_field_value=case_obj.nature,new_field_value=nature)
            except:
                return HttpResponse("名称重复")

            # 修改用例的name和case_nature以后要在 business_stp 中也做修改
            Business_stp.objects.filter(case_id=get_id).update(name=interface_name, case_nature=nature)
            # 修改用例的name和case_nature以后要在 execution_detail 中也做修改
            Execution_detail.objects.filter(case_id=get_id).update(name=interface_name, case_nature=nature)

            try:
                caseDetail_obj = InCaseList.objects.get(id=get_id).incasedetail_set.all()
                diff_obj = InCaseList.objects.get(id=get_id).diff_set.all()

                print "开始更新报文表,用例ID:%s。用例对象:%s" % (get_id, caseDetail_obj)

                print "开始按POST数据的长度循环更新报文表,POST数据长度为", len(content_objName)
                for i in range(len(content_objName)):
                    try:
                        obj=InCaseDetail.objects.get(id=caseDetail_obj[i].id)
                        print "用例详细ID为:%s。objId:%s value:%s" % (caseDetail_obj[i].id, content_objName[i], val[i])


                        InCaseDetail.objects.filter(id=caseDetail_obj[i].id).update(objId=content_objName[i],
                                                                                    value=val[i])
                        print "-"*100
                        print "开始将修改记录写入表中"
                        if(obj.value != val[i]):
                            InCaseList.objects.get(id=get_id).incaseaction_set.create(actor=user_name,action="edit",edit_field="value",
                                                                                      old_field_value=obj.value,new_field_value=val[i])
                    except:
                        print "POST长度大于数据库长度,开始创建"
                        InCaseDetail.objects.filter(id=caseDetail_obj[i].id).update(objId=content_objName[i],
                                                                                    value=val[i])

                for i in range(len(assert_objName)):
                    try:
                        print "开始更新断言表"
                        print "-" * 100
                        di_obj=Diff.objects.get(id=diff_obj[i].id)
                        Diff.objects.filter(id=diff_obj[i].id).update(objId=assert_objName[i],
                                                                      diffType=assert_method[i], value=expected_val[i],
                                                                      ex=sql_str[i], field_name=field_name[i])
                        print "将断言修改记录写入表中"
                        print "-" * 100
                        if(di_obj.diffType != assert_method[i]):
                             InCaseList.objects.get(id=get_id).incaseaction_set.create(actor=user_name,action="edit",edit_field="difftype",
                                                                                      old_field_value=diff_obj.diffType,new_field_value=assert_method[i])
                        if(di_obj.value != expected_val[i]):
                         InCaseList.objects.get(id=get_id).incaseaction_set.create(actor=user_name,action="edit",edit_field="difftype",
                                                                                  old_field_value=diff_obj.diffType,new_field_value=assert_method[i])
                        if(di_obj.ex != sql_str[i]):
                             InCaseList.objects.get(id=get_id).incaseaction_set.create(actor=user_name,action="edit",edit_field="difftype",
                                                                                      old_field_value=diff_obj.diffType,new_field_value=assert_method[i])

                    except:
                        print "POST长度大于数据库长度,开始创建aaa"
                        print user_name
                        InCaseList.objects.get(caseName=interface_name).diff_set.create(objId=assert_objName[i],
                                                                                        diffType=assert_method[i],
                                                                                        value=expected_val[i],
                                                                                        field_name=field_name[i],
                                                                                        ex=sql_str[i])


                        InCaseList.objects.get(id=get_id).incaseaction_set.create(actor=user_name,action="adddiff",add_objId=assert_objName[i],add_diffType=assert_method[i],
                                                add_value=expected_val[i],add_fieldname=field_name[i],add_ex=sql_str[i])

                post_length = len(assert_objName)
                dba_len = InCaseList.objects.get(id=get_id).diff_set.all().count()

                try:
                    if post_length < dba_len:
                        print "POST数据长度小于数据库中长度"
                        del_obj = InCaseList.objects.get(id=get_id).diff_set.all()[post_length:dba_len]

                        print "获取到要删除的数据库对象:%s,开始循环删除多余的数据" % del_obj
                        for i in del_obj:
                            print i.objId
                            InCaseList.objects.get(id=get_id).incaseaction_set.create(actor=user_name,action="deletediff",add_objId=i.objId,add_diffType=i.diffType,
                                                add_value=i.value,add_fieldname=i.field_name,add_ex=i.ex)
                            i.delete()

                        print "删除成功"

                except:
                    return HttpResponse("删除多余的失败")

                return HttpResponse("保存成功")
            except:
                return HttpResponse("修改失败")


        if action == u"保存用例":
            print "新增接口用例", "-" * 80
            status = request.POST.get("status")
            nature = request.POST.get("nature")
            bool_name = InCaseList.objects.filter(caseName=interface_name)

            print "当前登录用户：",user_name
            print "查看数据库中是否有重名,返回类型为:%s" % (bool(bool_name))
            if bool_name:
                return HttpResponse("名称重复")
            else:
                try:
                    print "写入用例表,模板ID为:%s,用例名称为:%s" % (template_id, interface_name)
                    Project.objects.get(name=pro_name).incaselist_set.create(tempId=template_id,creator=user_name,
                                                                             caseName=interface_name,status=status,nature=nature,category="接口用例")

                    print "开始写入报文表"
                    for i in range(len(content_objName)):
                        InCaseList.objects.get(caseName=interface_name).incasedetail_set.create(
                            objId=content_objName[i], value=val[i])

                    print "开始写入断言表"

                    for i in range(len(assert_objName)):
                        InCaseList.objects.get(caseName=interface_name).diff_set.create(objId=assert_objName[i],
                                                                                        field_name=field_name[i],
                                                                                        diffType=assert_method[i],
                                                                                        value=expected_val[i],
                                                                                        ex=sql_str[i])

                    # 将创建-操作写入操作记录表中
                    incase_id=InCaseList.objects.get(caseName=interface_name).id
                    InCaseAction.objects.create(actor=user_name,action="create",inCaseList_id=incase_id)

                    return HttpResponse("保存成功")

                except Exception,e:
                    print str(e)
                    transaction.rollback()
                    return HttpResponse("保存失败")
                else:
                    transaction.commit()

        if action == u"查询用例":
            pro_id = request.POST.get("pro_id")
            case_list = Project.objects.get(id=pro_id).incaselist_set.filter(status="有效")

            return render_to_response("apibus_querycase.html",{"case_list":case_list})

        if action == u"添加用例":
            id_list = request.POST.getlist("id_list[]")
            case_list = []
            for i in id_list:
                tmp = InCaseList.objects.get(id=i)
                case_list.append(tmp)


            return render_to_response("add_api_ajax.html", {"case_list": case_list})

        if action ==u"复制用例":
            try:
                # 获取接口用例的id
                incase_id = request.POST.get("incase_id")
                current_name = request.POST.get("pro_name")
                template_list = Project.objects.get(name=current_name).protemp_set.all()

                # 用例对象
                copycase_obj = InCaseList.objects.get(id=incase_id)
                # 通过用例中的模板ID查询模板详细
                template_obj = ProTemp.objects.get(id=copycase_obj.tempId).tempdetail_set.all()
                # 查询报文
                content_obj = InCaseList.objects.get(id=incase_id).incasedetail_set.all()
                # 查询断言
                diff_obj = InCaseList.objects.get(id=incase_id).diff_set.all()


                conten_dict = []
                # 利用字典把模板和报文 模板和断言结合
                for i in template_obj:
                    if i.type == u"响应报文":
                        pass
                    else:
                        conten_dict.append(i.__dict__)

                for i in range(len(conten_dict)):
                    """使用Try的方式防止模板增加字段导致修改用例失败"""
                    try:
                        conten_dict[i].update(content_obj[i].__dict__)
                    except:
                        pass

                case_list = InCaseList.objects.filter(project_id=Project.objects.get(name=current_name).id)


                return render_to_response("add_inter_face.html",
                                          {"current_name": current_name, "template_list": template_list,
                                           "diff_obj": diff_obj,
                                           "conten_dict": conten_dict, "get_id": incase_id,
                                           "copycase_obj": copycase_obj, "case_list": case_list})
            except Exception,e:
                print str(e)


        if action== u"查看接口用例详细信息":
            try:
                # 获取接口用例的id
                incase_id = request.POST.get("incase_id")
                pro_name = request.POST.get("pro_name")

                # 用例对象
                case_obj = InCaseList.objects.get(id=incase_id)
                # 通过用例中的模板ID查询模板详细
                template_obj = ProTemp.objects.get(id=case_obj.tempId).tempdetail_set.all()
                # 查询报文
                content_obj = InCaseList.objects.get(id=incase_id).incasedetail_set.all()
                # 查询断言
                diff_obj = InCaseList.objects.get(id=incase_id).diff_set.all()

                conten_dict = []
                # 利用字典把模板和报文 模板和断言结合
                for i in template_obj:
                    if i.type == u"响应报文":
                        pass
                    else:
                        conten_dict.append(i.__dict__)

                for i in range(len(conten_dict)):
                    """使用Try的方式防止模板增加字段导致修改用例失败"""
                    try:
                        conten_dict[i].update(content_obj[i].__dict__)
                    except:
                        pass
                case_list = InCaseList.objects.filter(project_id=Project.objects.get(name=pro_name).id)

                # 获取历史记录
                history_list=InCaseAction.objects.filter(inCaseList_id=incase_id).order_by('-actiondate')

                return render_to_response("show_incase_detail.html",{"pro_name": pro_name,
                                           "diff_obj": diff_obj,"history_list":history_list,
                                           "conten_dict": conten_dict, "get_id": get_id,
                                           "case_obj": case_obj, "case_list": case_list})
            except Exception,e:
                print str(e)

def imp_interface_ajax(request):
    get_id = request.POST.get("get_id")
    # 维护用例--取项目值可导入的模板列表
    current_name = Project.objects.get(id=InCaseList.objects.get(id=get_id).project_id).name
    template_list = Project.objects.get(name=current_name).protemp_set.all()

    # 用例对象
    case_obj = InCaseList.objects.get(id=get_id)
    # 通过用例中的模板ID查询模板详细
    template_obj = ProTemp.objects.get(id=case_obj.tempId).tempdetail_set.all()
    # 查询报文
    content_obj = InCaseList.objects.get(id=get_id).incasedetail_set.all()
    # 查询断言
    diff_obj = InCaseList.objects.get(id=get_id).diff_set.all()

    conten_dict = []
    # 利用字典把模板和报文 模板和断言结合
    for i in template_obj:
        if i.type == "响应报文":
            pass
        else:
            conten_dict.append(i.__dict__)

    for i in range(len(conten_dict)):
        """使用Try的方式防止模板增加字段导致修改用例失败"""
        try:
            conten_dict[i].update(content_obj[i].__dict__)
        except:
            pass

    return render_to_response("imp_interface_ajax.html", {"diff_obj": diff_obj, "conten_dict": conten_dict})


def add_interface_ajax(request):
    if request.method == "POST":
        tmp_id = request.POST.get("tmp_id")
        print "模板ID为:", tmp_id
        tempdetail = ProTemp.objects.get(id=tmp_id).tempdetail_set.all()
        # 报文内容
        temp_conten = []
        # 报文断言
        temp_assert = []
        for i in tempdetail:
            if i.type == u"响应报文":
                temp_assert.append(i)
            else:
                temp_conten.append(i)

        return render_to_response("add_interface_ajax.html", {"temp_conten": temp_conten, "temp_assert": temp_assert})

    return render_to_response("add_interface_ajax.html")


def api_list(request):
    """接口业务流列表"""
    if request.method == "POST":
        action = request.POST.get("action")

        if action == u"页面跳转":
            pro_name = request.POST.get("redirect")
            api_list = Project.objects.get(name=pro_name).api_business_set.all()
            return render_to_response("api_list.html", {"pro_name": pro_name, "api_list": api_list},
                                      context_instance=RequestContext(request))

        if action == u"删除业务流":
            inbu_id = request.POST.get("inbu_id")

            api_detail_sql = "DELETE  from webapp_api_detail where api_id = %s" % inbu_id
            api_business_sql = "DELETE from webapp_api_business where id =%s" % inbu_id

            sql_commend(api_detail_sql)
            sql_commend(api_business_sql)

            print "删除业务流成功"

        if action == u"调试用例":
            api_id = request.POST.get("api_id")  # 业务流ID
            api_name = sql_commend("select name from webapp_api_business where id = %s" % api_id)[0].get(
                "name")  # 业务流名称

            try:
                # 取IP
                regip = get_client_ip(request)
                runTest(regip, 'api_list', api_id, api_name)
                return HttpResponse("开始运行调试")
            except:
                return HttpResponse("发送调试信息失败")

    api_list = Project.objects.get(name="TPP").api_business_set.all()

    return render_to_response("api_list.html", {"api_list": api_list})


def api_business(request):
    """新增接口业务流"""
    if request.method == "POST":
        action = request.POST.get("action")

        if action == u"页面跳转":
            pro_list = Project.objects.filter(pro_user__contains=request.user)
            try:
                """点击首页,POST项目名称.ajax回传显示在首页"""
                redirect_page = request.POST.get("redirect")
                if redirect_page:
                    return render_to_response("api_business.html", {"pro_name": redirect_page, "pro_list": pro_list})
            except:
                print "页面跳转失败"

        if action == u"保存用例":
            """新增业务流用例"""
            pro_name = request.POST.get("pro_name")
            name = request.POST.get("ywlname")
            case_id = request.POST.getlist("case_id")
            case_name = request.POST.getlist("name")

            bool_name = Project.objects.get(name=pro_name).api_business_set.filter(name=name)

            if bool_name:
                return HttpResponse("名称重复")
            else:
                try:
                    # 写入业务流表返回对象
                    api_obj = Project.objects.get(name=pro_name).api_business_set.create(name=name)

                    for c_id, c_name in zip(case_id, case_name):
                        # 写入详细表返回对象
                        api_detail_obj = api_obj.api_detail_set.create(name=c_name)

                        # update另外一个外键
                        api_detail_obj.case_id = c_id
                        api_detail_obj.save()

                    return HttpResponse("保存成功")
                except:
                    return HttpResponse("保存失败")

        if action == u"修改用例":
            name = request.POST.get("ywlname")
            pro_name = request.POST.get("pro_name")
            case_name = request.POST.getlist("name")
            case_id = request.POST.getlist("case_id")
            bus_id = request.POST.get("bus_id")

            pro_obj = Project.objects.get(name=pro_name)
            try:
                pro_obj.api_business_set.filter(id=bus_id).update(name=name)
            except IntegrityError, e:
                print e
                return HttpResponse("名称重复")

            id_obj = pro_obj.api_business_set.get(id=bus_id).api_detail_set.all()
            for i in range(len(case_id)):
                try:
                    pro_obj.api_business_set.get(id=bus_id).api_detail_set.filter(id=id_obj[i].id).update(
                        name=case_name[i], case_id=case_id[i])
                except:
                    pro_obj.api_business_set.get(id=bus_id).api_detail_set.create(name=case_name[i], case_id=case_id[i])

            sql_count = pro_obj.api_business_set.get(id=bus_id).api_detail_set.count()
            if len(case_id) < sql_count:
                print "POST数据长度小于数据库长度,开始删除多余的数据库数据"
                del_obj = pro_obj.api_business_set.get(id=bus_id).api_detail_set.all()[len(case_id):sql_count]
                for i in del_obj:
                    i.delete()

            return HttpResponse("保存成功")

        if action == u"维护用例":
            """业务流列表中点维护用例跳转到该页面,加载业务流中的数据"""
            case_id = request.POST.get("id")
            pro_name = InCaseList.objects.get(id=case_id).project.name

            business_obj = sql_commend("select * from webapp_api_business where id=%s" % case_id)[0]

            print business_obj

            detail_obj = sql_commend("select case_id from webapp_api_detail where api_id = %s" % case_id)

            pro_list = Project.objects.filter(pro_user__contains=request.user)
            case_obj = []
            for i in detail_obj:
                case_tmp = sql_commend("select * from webapp_incaselist where id = %s" % i.get("case_id"))[0]
                case_obj.append(case_tmp)

            return render_to_response("api_business.html",
                                      {"business_obj": business_obj, "case_obj": case_obj, "pro_name": pro_name,
                                       "pro_list": pro_list})

    if request.method == "GET":
        return render_to_response("api_business.html")





def api_perform(request):
    """接口测试执行列表"""
    if request.method == "POST":
        action = request.POST.get("action")
        if action == u"跳转页面":
            per_list = Ap.objects.all
            return render_to_response("api_perform.html", {"per_list": per_list})
        if action == u"删除执行": #维护接口执行->删除执行

            id_list = request.POST.getlist("id_list[]")
            try:
                print "开始删除执行用例"
                for i in id_list:
                    del_perform = Ap.objects.get(id=i)
                    del_perform_detail = del_perform.ap_detail_set.all()
                    del_perform_detail.delete()
                    del_perform.delete()
                return HttpResponse("删除成功")
            except:
                return HttpResponse("删除失败")

        if action == u"运行执行": #维护接口执行->运行执行
            per_id = request.POST.get("run_id")
            per_name = Ap.objects.get(id=per_id).name
            try:
                regip = get_client_ip(request)
                runTest(regip, 'api_perform', per_id, per_name)
                return HttpResponse("开始运行调试")
            except:
                return HttpResponse("发送调试信息失败")

    return render_to_response("api_perform.html")


def ad_perform(request):
    """新增/编辑接口执行用例"""
    if request.method == "POST":
        action = request.POST.get("action")

        if action == u"添加用例":
            """添加用例的ajax"""
            id_list = request.POST.getlist("id_list[]")
            case_list = []
            for i in id_list:
                tmp = InCaseList.objects.get(id=i)
                case_list.append(tmp)
            return render_to_response("addcase_api_perform.html", {"case_list": case_list})

        if action == u"添加业务流":
            """添加业务流的ajax"""
            id_list = request.POST.getlist("id_list[]")
            bus_list = []
            for i in id_list:
                tmp = sql_commend("select * from webapp_api_business where id=%s" % i)
                bus_list.extend(tmp)
            return render_to_response("addcase_api_perform.html", {"bus_list": bus_list})

        if action == u"保存执行":
            """新建执行保存操作"""
            name = request.POST.get("name")
            c_name = request.POST.getlist("c_name")
            case_type = request.POST.getlist("case_type")
            case_id = request.POST.getlist("case_id")
            bus_id = request.POST.getlist("bus_id")

            try:
                print "开始写入执行表名称:", name
                ap_obj = User.objects.get(username=request.user).ap_set.create(name=name)
            except:
                return HttpResponse("名称重复")
            try:
                for i in range(len(case_type)):
                    # 写入执行详细表
                    detail_obj = ap_obj.ap_detail_set.create(name=c_name[i], case_type=case_type[i])
                    detail_obj.case_id = case_id[i]
                    detail_obj.api_id = bus_id[i]
                    detail_obj.save()
                return HttpResponse("保存成功")
            except:
                return HttpResponse("保存失败")

        if action == u"维护执行":
            """点击维护读取用例的内容载入页面"""
            c_id = request.POST.get("c_id")
            c_obj = Ap.objects.get(id=c_id)
            detail_obj = c_obj.ap_detail_set.all()

            # 获取当前用户对应项目的所有用例
            pro_list = Project.objects.filter(pro_user__contains=request.user)
            case_list = []
            business_list = []
            for i in pro_list:
                case_tmp = Project.objects.get(id=i.id).incaselist_set.all()
                case_list.extend(case_tmp)

                bus_tmp = Project.objects.get(id=i.id).api_business_set.all()
                business_list.extend(bus_tmp)

            return render_to_response("ad_perform.html",
                                      {"c_obj": c_obj, "detail_list": detail_obj, "case_list": case_list,
                                       "business_list": business_list,"pro_list":pro_list})

        if action == u"修改执行":
            """修改执行的保存操作"""
            c_id = request.POST.get("c_id")
            name = request.POST.get("name")
            c_name = request.POST.getlist("c_name")
            case_type = request.POST.getlist("case_type")
            case_id = request.POST.getlist("case_id")
            bus_id = request.POST.getlist("bus_id")

            try:
                print "开始更新执行名称"
                Ap.objects.filter(id=c_id).update(name=name)
            except:
                return HttpResponse("更新用例名称失败")

            d_obj = ap_detail.objects.filter(ap_id=c_id)

            try:
                print "开始更新执行用例的详细内容"
                for i in range(len(c_name)):
                    try:
                        ap_detail.objects.filter(id=d_obj[i].id).update(name=c_name[i], case_type=case_type[i],
                                                                        case_id=case_id[i], api_id=bus_id[i],
                                                                        edit_date=get_time())
                    except:
                        Ap.objects.get(id=c_id).ap_detail_set.create(name=c_name[i], case_type=case_type[i],
                                                                     case_id=case_id[i], api_id=bus_id[i],
                                                                     edit_date=get_time())

                if len(c_name) < len(d_obj):
                    print "POST数据长度小于数据库长度,删除多余的数据库内容"
                    del_obj = d_obj[len(c_name):len(d_obj)]
                    for i in del_obj:
                        i.delete()

                return HttpResponse("保存成功")
            except:
                return HttpResponse("保存失败")

        if action == u"查询用例":
            pro_id = request.POST.get("pro_id")
            case_list = Project.objects.get(id=pro_id).incaselist_set.filter(status="有效")
            return render_to_response("ProCaseList.html",{"case_list":case_list})

        if action == u"查询业务流":
            pro_id = request.POST.get("pro_id")
            business_list = Project.objects.get(id=pro_id).api_business_set.all()

            print pro_id
            print business_list
            return render_to_response("ProCaseList.html",{"business_list":business_list})

    if request.method == "GET":
        """新增执行"""
        # 获取当前用户对应项目的所有用例
        pro_list = Project.objects.filter(pro_user__contains=request.user)
        case_list = []
        business_list = []
        for i in pro_list:
            case_tmp = Project.objects.get(id=i.id).incaselist_set.all()
            case_list.extend(case_tmp)

            bus_tmp = Project.objects.get(id=i.id).api_business_set.all()
            business_list.extend(bus_tmp)
        pro_list = Project.objects.all()
        return render_to_response("ad_perform.html",
                                  {"case_list": case_list, "business_list": business_list,"pro_list":pro_list,})
