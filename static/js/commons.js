function info_change(ths) {
$(ths).parent().nextAll().children("input").each(function() {
if($(this).attr("name")=="age"||
    $(this).attr("name")=="brief"||
        $(this).attr("name")=="password"||
            $(this).attr("name")=="sex"){
    $(this).prop("disabled",false);//.removeAttr("disabled");//
}
});
}

function info_save(ths) {
//1.先完成信息的正确显示
//2.获取用户修改过后的 简介,密码,性别(对于头像的修改借助一个模态对话框)
//3.借助ajax发送到后台,通过post方法完成对于数据库相关信息的修改
//4.返回修改后的状态,
//  if正确的话,
//      则将修改状态再次为不可修改并将修改后的信息填充到原来的value
//  else:
//      alert("修改失败,请检查网络等")
var user_update_info = {};
$(ths).parent().nextAll().children("input").each(function() {

if($(this).attr("name")=="brief"){
    var brief = $(this).val();
    user_update_info["brief"] = brief;
}else if($(this).attr("name")=="password"){
    var password = $(this).val();
    user_update_info["password"] = password;
}else if($(this).attr("name")=="sex"){
    var sex = $(this).val();
    user_update_info["sex"] = sex;
}else if($(this).attr("name")=="age"){
    var age = $(this).val();
    user_update_info["age"] = age;
}
});
user_update_info = JSON.stringify(user_update_info);
$.ajax({
url: "/user_profile/",
type: "POST",
data: {"user_update_info":user_update_info},
dataType: "json",
success:function(arg) {
    if(arg.status){
        //当更改状态成功的时候,会刷新页面,并显示改变的结果
        $(".info_group").empty().html("<span style='color: coral;'>信息修改成功,即将刷新页面</span>");
        setTimeout(function() {
            location.href = "/user_profile/";
        },2000);

    }else{
        console.log("error");
    }
}
})
}

function submitMyHeadImg(ths){
    // console.log("----------------------");
    // console.log($("#upload_file")[0]);//表示这种里面实际上提交的是一个完整的form表单
    // console.log("----------------------");
    // var fileobj = $("#files")[0].files[0];
    // console.log(fileobj);
    // console.log("----------------------");
   $.ajax({
        url: "/upload_file/",
        type:"POST",
        cache:false,
        //与传统的提交不同,这里提交的是一种表单数据
        data:new FormData($("#upload_file")[0]),
        // dataType: "json",
        processData: false,
        contentType: false,
        success:function(arg) {
            console.log(arg);
            $(ths).parent().prev().empty().html("<span style='color: coral;'>上传成功,请刷新页面</span>");
        },
        error:function(arg) {
            console.log(arg);
            $(ths).parent().prev().empty().html("<span style='color: red;'>上传失败,请重试</span>");
        }
   })
}

function replace_em(str){
    str = str.replace(/\[expression_([0-9]*)\]/g,'<img src="/static/img/face/$1.gif" border="0" />');
    str = str.replace('/<br>/g', '\r\n');
    return str;
}

function ToggleCommentArea(ths) {

  nid = $(ths).attr("target");
  console.log(nid);

  $.ajax({
    // async :false,
    url: "/comment/",
    type: "GET",
    data:{"nid":nid},
    // dataType:"json",
    success:function(arg) {
        $(ths).parent().next().toggleClass("hide");
        console.log("success");
        var data_json = JSON.parse(arg);

        $.each(data_json,function(k,v) {
            console.log(k,v);
            var user__head_img = v['user__head_img'];
            var id = v['id'];
            var comment = v['comment'];
            var p_comment__user_id = v['p_comment__user_id'];
            var date = v['date'];
            var p_comment__user__username = v['p_comment__user__username'];
            var user__username = v['user__username'];


            obj = $(ths).parent().next().find("#commentZone");

            obj.append("<p><img style=\"with:25px;height:25px;float: left;margin:15px 3px 0 3px;\" src="+"/"+user__head_img+"></p>");
            obj.append("<span style='color:coral;'>"+user__username+":"+"</span>");
            obj.append("<span style='color:red;'>"+"@"+p_comment__user__username+"  "+comment+"</span>");
            obj.append("<p>"+date+"</p>");
            obj.append("<hr style='height: 1px;border: none;background-color: #555555;'/>")

        })


        // console.log(obj.prop("class"));

    },
    error:function(arg) {
      console.log("error");
      console.log(arg);
    }

  })
}

function PreviewFile(ths){
     var reader = new FileReader();

     reader.onload = function (e) {
        // get loaded data and render thumbnail.
        $("#image").attr('src',e.target.result);
     };

    // read the image file as a data URL.
    reader.readAsDataURL(ths.files[0]);
}

var i = 1;
function PreviewMultipleFile(ths){
     var reader = new FileReader();
     reader.onload = function (e) {
        // get loaded data and render thumbnail.But we should use the nextTags instead of the direct selector
         $(ths).next().attr('src',e.target.result);
        // $("#image").attr('src',e.target.result);
     };
    // read the image file as a data URL.
    reader.readAsDataURL(ths.files[0]);
    if(i<9){
        temp = $(ths).parent().parent();
        temp.after(temp.clone());//相当于直接对$(".addImage)
    }
    temp.parent().find("h6>span").eq(0).html(i);
    temp.parent().find("h6>span").eq(1).html(9-i);
    i=i+1;
}

function PostMessage(ths) {
    //制造一个装着微博表建立基本信息的字典
    var weibo_info = {};
    //获取微博的文本内容,如果有换行符或者回车换行则转化为<br>进行存储
    var text = $(".post>textarea").val();
    text = text.replace(/\n|\r\n/g,"<br>");
    //获取微博的可查看的权限状态
    var post_status = $(".cStatus i").text();
    if(post_status == "公开"){
        var the_perm = 0;
    }else if(post_status == "仅自己可见"){
        var the_perm = 1;
    }else{
        var the_perm = 2;
    }
    var perm = the_perm;
    //设置微博类型,比如是发布还是转载收藏的
    var wb_type = 0;// 微博类型默认为公开，当然之后允许用户手动去设置
    //获取用户ID，从而确定是哪个用户创建的此微博,这里面暂时有bug，需要被修正
    var user_id = $(".commentPlace button").attr("target");
    console.log("user_id",user_id);

    weibo_info["text"] = text;
    weibo_info["user_id"] = user_id;
    weibo_info["wb_type"] = wb_type;
    weibo_info["permission"] = perm;
    //只要想要发布一个微博,那么上面这四个属性就必须要有才可以使用微博面板这个功能
    weibo_data = JSON.stringify(weibo_info);//字典字符化

    $.ajax({
        // async:false,
        url: "/post_weibo/",
        type: "POST",
        data: {"weibo_data":weibo_data},
        dataType:"json",
        success:function(arg) {
            console.log("right");
            console.log(arg);
            if (arg.status) {
                //在后台返回相应的微博id,以arg.data.id的形式返回// console.log(arg.data.id);
                console.log(arg.message);

                $(".addImages").each(function (k, v) {//这是整个微博最难以实现的功能之一

                    var cur_Img = document.upload_weibo_img[k].weiboImg.files[0];//命名方式非常奇怪
                    var formData = new FormData();
                    formData.append('weibo_id', arg.data.id);//从后台获取的微博的id
                    formData.append('weiboImg', cur_Img);

                    if ($(this).find("#files").val()) {
                        $.ajax({
                            async:false,
                            url: "/upload_weibo_img/",
                            type: "POST",
                            cache: false,//cache设置为false，上传文件不需要缓存。
                            data: formData,
                            // data: new FormData($(".upload_weibo_img")[k]),//在某种程度上等效于$("#afasf")[0]
                            //Ajax的processData设置为false。因为data值是FormData对象，不需要对数据做处理。
                            processData: false,
                            //contentType设置为false。因为是由<form>表单构造的FormData对象，
                            // 且已经声明了属性enctype="mutipart/form-data"，所以这里设置为false。
                            contentType: false,
                            success: function (arg) {
                                //当所有的图片上传成功之后会返回一个微博唯一主键对象
                                var obj = JSON.parse(arg);
                                console.log(obj.message);
                            },
                            error: function (arg) {
                                var obj = JSON.parse(arg);
                                console.log(obj.message);
                            }
                        })
                    }
                });

                location.href = ("/index/");
            }else {
                console.log(arg.message);
            }
        }
    })
}

function setComment(ths) {
    var comment_data = {};
    //制造一个字典 里面有to_weibo,p_comment,user,comment_type,comment,data等相关信息

    var comment = $(ths).prev().val();
    var user_id = $(ths).attr("target");
    var to_weibo_id = $(ths).attr("weibo_id");

    //理论上这个值是@后面的对象 但是目前为了简单 所以采用空值代表评论根对象
    var p_comment_id = "";

    comment_data["comment"] = comment;
    comment_data["user_id"] = user_id;
    comment_data["to_weibo_id"] = to_weibo_id;
    comment_data["p_comment_id"] = p_comment_id;

    comment_data = JSON.stringify(comment_data);

    $.ajax({
        url: "/comment/",
        type: "POST",
        data: {"comment_related_data":comment_data},
        success:function(arg) {

            console.log("success");

            var data_json = JSON.parse(arg);

            obj = $('#commentZone');
            obj.empty();//先删除所有评论里面的内容

            console.log("obj:"+obj);

            $.each(data_json,function(k,v) {
                console.log(k,v);
                var user__head_img = v['user__head_img'];
                var id = v['id'];
                var comment = v['comment'];
                var p_comment__user_id = v['p_comment__user_id'];
                var date = v['date'];
                var p_comment__user__username = v['p_comment__user__username'];
                var user__username = v['user__username'];

                obj.append("<p><img style=\"with:25px;height:25px;float: left;margin:15px 3px 0 3px;\" src="+"/"+user__head_img+"></p>");
                obj.append("<span style='color:coral;'>"+user__username+":"+"</span>");
                obj.append("<span style='color:red;'>"+"@"+p_comment__user__username+"  "+comment+"</span>");
                obj.append("<p>"+date+"</p>");
                obj.append("<hr style='height: 1px;border: none;background-color: #555555;'/>")

            });

            $(ths).prev().val("");

        },
        error:function(arg) {
          console.log("error");
        }
    })
}

function TogglePostStatus(ths) {
    current_status = $(ths).text();
    $(ths).parent().prev().prev().text(current_status);
}

function settime(ths,timer){
    //设置逗留时间
    if(timer == 0){
        $(ths).prop("disabled",false);
        $(ths).html("重新获取验证码");
        return;
    }else {
        $(ths).prop("disabled",true);
        $(ths).html("<i class=\"fa fa-spinner fa-pulse\"></i>已发送("+timer+"s)");
        timer --;
    }
    setTimeout(function() {
            settime(ths,timer);
        },1000);//过1秒执行一次左边的函数
}

function TextStatusDetect(ths) {
    var text = $("#post_text").val();
    // console.log(text.length);
    if(text.trim()){
        $('.cSubmit button').prop("disabled",false).css("background","orangered");
    }else{
        $('.cSubmit button').prop("disabled",true).css("background","coral");
    }
}
