# -.- coding:utf-8 -.-
from django.conf.urls import patterns, include, url
from django.contrib import admin


# 登录url
urlpatterns = patterns('webapp.views',
                       url(r"^$", "login_view"),
                       )

# 默认后台
urlpatterns += patterns('',
                        url(r'^admin/', include(admin.site.urls)),
                        )

# 首页
urlpatterns += patterns('webapp.views',
                        url(r'^index/$', "index"),
                        )

# 退出登录
urlpatterns += patterns('webapp.views',
                        url(r'^logout_page/$', "logout_page"),
                        )

# UI用例列表
urlpatterns += patterns('webapp.views',
                        url(r'^case_list/$', "case_list"),
                        )

# 增加UI业务流
urlpatterns += patterns('webapp.views',
                        url(r'^add_business/$', "add_business"),
                        )

# 各种ajax
urlpatterns += patterns('webapp.views',
                        url(r'^case_ajax/$', "case_ajax"),
                        url(r'^method_ajax/$', "method_ajax"),
                        url(r'^action_ajax/$', "action_ajax"),
                        url(r"^perform_case_ajax/$", "perform_case_ajax"),
                        url(r'^process_ajax/$', "process_ajax"),
                        url(r'^ele_list_ajax/$', "element_list_ajax"),
                        url(r'^perform_ajax/$', "perform_ajax"),
                        url(r'^add_new_env_ajax/$', "addNewEnvAjax"),
                        url(r'^env_list_ajax/$', "envListAjax"),
                        url(r'^search_ajax/$', "search_ajax"),
                        url(r'add_new_messageObj_ajax/$', "add_new_messageObj_ajax"),
                        url(r'add_new_diffObj_ajax/$', "add_new_diffObj_ajax"),
                        url(r'chsTemp_ajax/$', "chsTemp_ajax"),
                        url(r'mdy_Temp_ajax/$', "mdy_Temp_ajax"),
                        url(r'importTemp_ajax/$', "importTemp_ajax"),
                        url(r'serchTemp_ajax/$', "serchTemp_ajax"),
                        url(r'add_template_ajax/', "add_template_ajax"),
                        url(r'add_interface_ajax/', "add_interface_ajax"),
                        url(r'imp_interface_ajax/', "imp_interface_ajax"),
                        )



# 业务流列表
urlpatterns += patterns('webapp.views',
                        url(r'^business_list/$', "business_list"),
                        )
# 新增-维护UI测试执行
urlpatterns += patterns('webapp.views',
                        url(r'^add_perform/$', "add_perform"),
                        )
# UI测试执行列表
urlpatterns += patterns('webapp.views',
                        url(r'^perform_list/$', "perform_list"),
                        )
# 用户管理
urlpatterns += patterns('webapp.views',
                        url(r'^user_management/$', "user_management"),
                        )
# 项目管理
urlpatterns += patterns('webapp.views',
                        url(r'^project_management/$', "project_management"),
                        )
# 新增项目
urlpatterns += patterns('webapp.views',
                        url(r'add_project/$', "add_project"),
                        )


# 测试详情列表页面
urlpatterns += patterns('webapp.views',
                        url(r'^report/$', "report"),
                        )

# 测试报告
urlpatterns += patterns('webapp.views',
                        url(r'^report_html/(?P<html_name>.+)/$', "report_html"),
                        )
# 元素管理
urlpatterns += patterns('webapp.views',
                        url(r'^add_element/$', "add_element"),
                        )
# 新增、维护用例
urlpatterns += patterns('webapp.views',
                        url(r'^case_process/$', "case_process"),
                        )

# 元素信息
urlpatterns += patterns('webapp.views',
                        url(r'^element_msg/$', "element_msg"),
                        )

#
urlpatterns += patterns('webapp.views',
                        url(r'^interfaceParamManager/$', "interfaceParamManager"),
                        )

# 接口用例列表
urlpatterns += patterns('webapp.views',
                        url(r'interface_caselist/', "interface_caselist"),
                        )

# 环境管理
urlpatterns += patterns('webapp.views',
                        url(r'data_base_manager/', "data_base_manager"),
                        )

# 接口模版管理
urlpatterns += patterns('webapp.views',
                        url(r'add_template/', "add_template"),
                        )

# 新增维护接口用例
urlpatterns += patterns('webapp.views',
                        url(r'add_inter_face/', "add_inter_face"),
                        )
# 新增接口业务流
urlpatterns += patterns('webapp.views',
                        url(r'api_business/', "api_business"),
                        )

# 接口业务流列表
urlpatterns += patterns('webapp.views',
                        url(r'api_list/', "api_list"),
                        )
# 接口测试执行列表
urlpatterns += patterns('webapp.views',
                        url(r'api_perform/', "api_perform"),
                        )

# 新增编辑接口测试执行
urlpatterns += patterns('webapp.views',
                        url(r'ad_perform/', "ad_perform"),
                        )



# 测试用
urlpatterns += patterns('webapp.views',
                        url(r'^base/$', "base"),
                        )