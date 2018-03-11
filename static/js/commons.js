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
                    // $("#image").attr("src","");
                    $(ths).parent().prev().empty().html("<span style='color: coral;'>上传成功,请刷新页面</span>");
                },
                error:function(arg) {

                    console.log(arg);
                    console.log("aaaaaaaaaaaaaaaaa");
                    $(ths).parent().prev().empty().html("<span style='color: red;'>上传失败,请重试</span>");
                    // console.log(arg.responseText);
                }
           })
        }

function replace_em(str){
            str = str.replace(/\</g,'<;');
            str = str.replace(/\>/g,'>;');
            str = str.replace(/\n/g,'<;br/>;');
            str = str.replace(/\[em_([0-9]*)\]/g,'<img src="/static/img/face/$1.gif" border="0" />');
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

function PreviewMultipleFile(ths){
			 var reader = new FileReader();

             reader.onload = function (e) {
                // get loaded data and render thumbnail.
                $("#image").attr('src',e.target.result);
             };

            // read the image file as a data URL.
            reader.readAsDataURL(ths.files[0]);

            $("#addImage").before($("#addImage").clone());

		}

function PostMessage(ths) {
		    var weibo_info = {};

		    var text = $(".post>textarea").val();
		    var post_status = $(".c6 i").text();
		    if(post_status == "公开"){
		        var the_perm = 0;
		    }else if(post_status == "仅自己可见"){
		        var the_perm = 1;
		    }else{
		        var the_perm = 2;
		    }
            var perm = the_perm;
		    var wb_type = 0;
		    var user_id = $(".commentPlace button").attr("target");

		    weibo_info["text"] = text;
            weibo_info["user_id"] = user_id;
            weibo_info["wb_type"] = wb_type;
            weibo_info["perm"] = perm;

            weibo_data = JSON.stringify(weibo_info);

		    $.ajax({
		        url: "/post_weibo/",
		        type: "POST",
		        data: {"weibo_data":weibo_data},
                success:function(arg) {
                    if(arg=="right"){
                        location.href = ("/index/");
                    }
                    console.log(arg);
                },
                error:function(arg) {
                  console.log("error");
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
            $(ths).parent().prev().text(current_status);
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
