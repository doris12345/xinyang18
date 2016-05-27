/* 左侧导航下拉 */
var hiddendivs = $('div.hidden');
var showmore = $('div.showmore');

(function ($) {
    showmore.click(function () {

        $(this).toggleClass('on');
        $(this).nextAll('div.hidden:first').slideToggle(300);
        this.blur();
        return false;
    })

})(jQuery);

/* 页面右侧缩放 */
var temp = 0;
function show_menu() {
    if (temp == 0) {
        $('.left').css({"display": "none"});
        $('.right').css({"width": "95%"});
        $('.right').css({"margin-left": "0"});
        $('.center').css({"background": "url(../static/img/center2.png)"});
        temp = 1;
    }
    else {
        $('.left').css({"display": "block"});
        $('.right').css({"width": "84%"});
        $('.center').css({"background": "url(../static/img/center.png)"});
        temp = 0;
    }
}


/* 新增测试用例页面 新减步骤 */
(function ($) {
    var index = 0;
    $(".show_addmore").click(function () {
        var addstep = index + 1;
        $(".list02 tr:last").after("<tr>" +
            "<td><input type='checkbox' class='checkbox' id='' name='checkbox'></td>" +
            "<td>" + addstep + "</td>" +
            "<td><input type='text' name='step_name' value=''/></td>" +
            "<td><select name='method' id=''><option value=''></option><option value='id'>id</option><option value='name'>name</option><option value='class name'>class name</option><option value='css selector'>css selector</option><option value='xpath'>xpath</option><option value='tag name'>tag name</option><option value='link text'>link text</option></select></td>" +
            "<td><input type='text' name='element' value=''/></td>" +
            "<td><input type='text' name='value' value=''/></td>" +
            "<td><select name='action' id=''><option value=''></option><option value='输入'>输入</option><option value='单击'>单击</option><option value='鼠标悬停'>鼠标悬停</option><option value='进入iframe'>进入iframe</option><option value='退出iframe'>退出iframe</option><option value='上传导入'>上传导入</option><option value='切换到下一个窗口'>切换到下一个窗口</option><option value='切换到默认窗口'>切换到默认窗口</option><option value='关闭当前窗口'>关闭当前窗口</option><option value='切换到指定窗口'>切换到指定窗口</option><option value='标准断言'>标准断言</option><option value='高级断言'>高级断言</option><option value='模拟回车键'>模拟回车键</option><option value='输入随机数字'>输入随机数字</option><option value='输入随机身份证'>输入随机身份证</option><option value='输入随机字符串'>输入随机字符串</option><option value='执行Linux命令'>执行Linux命令</option><option value='取值'>取值</option><option value='取值断言'>取值断言</option></select></td>" +
            "</tr>");
        index += 1;
        /* $(this).nextAll('ul.addmore:first').toggle(); */
        updateTags();
    });

    $(".show_addmore1").click(function () {
        var addstep = index + 1;
        $(".list02 tr:last").after("<tr>" +
            "<td><input type='checkbox' class='checkbox' id='' name='checkbox'></td>" +
            "<td>" + addstep + "</td>" +
            "<td><input type='text' name='step_name' value=''/></td>" +
            "<td><select name='method' id=''><option value=''></option><option value='id'>id</option><option value='name'>name</option><option value='class name'>class name</option><option value='css selector'>css selector</option><option value='xpath'>xpath</option><option value='tag name'>tag name</option><option value='link text'>link text</option></select></td>" +
            "<td><input type='text' name='element' value=''/></td>" +
            "<td><input type='text' name='value' value=''/></td>" +
            "<td><select name='action' id=''><option value=''></option><option value='输入'>输入</option><option value='单击'>单击</option><option value='鼠标悬停'>鼠标悬停</option><option value='进入iframe'>进入iframe</option><option value='退出iframe'>退出iframe</option><option value='上传导入'>上传导入</option><option value='切换到下一个窗口'>切换到下一个窗口</option><option value='切换到默认窗口'>切换到默认窗口</option><option value='关闭当前窗口'>关闭当前窗口</option><option value='切换到指定窗口'>切换到指定窗口</option><option value='标准断言'>标准断言</option><option value='高级断言'>高级断言</option><option value='模拟回车键'>模拟回车键</option><option value='输入随机数字'>输入随机数字</option><option value='输入随机身份证'>输入随机身份证</option><option value='输入随机字符串'>输入随机字符串</option><option value='执行Linux命令'>执行Linux命令</option><option value='取值'>取值</option><option value='取值断言'>取值断言</option></select></td>" +
            "</tr>");
        index += 1;
        updateTags();
        /* $(this).nextAll('ul.addmore:first').toggle(); */
    });
    $(".delete").click(function () {
        if (index == 0) {
            return false;
        } else {
            $(".list01 tr:last").remove();
            index -= 1;
        }
    });
})(jQuery);


/* 选中删除 */
(function ($) {
    $(document).on("click", ".delete_case", function () {
        var checkbox = $(".checkbox");
        var btn_name = $(this).text();
        var id_str = []
        for (var i = 0; i < checkbox.length; i++) {
            if (checkbox[i].checked == true) {
                id_str.push(checkbox[i].value);
                checkbox.eq(i).parents("tr").remove();
            }
        }
        $.post("", {'get_id': id_str, btn_name: btn_name}, function (aa, bb) {
            alert(aa);
            location.reload();
            return (aa, bb);
        })
    })
})(jQuery);

(function ($) {
    $(".delete_business").click(function () {
        var checkbox = $(".checkbox");
        var btn_name = $(this).text();
        var id_str = []
        for (var i = 0; i < checkbox.length; i++) {
            if (checkbox[i].checked == true) {
                id_str.push(checkbox[i].value);
                checkbox.eq(i).parents("tr").remove();
            }
        }
        $.post("", {'get_id': id_str, btn_name: btn_name}, function (aa, bb) {
            return (aa, bb);
        })
    });

})(jQuery);

(function ($) {
    $(document).on("click", ".delete_perform", function () {
        var checkbox = $(".checkbox");
        var btn_name = $(this).text();
        var id_str = []
        for (var i = 0; i < checkbox.length; i++) {
            if (checkbox[i].checked == true) {
                id_str.push(checkbox[i].value);
                checkbox.eq(i).parents("tr").remove();
            }
        }
        $.post("", {'get_id': id_str, "action": btn_name}, function (aa, bb) {
            location.reload();
            return (aa, bb);
        })
    })

})(jQuery);


(function ($) {
    $(".delete_mdy_perform").click(function () {
        var checkbox = $(".checkbox");
        var btn_name = $(this).text();
        var id_str = []
        for (var i = 0; i < checkbox.length; i++) {
            if (checkbox[i].checked == true) {
                id_str.push(checkbox[i].value);
                checkbox.eq(i).parents("tr").remove();
            }
        }
    });

})(jQuery);


//input表单焦点获得失去
$("input.foucs_blur").focus(function () {
    if ($(this).val() == this.defaultValue) {
        $(this).val("");
    }
}).blur(function () {
    if ($(this).val() == '') {
        $(this).val(this.defaultValue);
    }
});


/*tab切换*/
function tabs(tabTit, on, tabCon) {
    $(tabCon).each(function () {
        $(this).children().eq(0).show();
    });
    $(tabTit).each(function () {
        $(this).children().eq(0).addClass(on);
    });
    $(tabTit).children().click(function (event) {
        event.stopPropagation();
        $(this).addClass(on).siblings().removeClass(on);
        var index = $(tabTit).children().index(this);
        $(tabCon).children().eq(index).show().siblings().hide();
    });
}
tabs(".tab-head", "active", ".tab-content");


/* 页面弹出框框 */
$(function () {
    $(document).on("click", ".addcase_btn", function () {
        $(".mask").show();
        showDialog();
        $("#add_case_div").show();

        $("#test_list").empty();
        check_list = $(".checkbox");
        for (i = 0; i < check_list.length; i++) {
            check_list[i].checked = false
        }
        checkbox_case = $(".checkbox_case");
        for (i = 0; i < checkbox_case.length; i++) {
            checkbox_case[i].checked = false
        }
    })

    $(document).on("click", ".addcase_btn02", function () {
        $(".mask").show();
        showDialog();
        $("#test_cases02").show();
        $("#business_list").empty();
        check_list = $(".checkbox");
        for (i = 0; i < check_list.length; i++) {
            check_list[i].checked = false
        }
        checkbox_case = $(".checkbox_case");
        for (i = 0; i < checkbox_case.length; i++) {
            checkbox_case[i].checked = false
        }
    })


    $(".dialog .addcase_save").click(function () {//注册保存按钮点击事件
        $(".dialog").hide();
        $(".mask").hide();
    })

    $(".dialog .cancel").click(function () {//注册取消按钮点击事件
        $(".dialog").hide();
        $(".mask").hide();
    })


    /*根据当前页面与滚动条位置，设置提示对话框的Top与Left*/
    function showDialog() {
        var objW = $(window); //当前窗口
        var objC = $(".dialog"); //对话框
        var brsW = objW.width();
        var brsH = objW.height();
        var sclL = objW.scrollLeft();
        var sclT = objW.scrollTop();
        var curW = objC.width();
        var curH = objC.height();
        //计算对话框居中时的左边距
        var left = sclL + (brsW - curW) / 2;
        //计算对话框居中时的上边距
        var top = sclT + (brsH - curH) / 2;
        //设置对话框在页面中的位置
        objC.css({"left": left, "top": top});
    }

    $(window).resize(function () {//页面窗口大小改变事件
        if (!$(".dialog").is(":visible")) {
            return;
        }
        showDialog(); //设置提示对话框的Top与Left
    });

})


/* 用户管理 */
$(function () {
    var index = 0;
    $(".add_user").click(function () {
        var addstep = index + 1;
        $(".list02 tr:last").after("<tr>" +

            "<td><input type='checkbox' class='checkbox' id='' name=''></td>" +

            "<td>" + addstep + "</td>" +

            "<td class='username'></td>" +

            "<td><input type='password' value='' readonly='readonly'/></td>" +

            "<td></td>" +

            "</tr>");
        index += 1;
    });

})

/* 复选框只能选择一个 */
$(function () {
    var checkbox = $(".usertable .checkbox");
    checkbox.click(function () {
        var num = 0;
        for (var i = 0; i < checkbox.length; i++) {
            if (checkbox[i].checked) {
                num++;
            }
        }
        if (num >= 2) {
            this.checked = false;
            alert("只能选择一条记录！");
        }
    })

});

//添加用例的关闭div按钮
$(document).on("click", "#close_add_case", function () {
    $("#test_cases01").hide();
    $("#test_cases02").hide();
    $("#mask").hide()
})

/*------------------------------------add_perform.html--------------------------------------------*/
//添加用例
$(document).on("click", "#per_add_case", function () {
    $(".mask").show();
    showDialog();
    $("#per_addcase_div").show();
    $("#judge").val("choose_again");
})

//添加用例--取消按钮
$(document).on("click", "#gb_per_addcase", function () {
    var judge=$("#judge").val();
    //alert(judge);
    if(judge=="choose_again"){
        $("#per_addcase_div").hide();
        $(".mask").hide();
        $("#p_add_case").empty();
    }
    if(judge=="choose_first"){
        $.get("/perform_list/", function (date) {
            $(".right").empty();
            $(".right").append(date);
        })
    }
})

//添加用例(包括接口用例，业务流)--保存按钮
$(document).on("click", "#ad_case", function () {
    var a = $(".checkbox_case:checked");
    var b = $(".checkbox_incase:checked");
    var c = $(".checkbox_bus:checked");
    //获取所勾选用例的id
    var caseidStr = [];
    var incaseidStr = [];
    var busidStr = [];
    for (var i = 0; i < a.length; i++) {
        caseidStr.push(a[i].name);
    }
    for (var i = 0; i < b.length; i++) {
        incaseidStr.push(b[i].name);
    }
    for (var i = 0; i < c.length; i++) {
        busidStr.push(c[i].name);
    }

    if(a.length == 0 && b.length == 0 && c.length == 0){
        alert("请至少选择一个用例！");
    }
    else{
            $.post('/perform_ajax/', {"action": "添加用例","case":caseidStr, "incase":incaseidStr, "bus":busidStr}, function (data) {
                $("#sortable").append(data);
                $("#per_addcase_div").hide();
                $("#mask").hide();
                $("#p_add_case").empty();
            });
            $(".checkbox_case").attr("checked", false);
        }
})


//添加用例--查询按钮
$(document).on("click", "#qry_btn", function () {
    //取下拉框中当前项目的ID
    var obj = document.getElementById('select_case');
    var text = obj.options[obj.selectedIndex].value;
    if (text == "" | text == null) {
        $("#test_list").empty();
    }
    else {
        $.post("/perform_case_ajax/", {"pro_id": text}, function (result) {
            $("#p_add_case").empty();
            $("#p_add_case").append(result);
        })
    }
})

//保存执行
$(document).on("click", "#create_case_perform", function () {
    var name = $(".search input").val();
    if (name == "" || name == null) {
        alert("执行名称不能为空")
    }
    else {
        $("#save_perform").ajaxSubmit(function (date) {
            alert(date);
            if (date == "保存成功") {
                $.get("/perform_list/", function (date) {
                    $(".right").empty();
                    $(".right").append(date);
                })
            }
        })
        return false
    }
})

//删除用例
$(document).on("click", ".per_del_case", function () {
    $(this).parent().parent().remove();
})

//维护用例
$(document).on("click", ".dgb_all", function () {
    var get_id = $(this).attr("name");
    var nature = $(this).attr("nature");
    if (nature == "测试用例") {
        $.post("/case_process/", {"action": "维护用例", "case_id": get_id}, function (date) {
            $(".right").empty();
            $(".right").append(date);
        })
    }
    if (nature == "接口用例") {
        $.post("/add_inter_face/", {"action": "维护接口用例", "get_id": get_id}, function (date) {
            $(".right").empty();
            $(".right").append(date);
        })
    }
    if (nature == "业务流用例") {
        $.post("/add_business/", {"action": "维护业务流", "bus_id": get_id}, function (date) {
            $(".right").empty();
            $(".right").append(date);
        })
    }
})

//添加用例--全选
$(document).on("click", ".all_case", function () {
    var isChecked = $(this)[0].checked;

    var checkbox_case=document.getElementsByClassName("checkbox_case");
    var checkbox_incase=document.getElementsByClassName("checkbox_incase");
    var checkbox_bus=document.getElementsByClassName("checkbox_bus");

    for(var i=0;i<checkbox_case.length;i++)
       checkbox_case[i].checked=isChecked;
    for(var i=0;i<checkbox_incase.length;i++)
       checkbox_incase[i].checked=isChecked;
    for(var i=0;i<checkbox_bus.length;i++)
       checkbox_bus[i].checked=isChecked;

    //var check_all = $(this)[0].checked;
    //if (check_all == true) {
    //    $(".checkbox_case").attr("checked", true);
    //}
    //if (check_all == false) {
    //    $(".checkbox_case").attr("checked", false);
    //}

})

/*------------------------------------perform_list.html--------------------------------------------*/
//运行执行
$(document).on("click", ".per_debug", function () {
    var msg = confirm("请确认打开调试客户端");
    if (msg == true) {
        var case_id = $(this).attr("name");
        var action = $(this).text();
        $.post("/perform_list/", {case_id: case_id, "action": action}, function (result) {
            alert(result)
        })
    }
})


//点击新增执行
$(document).on("click", "#ac_perform", function () {
    $.get("/add_perform/", function (date) {
        $(".right").empty();
        $(".right").append(date);
        $(".mask").show();
        showDialog();
        $("#per_addcase_div").show();
        $("#judge").val("choose_first");
    })
})

//维护执行
$(document).on("click", ".wh_perform", function () {
    var per_id = $(this).attr("name");
    $.post("/add_perform/", {"action": "维护执行", "per_id": per_id}, function (date) {
        $(".right").empty();
        $(".right").append(date);
        $("#judge_case").val("1");//1:从维护执行进入用例维护页面；2：从维护业务流进入用例维护页面；
        $("#judge_id").val(per_id);
    })
})

//复制执行
$(document).on("click", ".perform_copy", function () {
     var per_id = $(this).attr("name");  //获取执行的id
     $.post("/add_perform/", {"action": "复制执行", "per_id": per_id}, function (date) {
        $(".right").empty();
        $(".right").append(date)
    })
})

//删除执行
$(document).on("click", ".sc_perform", function () {
    var perform_id = $(this).attr('name');
    var msg = confirm("确认删除吗?");
    if (msg == true) {
        $(this).parent().parent().remove();
        $.post("/perform_list/", {'get_id': perform_id, "action": "删除执行"}, function (date) {
            alert(date);
            if (date == "删除成功") {
                $.get("/perform_list/", function (date) {
                    $(".right").empty();
                    $(".right").append(date);
                })
            }
        })
    }
})

//点击执行名称查看详细信息
$(document).on("click", ".perform_detail", function () {
    var per_id = $(this).attr("name");//获取执行的id
    $.post("/perform_list/", {"per_id": per_id, action: "查看执行详细信息"}, function (date) {
         $(".right").empty();
         $(".right").append(date);
    })
})

/*------------------------------------api_list.html--------------------------------------------*/
//维护用例
$(document).on("click", ".edit_case", function () {
    var case_id = $(this).attr("name");
    $.post("/api_business/", {"action": "维护用例", "id": case_id}, function (date) {
        $(".right").empty();
        $(".right").append(date);

    })
})


//删除接口业务流
$(document).on("click", ".del_btn", function () {
    var msg = confirm("确认删除吗?");
    if (msg == true) {
        var inbu_id = $(this).attr("name");
        $(this).parent().parent().remove();
        $.post("/api_list/", {"action": "删除业务流", "inbu_id": inbu_id})
    }
})

//调试用例
$(document).on("click", ".dbg_api", function () {
    var msg = confirm("请确认打开调试客户端");
    if (msg == true) {
        var api_id = $(this).attr("name");
        var pro_name = $(".top span").eq(0).text();

        $.post("/api_list/", {"action": "调试用例", "pro_name": pro_name, "api_id": api_id}, function (date) {
            alert(date)
        })
    }
})

//新增业务流
$(document).on("click", "#add_api_bus", function () {
    var pro_name = $(".top span").eq(0).text();
    $.post("/api_business/", {"action": "页面跳转", redirect: pro_name}, function (date) {
        $(".right").empty();
        $(".right").append(date);

    })
})

/*------------------------------------api_business.html--------------------------------------------*/
function showDialog() {
    var objW = $(window); //当前窗口
    var objC = $(".dialog"); //对话框
    var brsW = objW.width();
    var brsH = objW.height();
    var sclL = objW.scrollLeft();
    var sclT = objW.scrollTop();
    var curW = objC.width();
    var curH = objC.height();
    //计算对话框居中时的左边距
    var left = sclL + (brsW - curW) / 2;
    //计算对话框居中时的上边距
    var top = sclT + (brsH - curH) / 2;
    //设置对话框在页面中的位置
    objC.css({"left": left, "top": top});
}


//添加用例按钮
$(document).on("click", "#add_case", function () {
    $("#mask").show();
    showDialog();
    $(".dialog").show();
})


//删除用例按钮
$(document).on("click", "#del_case", function () {
    var check_list = $(".checkbox:checked");
    for (i = 0; i < check_list.length; i++) {
        check_list.eq(i).parent().parent().remove()
    }
})

//添加用例--查询按钮
$(document).on("click","#apibus_qry",function(){
    var pro_id = $("#apibus_prolist").find("option:selected").val();
    $.post("/add_inter_face/",{"action":"查询用例","pro_id":pro_id},function(date){
        $("#apubus_div").empty();
        $("#apubus_div").append(date);
    })
})

//添加用例--添加按钮
$(document).on("click","#apibus_tjcase",function(){
    var check_list = $(".checkbox_x:checked");
    var id_list = [];
    for(i=0;i<check_list.length;i++){
        id_list.push(check_list.eq(i).attr("name"))
    }
    $.post("/add_inter_face/",{"id_list":id_list,"action":"添加用例"},function(date){
        $("#case_list").append(date);

        $(".dialog").hide();
        $("#mask").hide();
        $(".checkbox_x:checked").attr("checked",false);

    })
})


//添加用例--取消按钮
$(document).on("click","#cencel_apibus",function(){
    $(".dialog").hide();
    $("#mask").hide();
    $(".checkbox_x:checked").attr("checked",false);
})


//保存按钮
$(document).on("click", "#bc_btn", function () {
    var ywlname = $("#ywlname").val();
    if (ywlname != "") {
        $("#save_api").ajaxSubmit(function (date) {
            alert(date);
            if (date == "保存成功") {
                var pro_name = $("#current_pro_name").text();
                $.post("/api_list/", {"action": "页面跳转", redirect: pro_name}, function (date) {
                    $(".right").empty();
                    $(".right").append(date);

                })
            }
        })
    }
    else {
        alert("请输入业务流名称")
    }
})


//维护用例
$(document).on("click",".edit_bus_case", function () {
    var case_id = $(this).attr("name");
     $.post("/add_inter_face/", {"action": "维护接口用例", "get_id": case_id}, function (date) {
        $(".right").empty();
        $(".right").append(date);
    })


})

/*------------------------------------api_perform.html--------------------------------------------*/
//新建执行
$(document).on("click", "#add_api_perform", function () {
    $.get("/ad_perform/", function (date) {
        $(".right").empty();
        $(".right").append(date)
    })
})


//删除执行
$(document).on("click", "#del_api_perform", function () {
    var check_list = $(".checkbox:checked");
    if (check_list.length == 0) {
        alert("请勾选要删除的执行用例")
    }
    else {
        var id_list = [];
        for (i = 0; i < check_list.length; i++) {
            var id_tmp = check_list.eq(i).attr("name");
            id_list.push(id_tmp)
            check_list.eq(i).parent().parent().remove();
        }
        $.post("/api_perform/", {"action": "删除执行", "id_list": id_list}, function (date) {
            alert(date)
        })
    }
})


//维护执行
$(document).on("click", ".mdy_perform", function () {
    var case_id = $(this).attr("name");
    $.post("/ad_perform/", {"action": "维护执行", "c_id": case_id}, function (date) {
        $(".right").empty();
        $(".right").append(date);
    })
})

//运行执行
$(document).on("click", ".run_perform", function () {
    var tmp_id = $(this).attr("name");
    var msg = confirm("请确认打开调试客户端");
    if (msg == true) {
        $.post("/api_perform/", {"action": "运行执行", "run_id": tmp_id}, function (date) {
            alert(date)
        })
    }
})


/*------------------------------------ad_perform.html--------------------------------------------*/
//添加用例
$(document).on("click", "#a_pr", function () {
    $("#mask").show();
    showDialog();
    $("#a_case").show();
})


//添加用例--查询
$(document).on("click", "#qry_case_ap", function () {
    var pro_id = $("#a_case select").find("option:selected").val();
    $.post("/ad_perform/", {"action": "查询用例", "pro_id": pro_id}, function (date) {
        $("#a_case div:eq(1)").empty();
        $("#a_case div:eq(1)").append(date);
    })
})


//添加业务流
$(document).on("click", "#a_bus", function () {
    $("#mask").show();
    showDialog();
    $("#show_bus").show();
})


//添加业务流--查询
$(document).on("click", "#qry_bus_ap", function () {
    var pro_id = $("#show_bus select").find("option:selected").val()
    $.post("/ad_perform/", {"action": "查询业务流", "pro_id": pro_id}, function (date) {
        $("#show_bus div:eq(1)").empty();
        $("#show_bus div:eq(1)").append(date);
    })
})


//添加用例--添加按钮
$(document).on("click", "#add_a", function () {
    var check_list = $(".checkbox_add:checked");
    var id_list = []

    if (check_list.length == 0) {
        alert("请勾选要添加的用例")
    }
    else {
        for (i = 0; i < check_list.length; i++) {
            var id_tmp = check_list.eq(i).attr("name")
            id_list.push(id_tmp)
        }
        $.post("/ad_perform/", {"id_list": id_list, "action": "添加用例"}, function (date) {
            $(".tablelist table tbody").eq(1).append(date)
        })

        $(".checkbox_add").attr("checked", false)
        $("#a_case").hide();
        $("#mask").hide();
    }
})


//添加用例--取消按钮
$(document).on("click", "#cencel_a", function () {
    $(".checkbox_add").attr("checked", false)
    $("#a_case").hide();
    $("#mask").hide();
    $("#add_element").hide();
})


//添加业务流--添加按钮
$(document).on("click", "#add_b", function () {
    var check_list = $(".checkbox_add:checked");
    if (check_list.length == 0) {
        alert("请勾选要添加的业务流")
    }
    else {
        var id_list = [];
        for (i = 0; i < check_list.length; i++) {
            var tmp_id = check_list.eq(i).attr("name")
            id_list.push(tmp_id)
        }
        $.post("/ad_perform/", {"action": "添加业务流", "id_list": id_list}, function (date) {
            $(".tablelist table tbody").eq(1).append(date)
        })
        $(".checkbox_add").attr("checked", false)
        $("#show_bus").hide();
        $("#mask").hide();
    }
})


//添加业务流--取消按钮
$(document).on("click", "#cencel_b", function () {
    $(".checkbox_add").attr("checked", false)
    $("#show_bus").hide();
    $("#mask").hide();
})


//删除用例
$(document).on("click", "#d_pr", function () {
    var check_list = $(".checkbox:checked");
    if (check_list.length == 0) {
        alert("请勾选要删除的用例")
    }
    else {
        for (i = 0; i < check_list.length; i++) {
            check_list.eq(i).parent().parent().remove()
        }
    }

})


//保存用例
$(document).on("click", "#s_pr", function () {
    $("#add_perform").ajaxSubmit(function (date) {
         alert(date);
        if (date == "保存成功") {
             $.post("/api_perform/", {"action": "跳转页面"}, function (date) {
            $(".right").empty();
            $(".right").append(date);
        })
        }
    })
    return false
})


//维护用例
$(document).on("click",".edit_pr_case", function () {
    var id = $(this).attr("name");
    var status = $(this).attr("status");
    if(status == "接口用例"){
     $.post("/add_inter_face/", {"action": "维护接口用例", "get_id": id}, function (date) {
        $(".right").empty();
        $(".right").append(date);
    })
    }
    if(status == "业务流用例"){
    $.post("/api_business/", {"action": "维护用例", "id": id}, function (date) {
        $(".right").empty();
        $(".right").append(date);

    })
    }
})
/*------------------------------------modify_inter_case_list.html--------------------------------------------*/
// 调试接口用例
$(document).on("click", ".debug", function () {
    var msg = confirm("请确认打开调试客户端");
    if (msg == true) {
        var in_id = $(this).attr("name");
        var pro_name = $("#current_proname").text();
        $.post("/interface_caselist/", {"action":"测试调试","in_id": in_id, pro_name: pro_name}, function (date) {
            if (date == "调试错误") {
                alert(date)
            }
        })
    }
})


// 删除接口用例
$(document).on("click", ".delete_caseA", function () {
    var msg = confirm("确认删除吗?");
        if (msg == true) {
            var in_id = $(this).attr("name");
            $(this).parent().parent().remove();
            $.post("/interface_caselist/", {'get_id':in_id, "action":"删除用例"}, function (result) {
                alert(result)
        })
    }

})


//新增接口用例
$(document).on("click", "#add_interface", function () {
    var pro_name = $("#current_proname").text();
    $.post("/add_inter_face/", {"action": "新增接口用例", redirect: pro_name}, function (date) {
        $(".right").empty();
        $(".right").append(date);
        $("#judge_case").val("0");
        $("#mask").show();
        showDialog();
        $("#use_template").show();
    })
})


//维护接口用例
$(document).on("click", ".mdy_interface", function () {
    var case_id = $(this).attr("name");
    $.post("/add_inter_face/", {"action": "维护接口用例", "get_id": case_id}, function (date) {
        $(".right").empty();
        $(".right").append(date);
        $("#judge_case").val("0");
        $("#judge_id").val(case_id);
    })
})


//复制接口用例
$(document).on("click", ".in_copy", function () {
     var incase_id = $(this).attr("name");  //获取复制用例的id
     var pro_name=$(this).attr("pro_name")
     $.post("/add_inter_face/", {"action": "复制用例", "incase_id": incase_id, "pro_name":pro_name}, function (date) {
        $(".right").empty();
        $(".right").append(date)
    })
})


//点击接口用例名显示详细信息
$(document).on("click", ".incase_detail", function () {
    var incase_id = $(this).attr("name");//获取接口用例的id
    var pro_name=$(this).attr("pro_name")

    $.post("/add_inter_face/", {"incase_id": incase_id, "pro_name":pro_name, action: "查看接口用例详细信息"}, function (date) {
         $(".right").empty();
         $(".right").append(date);
    })
})

/*------------------------------------add_inter_face.html--------------------------------------------*/

//导入模板--取消按钮
$(document).on("click", "#close_div", function () {
    var pro_name=$("#current_pro_name").text();
    $("#mask").hide();
    $("#use_template").hide();
     $.post("/interface_caselist/", {"action": "页面跳转", redirect: pro_name}, function (date) {
        $(".right").empty();
        $(".right").append(date);
    })
})


//导入模板--应用
$(document).on("click", "#imp_btn", function () {
    //获取模板ID
    var temp_id = $(this).attr("name");

    $("#template_id").val(temp_id);

    $("#table_div").empty();

    $.post("/add_interface_ajax/", {tmp_id: temp_id}, function (date) {
        $("#table_div").append(date)
    })
    $(".mask").hide();
    $("#use_template").hide();
})


//删除断言
$(document).on("click", ".delete_diff", function () {
    //获取当前的断言个数：如果只剩下一个断言，则不能被删除
    var msg = confirm("确认删除吗?");
    if (msg == true) {
        var diffs = $('.delete_diff');
        var len = diffs.length;
        if(len == 1)
            alert("该步骤不能被删除");
        else
            $(this).parent().parent().remove();
    }
})


//增加断言
$(document).on("click", ".add_diff", function () {
    var index=$(this).parent().parent().index();
    $("#inter_assert tr").eq(index).after("<tr>" +
    "<td><input type='text' name='assert_objName'></td>" +
    "<td><input type='text' name='field_name'></td>" +
    "<td><select class='assert_method' name='assert_method'><option></option><option value='返回值与数据库对比'>返回值与数据库对比</option><option value='期望值与返回值对比'>期望值与返回值对比</option><option value='期望值与数据库对比'>期望值与数据库对比</option><option value='脚本高级断言对比'>脚本高级断言对比</option></select></td>" +
    "<td><input type='text' name='expected_val'></td>" +
    "<td><input type='text' name='sql_str'></td>" +
    "<td id='operation'> <input type='button' class='add_diff' title='增加断言'>"+
    "<input type='button' class='add_timeout'  title='增加延时'>"+
    "<input type='button' class='delete_diff'  title='删除断言'></td>"+
    "</tr>");

})


//增加延时
$(document).on("click", ".add_timeout", function () {
    alert("脚本运行中会默认等待您输入的时间");
     var index=$(this).parent().parent().index();
    $("#inter_assert tr").eq(index).after("<tr>" +
        "<td><input type='text' name='assert_objName' readonly='readonly'></td>" +
        "<td><input type='text' name='field_name'  readonly='readonly'></td>" +
        "<td><select name='assert_method'><option value='延时等待'>延时等待</option></select></td>" +
        "<td><input type='text' name='expected_val' placeholder='请输入延迟的时间(整数/秒)'></td>" +
        "<td><input type='text' name='sql_str'></td>" +
        "<td id='operation'> <input type='button' class='add_diff'  title='增加断言'>"+
        "<input type='button' class='add_timeout'  title='增加延时'>"+
        "<input type='button' class='delete_diff'  title='删除断言'></td>"+
        "</tr>");
})


//保存用例
$(document).on("click", "#save_interface", function () {
    var in_name=$("#interface_name").val();
    var judge = $("#judge_case").val();
    var judge_id= $("#judge_id").val();
    var flag=false;
    $(".assert_method").each(function(index) {
    var self = $(this);
    var val = self.val();  //获得选中option.value; var text = self.find("option:selected").text() //获得选中的option中的文本值
    if(val=="")
        flag=true;
  })

    if (in_name == "") {
        alert("用例名称不能为空");
    }
    else if(flag == true){
        alert("断言的比对方式不能为空");
    }
    else {
        $("#interface").ajaxSubmit(function (date) {
            alert(date);
            if (date == "保存成功") {
                var pro_name = $("#current_pro_name").text();
                if(judge=="1") { //从维护执行页面进入接口用例维护页面
                    $.post("/add_perform/", {"action": "维护执行", "per_id": judge_id}, function (date) {
                        $(".right").empty();
                        $(".right").append(date);
                    })
                }
                else if(judge=="2") { //从维护业务流页面进入接口用例维护页面返回业务流维护
                    $.post("/add_business/", {"action": "维护业务流", "bus_id": judge_id}, function (date) {
                        $(".right").empty();
                        $(".right").append(date);
                    })
                }
                else if(judge=="0"){ //从接口模板创建用例进入新增接口用例页面，以及直接从接口用例维护
                    $.post("/interface_caselist/", {"action": "页面跳转", redirect: pro_name}, function (date) {
                        $(".right").empty();
                        $(".right").append(date);
                    })
                }
            }
        })
        return false
    }
})


/*------------------------------------case_process.html--------------------------------------------*/
//添加用例
$(document).on("click", "#case_add_case", function () {
    $(".mask").show(); //设置背景为阴影
    showDialog(); //弹出窗口
    $("#add_case_div").show();

})


 //增加web用例--删除步骤
$(document).on("click", ".delstep", function () {
    //获取当前的步骤个数：如果只剩下一个步骤，则不能被删除
    var $elements = $('.delstep');
    var len = $elements.length;
    if(len == 1)
        alert("该步骤不能被删除");
    else
        $(this).parent().parent().remove();

    //让所有步骤的序列号依次排序
    var checkbox_list = $(".checkbox_step");
    for(i in checkbox_list)
        checkbox_list.eq(i).parent().next().text(parseInt(i)+1);

})


//修改web用例--在紧邻该步骤后面增加步骤
$(document).on("click", "#xg_addstep", function () {
    //获取当前的步骤序号
    var index=$(this).parent().parent().index();

    $.get("/process_ajax/", function (date) {

        $("#tb tbody tr").eq(index).after("<tr>" +
        "<td style='display:none'> <input type='checkbox' class='checkbox_step' name='checkbox'></td>" +
        "<td></td>" +
        "<td><input type='text'  name='desc' style='width: 80%;'></td>" +
        "<td align='center'> <select name='fun' style='width: 80%;' class='select'> <option></option> <option value='单击'>单击</option> <option value='输入'>输入</option> <option value='标准断言'>标准断言</option> <option></option> <option style='font-size: 10px'>请选择</option></select> </td>" +
        "<td><input type='text'  name='value' style='width: 80%;'></td>" +
        "<td><input type='hidden' class='ele_id' name='ele_id' value=''> <a href='#' class='ele_name' style='color: red'>添加元素</a> </td>"+
        "<td align='center' id='operation2'><input id='addstep' type='button' title='新增步骤'> <input class='delstep' type='button' title='删除步骤'></td>" +
        "</tr>");

        //让所有步骤的序列号依次排序
        var checkbox_list = $(".checkbox_step");
        for(i in checkbox_list)
            checkbox_list.eq(i).parent().next().text(parseInt(i)+1);
    })
})


//增加web用例--在紧邻该步骤后面增加步骤
$(document).on("click", "#addstep", function () {
    //获取当前的步骤序号
    var index=$(this).parent().parent().index();

    $.get("/process_ajax/", function (date) {

        $("#tb tbody tr").eq(index).after("<tr>" +
        "<td style='display:none'><input type='checkbox' class='checkbox_step' name='checkbox'></td>" +
        "<td></td>" +
        "<td><input type='text' name='desc' style='width: 80%;'></td>" +
        "<td align='center'><select name='fun' style='width: 80%;' class='select'> <option></option> <option value='单击'>单击</option> <option value='输入'>输入</option> <option value='标准断言'>标准断言</option> <option></option> <option style='font-size: 10px'>请选择</option></select> </td>" +
        "<td><input type='text' name='value' style='width: 80%;'></td>" +
        "<td><input type='hidden' class='ele_id' name='ele_id' value=''> <a href='#' class='ele_name' style='color: red'>添加元素</a> </td>"+
        "<td align='center' id='operation2'><input id='addstep' type='button' title='新增步骤'> <input class='delstep' type='button' title='删除步骤'></td>" +
        "</tr>");

        //让所有步骤的序列号依次排序
        var checkbox_list = $(".checkbox_step");
        for(i in checkbox_list)
            checkbox_list.eq(i).parent().next().text(parseInt(i)+1);
    })
})


//增加步骤
$(document).on("click", "#add_step", function(){
    $.get("/process_ajax/", function(date) {
        $("#tb tbody").append(date)
    })
})


//步骤--添加元素
$(document).on("click", ".ele_name", function () {
    var current_pro_name = $("#current_pro_name").text();
    $.post("/ele_list_ajax/", {"current_pro_name": current_pro_name,"ele_id":0}, function (date) {
        $("#table_div").empty();
        $("#table_div").append(date);
    });

    //获取当前步骤序号
    var index=$(this).parent().parent().children().eq(1).text();
    $(".mask").show();
    showDialog();
    $("#element_list").show();
    $("#chosen_ele_index").val(index);

});


//元素列表--取消按钮
$(document).on("click", "#close_ele_list", function () {
    $("#element_list").hide();
    $(".mask").hide();
});


//元素列表--应用
$(document).on("click", ".yy_ele", function () {

    //获取应用元素的id和name
    elelist_id = $(this).attr("name");
    elelist_name = $(this).attr("ele_name");

    //找到被应用步骤中的元素id和name
    index=$("#chosen_ele_index").val();//被应用步骤的序号
    //alert(index);
    //alert(elelist_id);
    //alert(elelist_name);
    var ck_index=parseInt(index)-1;
    ele_id = $(".checkbox_step").eq(ck_index).parent().parent().find("[class=ele_id]");
    ele_name = $(".checkbox_step").eq(ck_index).parent().parent().find("[class=ele_name]");

    ele_id.val(elelist_id);
    ele_name.text(elelist_name);
    ele_name.css("color", "lightseagreen");
    $("#ele_id").val(elelist_id);
    $("#element_list").hide();
    $("#mask").hide();
});


//元素列表--编辑
$(document).on("click", ".bj_ele", function () {
    var tr_list = $(this).parent().parent().children();
    var case_msg = [];
    for (i = 0; i < tr_list.length - 1; i++) {
        var a = tr_list.eq(i).children().text();
        case_msg.push(a);
    }
    $("#element_list").hide();
    $("#mdy_ele_div").show();
    $("#m_id").val(case_msg[0]);
    $("#m_name").val(case_msg[1]);
    $("#m_fun").val(case_msg[2]);
    $("#m_val").val(case_msg[3]);
    $("#m_url").val(case_msg[4]);
    $("#m_desc").val(case_msg[5]);
})


//编辑元素--取消
$(document).on("click", "#close_mdy_ele", function () {
    $("#mdy_ele_div").hide();
    $("#element_list").show();
})


//编辑元素-保存
$(document).on("click", "#mdy_sure", function () {
    $("#mdy_ele_form").ajaxSubmit(function (date) {
        alert(date)
        if (date == "修改成功") {
            $("#mdy_ele_div").hide();
            $("#mask").hide();
        }
    })
    return false
})


//删除步骤
$(document).on("click", "#del_step", function () {

    $(this).parent().parent().remove();
})


//取消按钮
$(document).on("click", "#cencel", function () {
    var check_list = $(".checkbox_step");
    for (i = 0; i < check_list.length; i++) {
        if (check_list[i].checked == true) {
            check_list.eq(i).parent().parent().remove()
        }
    }
})


//元素详情-关闭按钮
$(document).on("click", "#close", function () {
    $(".mask").hide();
    $("#element_msg").hide();
    $("#msg").children().children().find("[class=thead]").siblings().remove()
})


//元素详情中的元素列表按钮
$(document).on("click", ".ele_list", function () {
    var current_pro_name = $("#current_pro_name").text();  //ajax POST当前项目名，取改项目下所有的元素列表显示
    $.post("/ele_list_ajax/", {"current_pro_name": current_pro_name}, function (date) {
        $("#table_div").empty();
        $("#table_div").append(date)

    })
    //$("#element_msg").hide();
    $("#element_list").show();
})

//排序
$(document).on("click", "#sort", function () {
    var checkbox_list = $(".checkbox_step");
    for (i = 0; i < checkbox_list.length; i++) {
        checkbox_list.eq(i).parent().next().text(i + 1)
    }
})


//添加元素按钮
$(document).on("click", "#cencel", function () {
    $("#element_list").hide();
    $("#add_element").show();
})


//添加元素--保存按钮
$(document).on("click", "#add_sure", function () {

    $("#save_add_ele").ajaxSubmit(function (date) {
        alert(date)
        if (date == "添加元素成功") {
            $("#save_add_ele").clearForm();
            $("#mask").hide();
            $("#add_element").hide();

        }
    })
    return false
})


//添加元素--取消按钮
$(document).on("click", "#close_ele", function () {
    $("#add_element").hide();
    $("#mask").hide();
})


//添加用例的保存按钮
$(document).on("click", ".save", function () {
    var check_obj = $(".checkbox_add:checked");
    var val_list = []
    if (check_obj.length > 1) {
        for (i = 0; i < check_obj.length; i++) {
            val_list.push(check_obj[i].value);
        }
    }
    else {
        val_list.push(check_obj.val())
    }

    $.post('/case_ajax/', {id: val_list}, function (date) {
        $("#tb tbody").append(date);

        $(".checkbox_add").attr("checked", false);
        $("#add_case_div").hide();
        $(".mask").hide();
        updateTags();
    });
})


//添加用例--取消按钮
$(document).on("click", "#close_add_case", function () {
    $("#add_case_div").hide();
    $(".checkbox_add").attr("checked", false);
    $(".mask").hide();
})


//保存用例按钮
$(document).on("click", "#save_case_process", function () {
    var case_name = $("#casename").val();
    //获取登录用户名，记录用户操作
    var username = document.getElementById("username").innerHTML;
    var judge = $("#judge_case").val();
    var judge_id= $("#judge_id").val();
    var pro_name = $("#current_pro_name").text();
    if (case_name == "" || case_name == null) {
        alert("请输入用例名称");
    }
    else{
        $("#save_process").ajaxSubmit(function (date) {
            alert(date);
            if (date == "保存成功" || date == "修改成功") {
                if(judge=="1") { //从维护执行页面进入Web用例维护页面，保存后返回执行维护
                        $.post("/add_perform/", {"action": "维护执行", "per_id": judge_id}, function (date) {
                        $(".right").empty();
                        $(".right").append(date);
                    })
                }
                else if(judge=="2") { //从维护业务流页面进入Web用例维护页面返回业务流维护
                         $.post("/add_business/", {"action": "维护业务流", "bus_id": judge_id}, function (date) {
                            $(".right").empty();
                            $(".right").append(date);
                        })
                }
                else if(judge=="0"){   //从维护用例页面进入Web用例维护页面返回用例列表
                        $.post("/case_list/", {"action": "页面跳转", redirect: pro_name}, function (date) {
                        $(".right").empty();
                        $(".right").append(date);
                    })
                }
            }
        })
        return false
    }
})


//下拉框请选择
$(document).on("change", ".select", function () {
    var checkText = $(this).find("option:selected").text();
    $("#yy_fun").attr("value", $(".select").index($(this))) //给应用按钮增加属性.值为select的索引
    if (checkText == "请选择") {
        $(".mask").show();
        showDialog();
        $("#fun_list").show();
        $(this).get(0).selectedIndex = 0; //弹出DIV，切换到第一个选项，以后可以再次出发change事件
        $(".checkbox_fun").attr("checked", false) //取消所有的勾选
    }
})


//动作列表--取消按钮
$(document).on("click", "#gb_fun_div", function () {
    $("#fun_list").hide();
    $(".mask").hide();
})


//动作列表--应用按钮
$(document).on("click", "#yy_fun", function () {
    var check_list = $(".checkbox_fun:checked");
    if (check_list.length != 1) {
        alert("请勾选一个动作")
    }
    else {
        fun_name = check_list.attr("value");
        select_index = $(this).attr("value");
        $(".select").eq(select_index).find("option").eq(0).text(fun_name);
        $(".select").eq(select_index).find("option").eq(0).val(fun_name);
        $("#fun_list").hide();
        $(".mask").hide();
    }
})

/*------------------------------------case_list.html--------------------------------------------*/
//新增用例
$(document).on("click", "#xz_yl", function () {
    var pro_name = $("#cur_name").text();
    //获取登录用户名，记录用户操作
    var username = document.getElementById("username").innerHTML;
    $.post("/case_process/", {"action": "页面跳转", "pro_name": pro_name,"username":username}, function (date) {
        $(".right").empty();
        $(".right").append(date);

        $.get("/process_ajax/", function (date) {
        $("#tb tbody").append(date)
        })

        $("#judge_case").val("0");
    })
})


//维护用例
$(document).on("click", ".mdy_case", function () {
    var case_id = $(this).attr("name");  //获取维护用例的id
    $.post("/case_process/", {"action": "维护用例", "case_id": case_id}, function (date) {
        $(".right").empty();
        $(".right").append(date);
        $("#judge_case").val("0");
        $("#judge_id").val(case_id);
    })
})


//复制用例
$(document).on("click", ".case_copy", function () {
     var case_id = $(this).attr("name");  //获取复制用例的id
     $.post("/case_process/", {"action": "复制用例", "case_id": case_id}, function (date) {
        $(".right").empty();
        $(".right").append(date)
    })
})


//测试调试
$(document).on("click", ".case_debug", function () {
    var msg = confirm("请确认打开调试客户端");
    if (msg == true) {
        var case_id = $(this).attr("name");
        //获取登录用户名，记录用户操作
        var username = document.getElementById("username").innerHTML;
        //alert(username);
        $.post("/case_list/", {"action": "测试调试", "case_id": case_id,"username":username}, function (date) {
            alert(date)
        })
    }
})


//删除用例
$(document).on("click", ".sc_yl", function () {
    var msg = confirm("确认删除吗?");
    if (msg == true) {
        var pro_name = $("#cur_name").text();
        var case_id = $(this).attr("name");
        $.post("/case_list/", {"action": "删除用例", "case_id": case_id}, function (date) {
            alert(date);
            if (date == "删除成功") {
            $.post("/case_list/", {"action": "页面跳转", redirect: pro_name}, function (date) {
                    $(".right").empty();
                    $(".right").append(date);
                })
            }
        })
        return false
    }
})


//点击用例名称查看详细信息
$(document).on("click", ".case_detail", function () {
    var case_id = $(this).attr("name");//获取用例的id
    $.post("/case_list/", {"case_id": case_id, action: "查看用例详细信息"}, function (date) {
         $(".right").empty();
         $(".right").append(date);
    })
})

/*------------------------------------add_element.html--------------------------------------------*/

//添加元素按钮
$(document).on("click", "#tj_ele", function () {
    $(".mask").show();
    showDialog();
    $("#add_ele_div").show();
})


//添加元素--保存按钮
$(document).on("click", "#add_sure", function () {

    //获取登录用户名，记录用户操作
    var username = document.getElementById("username").innerHTML;
    //获取项目名称
    pro_name=$(this).attr("name");
    //获取字段值
    var ele_name=$("#el_name").val();
    var ele_fun=$("#el_fun").val();
    var ele_url=$("#el_url").val();
    var ele_value=$("#el_value").val();
    var ele_desc=$("#el_desc").val();

     $.post("/add_element/", {"action": "添加元素", "username":username,"pro_name":pro_name,"ele_name":ele_name,"ele_fun":ele_fun,"ele_url":ele_url,"ele_value":ele_value,"ele_desc":ele_desc}, function (date) {
        alert(date)
        if (date == "添加成功") {
            $.post("/add_element/", {"action": "页面跳转", redirect: pro_name}, function (date) {
                $(".right").empty();
                $(".right").append(date);
            })
        }
    })
    return false
})


//添加元素--取消按钮
$(document).on("click", "#close_add_elediv", function () {
    $("#add_ele_div").hide();
    $(".mask").hide();
})


//编辑元素
$(document).on("click", "#xg_ele", function () {

    var tr = $(this).parent().parent().children();
    var td_text0 = tr.eq(0).children().text();
    var td_text1 = tr.eq(1).children().val();
    var td_text2= tr.eq(2).children().text();
    var td_text3 = tr.eq(3).children().text();
    var td_text4 = tr.eq(4).children().text();
    var td_text6 = tr.eq(6).children().text();

    $("#mdf_ele td").eq(0).children().val(td_text0);
    $("#mdf_ele td").eq(1).children().val(td_text1);
    $("#mdf_ele td").eq(2).children().val(td_text2);
    $("#mdf_ele td").eq(3).children().val(td_text3);
    $("#mdf_ele td").eq(4).children().val(td_text4);
    $("#mdf_ele td").eq(5).children().val(td_text6);

    //for (i = 0; i < tr.length-2; i++) {
    //    var td_text = tr.eq(i).children().text();
    //    $("#mdf_ele td").eq(i).children().val(td_text)
    //}

    $(".mask").show();
    showDialog();
    $("#xg_ele_div").show()

});


//编辑元素--取消按钮
$(document).on("click", "#gb_xgdiv", function () {
    $("#xg_ele_div").hide();
    $(".mask").hide();
});

//编辑元素--保存按钮
$(document).on("click", "#xg_ele_sure", function () {
    //获取登录用户名，记录用户操作
    var username = document.getElementById("username").innerHTML;

    //获取项目名称
    pro_name=$(this).attr("name");

    //获取字段值
    var ele_id=$("#ele_id").val();
    var ele_name=$("#ele_name").val();
    var ele_fun=$("#ele_fun").val();
    var ele_url=$("#ele_url").val();
    var ele_value=$("#ele_value").val();
    var ele_desc=$("#ele_desc").val();
    //alert(ele_desc)

     $.post("/add_element/", {"action": "修改元素", "username":username, "pro_name":pro_name, "ele_id":ele_id, "ele_name":ele_name, "ele_fun":ele_fun, "ele_url":ele_url, "ele_value":ele_value, "ele_desc":ele_desc}, function (date) {
        alert(date)
        if (date == "修改成功") {
            $.post("/add_element/", {"action": "页面跳转", redirect: pro_name}, function (date) {
                $(".right").empty();
                $(".right").append(date);
            })
        }
    });

    return false
});

//删除元素
$(document).on("click", "#sc_ele", function () {
    var msg = confirm("确认删除吗?");
    if (msg == true) {
        ele_id=$(this).attr("name");
        $.post("/add_element/", {"action": "删除元素", "ele_id": ele_id}, function (date) {
            alert(date);
            if (date == "删除成功") {
                var pro_name = $("#current_pro_name").text();
                $.post("/add_element/", {"action": "页面跳转", redirect: pro_name}, function (date) {
                    $(".right").empty();
                    $(".right").append(date);
                })
            }
        })
    }
});


//点击元素名称查看详细信息
$(document).on("click", ".ele_detail", function () {
    var tr = $(this).parent().parent().children();
    var td_text0 = tr.eq(0).children().text();
    var td_text1 = tr.eq(1).children().val();
    var td_text2= tr.eq(2).children().text();
    var td_text3 = tr.eq(3).children().text();
    var td_text4 = tr.eq(4).children().text();
    var td_text6 = tr.eq(6).children().text();

    var ele_id = $(this).attr("name");  //获取元素的id
    var pro_name = $(this).attr("pro_name");  //获取元素的id

    $.post("/add_element/", {"ele_id": ele_id, action: "查看元素详细信息","pro_name":pro_name}, function (date) {
         $(".right").empty();
         $(".right").append(date);
         $("#detail_ele td").eq(0).children().val(td_text0);
         $("#detail_ele td").eq(1).children().val(td_text1);
         $("#detail_ele td").eq(2).children().val(td_text2);
         $("#detail_ele td").eq(3).children().val(td_text3);
         $("#detail_ele td").eq(4).children().val(td_text4);
         $("#detail_ele td").eq(5).children().val(td_text6);
         $(".mask").show();
         showDialog();
         $("#detail_ele_div").show();
    })
});


//查看元素--关闭按钮
$(document).on("click", "#gb_viewdiv", function () {
    $("#detail_ele_div").hide();
    $(".mask").hide();
});

/*------------------------------------business_list.html--------------------------------------------*/
//新增业务流
$(document).on("click", "#zj_bus", function () {
    var pro_name = $(".top span")[0].textContent;
    $.post("/add_business/", {"action": "页面跳转", redirect: pro_name}, function (date) {
        $(".right").empty();
        $(".right").append(date);
        $(".mask").show();
        $("#judge_case").val("2");
        showDialog();
        $("#bus_addcase_div").show();
        $("#judge_bus").val("choose_first");
    })
})


//取消添加用例弹框
$(document).on("click", "#cancel_addcase_div", function () {
    $("#bus_addcase").hide();
    $(".mask").hide();
})

//维护业务流
$(document).on("click", ".wh_bus", function () {
    var bus_id = $(this).attr("name");
    $.post("/add_business/", {"action": "维护业务流", "bus_id": bus_id}, function (date) {
        $(".right").empty();
        $(".right").append(date);
        $("#judge_case").val("2");//2：从维护业务流进入用例维护页面；
        $("#judge_id").val(bus_id);
    })
})

//删除业务流
$(document).on("click", ".sc_bus", function () {
    var msg = confirm("确认删除吗?");
    if (msg == true) {
        var bu_id = $(this).attr("name");
        $(this).parent().parent().remove();

        $.post("/business_list/", {"action": "删除业务流", "bu_id": bu_id}, function (date) {
            alert(date);
            if (date == "删除成功") {
                var pro_name = $(".top span")[0].textContent;
                $.post("/business_list/", {"action": "页面跳转", redirect: pro_name}, function (date) {
                    $(".right").empty();
                    $(".right").append(date);
                })
            }
        })
    }
});


//复制业务流
$(document).on("click", ".bu_copy", function () {
     var bus_id = $(this).attr("name");  //获取复制业务流的id
     $.post("/business_list/", {"action": "复制业务流", "bus_id": bus_id}, function (date) {
        $(".right").empty();
        $(".right").append(date);
    })
});


//调试业务流
$(document).on("click", ".dbg_bus", function () {
    var dbg_id = $(this).attr("name");
    var msg = confirm("请确认开打调试客户端");
    if (msg == true) {
        $.post("/business_list/", {"action": "调试业务流", "dbg_id": dbg_id}, function (date) {
            alert(date)
        })
    }
});

//点击业务流名显示详细信息
$(document).on("click", ".bus_detail", function () {
    var bus_id = $(this).attr("name");//获取业务流的id
    $.post("/business_list/", {"bus_id": bus_id,  "action": "查看业务流详细信息"}, function (date) {
         $(".right").empty();
         $(".right").append(date);
    })
});

/*------------------------------------add_business.html--------------------------------------------*/
//添加用例
$(document).on("click", "#bus_add_case", function () {
    $(".mask").show();
    showDialog();
    $(".checkbox_case").attr("checked", false)
    $("#bus_addcase_div").show();
    $("#judge_bus").val("choose_again");
});


//添加用例--应用按钮
$(document).on("click", "#bus_tj_case", function () {
    var check_list = $(".checkbox_case:checked");
    if (check_list.length == false){
        alert("请勾选要应用的用例")
    }
    else {
        var caseid_list = [];
        var incaseid_list = [];
        for (i = 0; i < check_list.length; i++) {
            var id=check_list.eq(i).attr("name");
            case_type=check_list.eq(i).parent().parent().children().eq(5).text();
            //alert(case_type);
            if(case_type=="Web用例")
                caseid_list.push(id);
            else if(case_type=="接口用例")
                incaseid_list.push(id);
        }
        $.post("/add_business/", {"action": "添加用例", "caseid_list": caseid_list ,"incaseid_list": incaseid_list}, function (date) {
            $(".tablelist table tbody").eq(1).append(date)
        });
        $("#bus_addcase_div").hide();
        $(".mask").hide();
    }
});

//添加用例--取消按钮
$(document).on("click", "#gb_addcase_div", function () {
    var judge=$("#judge_bus").val();
    var pro_name=$("#current_pro_name").text();

    if(judge=="choose_again"){
        $("#bus_addcase_div").hide();
        $(".mask").hide();
    }
    if(judge=="choose_first"){
        $.post("/business_list/", {"action": "页面跳转", redirect: pro_name}, function (date) {
            $(".right").empty();
            $(".right").append(date);
        })
    }
});


//业务流--删除用例
$(document).on("click", "#bus_del_case", function () {
    $(this).parent().parent().remove();
});


//保存业务流
$(document).on("click", "#bus_save_case", function () {
    var bus_name = $(".search input").eq(0).val();
    var judge_case=$("#judge_case").val();
    var judge_id=$("#judge_id").val();
    if (bus_name == "" || bus_name == null) {
        alert("请输入业务流名称");
    }
    else {
        $("#form_business").ajaxSubmit(function (date) {
            alert(date)
            if (date == "保存成功") {
                var pro_name = $("#current_pro_name").text();
                if(judge_case=="2"){
                        $.post("/business_list/", {"action": "页面跳转", redirect: pro_name}, function (date) {
                        $(".right").empty();
                        $(".right").append(date);
                    })
                }
                else if(judge_case=="1"){
                        $.post("/add_perform/", {"action": "维护执行", "per_id": judge_id}, function (date) {
                        $(".right").empty();
                        $(".right").append(date);
                    })
                }
            }
        });
        return false
    }
});

/*------------------------------------InterfaceParamManager.html--------------------------------------------*/
//删除模板
$(document).on("click", "#del_template", function () {

    var msg = confirm("确认删除吗?");
    if (msg == true) {
        $(this).parent().parent().remove();
        var tmp_id = $(this).attr("name");//获取删除项目的id
        $.post('/interfaceParamManager/', {"tmp_id": tmp_id, "action": "删除模板"}, function (date) {
            alert(date);
            if (date == "删除成功") {

                $.get("/interfaceParamManager/", function (date) {
                    $(".right").empty();
                    $(".right").append(date);
                })
            }
        })
    }
});


//新增json模板
$(document).on("click", "#add_json", function () {
    //获取当前项目名称
    var pro_name=$(this).attr("name");
    $.post("/add_template/", {"action": "新增json模版","pro_name":pro_name}, function (date) {
        $(".right").empty();
        $(".right").append(date);
        $("#content_tr").append("<tr>"+
        "<td style='display:none'> <input type='checkbox' class='checkbox'> </td>"+
        "<td> 1 </td>"+
        "<td> <input type='text' name='objname'> </td>"+
        "<input type='hidden' name='part' value=''>"+
        "<td> <input type='text' name='list'> </td>"+
        "<td> <input type='text' name='key'> </td>"+
        "<td> <select name='type'> <option></option> <option value='发送报文'>发送报文</option> <option value='响应报文'>响应报文</option> </select> </td>"+
        "<td id='operation'> <input type='button' class='add_content'  title='新增字段'> <input type='button' class='del_content'  title='删除字段'></td>"+
        "</tr>");
    })
})


//新增jms模板
$(document).on("click", "#add_jms", function () {
    var pro_name=$(this).attr("name");
    $.post("/add_template/", {"action": "新增jms模版","pro_name":pro_name}, function (date) {
        $(".right").empty();
        $(".right").append(date);
        $("#content_tr").append("<tr>"+
        "<td style='display:none'> <input type='checkbox' class='checkbox'> </td>"+
        "<td> 1 </td>"+
        "<td> <input type='text' name='objname'> </td>"+
        "<td> <select name='part' required> <option></option> <option value='报文头'>报文头</option> <option value='报文头'>报文体</option> </select> </td>"+
        "<input type='hidden' name='part' value=''>"+
        "<td> <input type='text' name='list'> </td>"+
        "<td> <input type='text' name='key'> </td>"+
        "<td> <select name='type'> <option></option> <option value='发送报文'>发送报文</option> <option value='响应报文'>响应报文</option> </select> </td>"+
        "<td id='operation'> <input type='button' class='add_content'  title='新增字段'> <input type='button' class='del_content'  title='删除字段'></td>"+
        "</tr>");
    })
});


//编辑模板
$(document).on("click", "#mdy_tmp", function () {
    var pro_name=$(this).attr("pro_name");
    var tempplate_id = $(this).attr("name");
    var tmp_type = $(this).attr("tmp_type");
    $.post("/add_template/", {"temp_id": tempplate_id, "tmp_type": tmp_type, "action": "编辑模板","pro_name":pro_name}, function (date) {
        $(".right").empty();
        $(".right").append(date);
    })
});

//复制模板
$(document).on("click", ".copy_template", function () {
     var template_id = $(this).attr("name");  //获取复制模板的ID
     var pro_name=$(this).attr("pro_name");
     var tmp_type = $(this).attr("tmp_type");
     $.post("/add_template/", {"action": "复制接口模板", "temp_id": template_id,"tmp_type": tmp_type, "pro_name":pro_name}, function (date) {
        $(".right").empty();
        $(".right").append(date)
    })
});


//用模板直接创建用例
$(document).on("click", ".create_case", function () {
    //获取模板ID
    var temp_id = $(this).attr("name");
    var pro_name = $("#current_project").text();
    $.post("/add_inter_face/", {"action": "新增接口用例", redirect: pro_name}, function (date) {
        $(".right").empty();
        $(".right").append(date);
        $("#judge_case").val("0");//3表示从接口模板管理进入
        $("#judge_id").val(temp_id);
        $.post("/add_interface_ajax/", {tmp_id: temp_id}, function (date) {
            $("#template_id").val(temp_id);
            $("#table_div").empty();
            $("#table_div").append(date)
        })
    })
});


/*------------------------------------template_manage.html--------------------------------------------*/
//导入模板按钮
$(document).on("click", "#imp_tmp_btn", function () {
    var temp_type = $(this).attr("name");
    //根据倒入按钮的name属性来显示不同的div
    if (temp_type == "JSON" || temp_type == "编辑JSON") {
        $(".mask").show();
        showDialog();
        $(".checkbox-json").attr("checked", false);
        $("#import_json").show();
    }
    if (temp_type == "JMS" || temp_type == "编辑JMS") {
        $(".mask").show();
        showDialog();
        $(".checkbox-json").attr("checked", false);
        $("#import_jms").show();
    }
});


//新增JSON模板--导入模板Div--应用按钮
$(document).on("click", "#yy_json", function () {

    var get_id = $(this).attr("name");
    $.post("/add_template_ajax/", {tmp_id: get_id}, function (date) {
        $("#content_tr:last").append(date);
    })
    $(".checkbox-json").attr("checked", false);
    $(".mask").hide();
    $("#import_json").hide();

});


//新增JSON模板--导入模板Div--取消按钮
$(document).on("click", "#gb_json", function () {
    $(".checkbox-json").attr("checked", false);
    $(".mask").hide();
    $("#import_json").hide();
})


//新增字段
$(document).on("click", ".add_content", function () {
    //获取当前的字段序号
    var index=$(this).parent().parent().index();
    var template_type = $("#template_type").val();
    if (template_type == "JSON" || template_type == "编辑JSON") {
        //$("#content_tr:last").append(date)
        $("#content_tr tr").eq(index).after("<tr>"+
        "<td style='display:none'> <input type='checkbox' class='checkbox'> </td>"+
        "<td> <a></a> </td>"+
        "<td> <input type='text' name='objname'> </td>"+
        "<input type='hidden' name='part' value=''>"+
        "<td> <input type='text' name='list'> </td>"+
        "<td> <input type='text' name='key'> </td>"+
        "<td> <select name='type'> <option></option> <option value='发送报文'>发送报文</option> <option value='响应报文'>响应报文</option> </select> </td>"+
        "<td id='operation'> <input type='button' class='add_content'  title='新增字段'> <input type='button' class='del_content'  title='删除字段'></td>"+
        "</tr>");
    }
    if (template_type == "JMS" || template_type == "编辑JMS") {

        //$("#content_tr:last").append(date)
         $("#content_tr tr").eq(index).after("<tr>"+
        "<td style='display:none'> <input type='checkbox' class='checkbox'> </td>"+
        "<td> <a></a> </td>"+
        "<td> <input type='text' name='objname'> </td>"+
        "<td> <select name='part' required> <option></option> <option value='报文头'>报文头</option> <option value='报文头'>报文体</option> </select> </td>"+
        "<input type='hidden' name='part' value=''>"+
        "<td> <input type='text' name='list'> </td>"+
        "<td> <input type='text' name='key'> </td>"+
        "<td> <select name='type'> <option></option> <option value='发送报文'>发送报文</option> <option value='响应报文'>响应报文</option> </select> </td>"+
        "<td id='operation'> <input type='button' class='add_content'  title='新增字段'> <input type='button' class='del_content'  title='删除字段'></td>"+
        "</tr>");
    }

    //让所有步骤的序列号依次排序
    var checkbox_list = $(".checkbox");
    for(i in checkbox_list)
        checkbox_list.eq(i).parent().next().text(parseInt(i)+1);
});

//删除字段
$(document).on("click", ".del_content", function () {
    //获取当前的字段个数：如果只剩下一个字段，则不能被删除
    var $elements = $('.del_content');
    var len = $elements.length;
    if(len == 1)
        alert("该步骤不能被删除");
    else
        $(this).parent().parent().remove();

    //让所有步骤的序列号依次排序
    var checkbox_list = $(".checkbox");
    for(i in checkbox_list)
        checkbox_list.eq(i).parent().next().text(parseInt(i)+1);
})

//排序
//$(document).on("click", "#sort", function () {
//    var checkbox_list = $(".checkbox");
//    for (i = 0; i < checkbox_list.length; i++) {
//        checkbox_list.eq(i).parent().next().text(i + 1)
//    }
//})

//保存模板
$(document).on("click", "#save_template", function () {
    //获取项目名称
    var pro_name=$("#project_name").val();
    //获取模板名称
    var temp_name = $("#template_name").val();
    if (temp_name == false) {
        alert("必须填写模板名称")
    }
    else {
        $("#save_temp").ajaxSubmit(function (date) {
            alert(date);
            if (date == "保存成功") {
                $.post("/interfaceParamManager/", {"action": "页面跳转", redirect: pro_name}, function (date) {
                    $(".right").empty();
                    $(".right").append(date);
                })
            }
        });
        return false
    }
});


//新增JMS模板--导入模板div--应用
$(document).on("click", "#yy_jms", function () {
    var check_list = $(".checkbox-jms:checked");
    if (check_list.length != 1) {
        alert("只能倒入一个模板");
    }
    else {
        var get_id = check_list.attr("name");
        $.post("/add_template_ajax/", {tmp_id: get_id}, function (date) {
            $("#content_tr:last").append(date);
        });

        $(".checkbox-jms").attr("checked", false);
        $(".mask").hide();
        $("#import_jms").hide();
    }
});


//新增JMS模板--导入模板div--取消
$(document).on("click", "#gb_jms", function () {
    $(".checkbox-jms").attr("checked", false);
    $(".mask").hide();
    $("#import_jms").hide();
});


/*------------------------------------project_management.html--------------------------------------------*/
//新增项目
$(document).on("click", "#add_pro_btn", function () {
    $.post("/add_project/", {"action": "页面跳转"}, function (date) {
        $(".right").empty();
        $(".right").append(date)
    })
});


//新增/编辑项目-添加该项目的数据库信息
$(document).on("click",".add_database",function(){
      $("#add_DB").append(
        "<tr>"+
        "<td><input  name='db_name' type='text' value='' required autofocus></td>"+
        "<td><input  name='db_address' type='text' value='' required autofocus></td>"+
        "<td><input  name='db_port' type='text' value='' required autofocus></td>"+
        "<td><input  name='db_connecttype' type='text' value='' required autofocus></td>"+
        "<td><input  name='db_connectdata' type='text' value='' required autofocus></td>"+
        "<td><input  name='db_username' type='text' value='' required autofocus></td>"+
        "<td><input  name='db_password' type='text' value='' required autofocus></td>"+
        "<td> <select name='db_status' ><option value='True'>True</option><option value='False'>False</option></select> </td>"+
        "<td><input class='sc_db' type='button'  title='删除'></td>"+
        "</tr>"
    );
});


//新增/编辑项目-删除该项目的数据库信息
$(document).on("click",".sc_db",function(){
    $(this).parent().parent().remove();
});


//新增/编辑项目-添加/修改成员按钮
$(document).on("click",".addmember",function(){
    showDialog();
    $(".moremember_dialog").show();
    // 获取现有项目人员
    name_str = $(".memberlist").text();
    // 获取所有人员对象,通过chebox遍历value值
    check_list = $(".checkbox2").valueOf();

    //遍历人员是否包含在享有项目人员中,如果包含且没勾选就勾选上
    for (i = 0; i < check_list.length; i++) {
        // 先取消所有勾选，再通过对比勾选所需
        check_list[i].checked = false;
        var check_val = check_list[i].value;
        if (name_str.indexOf(check_val) >= 0) {
            if (check_list[i].checked == false) {
                check_list[i].click();
            }
        }
    }
});


//添加&修改项目人员--保存人员信息
$(document).on("click",".member_save",function(){
    var checkbox2 = $(".checkbox2");
    var user = $(".memberlist");
    user.html("");
    var value = new Array();
    var num = 0;
    for (var i = 0; i < checkbox2.length; i++) {
        if (checkbox2[i].checked == true) {
            value[num] = $(".checkbox2").eq(i).parent().siblings('.user').html();
            num++;
        }
    }
    user.html(value.join("，"));
    $(".moremember_dialog").hide();
});


//添加&修改项目人员--取消
$(document).on("click",".member_cancel",function(){
    $(".moremember_dialog").hide();
});


//新增项目--保存
$(document).on("click", "#save_pro", function () {
    //获取项目基本信息
    var pro_name = $("#add_pro").val();
    var user_name = $("#add_cy").text();
    if(!pro_name){
        alert("项目名称不能为空");
    }
    else if(user_name=="" || user_name==null) {
        alert("请至少添加一名成员");
    }
    else{
        $("#form_project").ajaxSubmit(function (date) {
            alert(date);
            if (date == "保存成功") {
                $.get("/project_management/", function (date) {
                    $(".right").empty();
                    $(".right").append(date);
                })
            }
        })
    }
});


//维护项目
$(document).on("click", "#modify_pro_btn", function () {
    var pro_id = $(this).attr("name");//获取维护项目的id
    $.post("/project_management/", {"action": "编辑项目", "pro_id": pro_id}, function (date) {
        $(".right").empty();
        $(".right").append(date)
    })
});


//删除项目
$(document).on("click", "#del_project", function () {
    var msg = confirm("确认删除吗?");
    if (msg == true) {
        var pro_id = $(this).attr("name");  //获取删除项目的id
        $.post("/project_management/", {"pro_id": pro_id, action: "删除项目"}, function (date) {
            alert(date);
            if (date == "删除成功") {
                $.get("/project_management/", function (date) {
                    $(".right").empty();
                    $(".right").append(date);
                })
            }
        })
    }
});


//点击项目名称查看详细信息
$(document).on("click", ".pro_detail", function () {
    var pro_id = $(this).attr("name");//获取项目的id
    $.post("/project_management/", {"pro_id": pro_id, action: "查看项目详细信息"}, function (date) {
         $(".right").empty();
         $(".right").append(date);
    })
})

/*------------------------------------user_management.html--------------------------------------------*/
//新增用户
$(document).on("click","#btn_add_user", function () {
    $(".mask").show();
    showDialog();
    $(".user_dialog").show();
});


//新增用户--保存
$(document).on("click", "#save", function () {
    var add_user = $("#add_user").val();
    var first_name = $("#first_name").val();
    var password = $("#password").val();
    var chest = '';
    var status = document.getElementsByName("radiobutton");
    for (i = 0; i < status.length; i++) {
        if (status[i].checked == true) {
            chest += status[i].value
        }
    }
    if(add_user==false || first_name==false || password==false){
        alert("全部都要填写")
    }
    else{
        $.post("/user_management/", {
            add_user: add_user,
            first_name: first_name,
            password: password,
            chest: chest,
            action: "新增用户"
        }, function (date) {
            alert(date);
            if (date == "保存成功") {
                $.get("/user_management/", function (date) {
                    $(".right").empty();
                    $(".right").append(date);
                })
            }
        })
    }
});


//新增用户--取消
$(document).on("click","#cencel_adduser", function () {
    $(".user_dialog").hide();
    $(".mask").hide();
});


//维护用户
$(document).on("click",".wh_user", function () {
    $(".mask").show();
    showDialog();
    $(".changeuser_dialog").show();
});


//维护用户信息--取消
$(document).on("click","#cencel_changeuser", function () {
    $(".changeuser_dialog").hide();
    $(".mask").hide();
});


//维护用户信息
$(document).on("click", ".wh_user", function () {

    var userid = $(this).attr("name"); //获取该用户的id
    var username = $(this).parents("tr").find("[class='username']").text(); //获取用户名
    var name = $(this).parents("tr").find("[class='name']").text(); //获取用户realname
    var status = $(this).parents("tr").find("[class='isactive']").text(); //获取用户状态
    $("#user_id").val(userid);
    $("#user_name").val(username);
    $("#user_first_name").val(name);

    if(status == "True") {
        $("input[name='radiobutton2']").eq(0).attr("checked", true);
    }
    if(status == "False"){
        $("input[name='radiobutton2']").eq(1).attr("checked", true);
    }

    $(".mask").show();
    showDialog();
    $(".changeuser_dialog").show();
});


//维护用户信息--保存
$(document).on("click", "#save_xg", function () {
    var id = $("#user_id").val();
    var name = $("#user_name").val();
    var first_name = $("#user_first_name").val();
    var password = $("#user_password").val();

    var username = document.getElementById("username").innerHTML;
    var chest = "";
    var status = document.getElementsByName("radiobutton2");

    for (i = 0; i < status.length; i++) {
        if (status[i].checked == true) {
            chest += status[i].value
        }
    }
    if(!name || !first_name){
        alert("请填写所有信息")
    }
    else{
        $.post("/user_management/", {
            id:id,
            name: name,
            first_name: first_name,
            password:password,
            chest: chest,
            action: "维护用户",
            username:username
        }, function (date) {
            alert(date);
            if (date == "保存成功") {
                $.get("/user_management/", function (date) {
                    $(".right").empty();
                    $(".right").append(date);
                })
            }
            else if(date == "保存成功，用户需要重新登录"){
               location.href = "http://172.16.6.136:8000/";
            }
        })
    }
});


//删除用户信息
$(document).on("click", ".sc_user", function () {
    var msg = confirm("确认删除吗?");
    if (msg == true) {
        var user_id = $(this).attr("name"); //获取该用户的id
        $.post("/user_management/", {"action": "删除用户", "user_id": user_id}, function (date) {
            alert(date);
            if (date == "删除成功") {
                $.get("/user_management/", function (date) {
                    $(".right").empty();
                    $(".right").append(date);
                })
            }
        })
    }
});


//重置密码
$(document).on("click",".cz_user", function () {
    var user_name = $(this).attr("name");
    $("#modify_user").val(user_name);
    $(".mask").show();
    showDialog();
    $(".changepwd_dialog").show();
});


//重置密码--确定
$(document).on("click","#modify_password", function () {
    $("#myd_pass").ajaxSubmit(function (date) {
        alert(date);
        if(date == "修改成功"){
            $.get("/user_management/", function (date) {
                $(".right").empty();
                $(".right").append(date);
            })
        }
    });
    return false
});


//重置密码--取消
$(document).on("click","#gb_mdypass",function(){
    $(".changepwd_dialog").hide();
    $(".mask").hide();
});









