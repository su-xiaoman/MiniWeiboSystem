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

function ToggleLikeStatus(ths){
    var likeStatus = parseInt($(ths).attr("likeStatus"));
    if(likeStatus==0){
        $(ths).css("color","red");
        $(ths).attr("likeStatus",1);
    }else{
        $(ths).css("color","black");
        $(ths).attr("likeStatus",0);
    }



    // var weibo_id = $(ths).attr("weibo_id");

    // $.ajax({
    //     url: "/like/",
    //     type: "GET",
    //     data:{"weibo_id":weibo_id},
    //     dataType:"json",
    //     success:function(arg) {
    //         console.log("likeStatus");
    //         console.log(arg.likeStatus);//likeStatus
    //
    //         if(arg.likeStatus<=0){//如果为0，说明该用户还没有点赞，则
    //             //1.改变点赞标志
    //              $(ths).css("color","red");
    //              $(ths).attr("likestatus",1);
    //              //2.在后台数据库中将此数据加1
    //             //可能需要建立一个数组，从而保证weibo_id也被传送过去
    //             $.ajax({
    //                 url: "/like/",
    //                 type: "POST",
    //                 data:{"status":0},
    //                 success:function (arg) {
    //                     console.log("success变红");
    //                 }
    //             });
    //
    //         }else if(arg.likeStatus>=1){//用户已经点赞了，那么就变成相反的
    //            $(ths).css("color","black");
    //            $(ths).attr("likestatus",0);
    //            //2.在后台数据库中将此数据减1
    //             $.ajax({
    //                 url: "/like/",
    //                 type: "POST",
    //                 data:{"status":1},
    //                 success:function (arg) {
    //                     console.log("success变黑");
    //                 }
    //             });
    //
    //
    //         }else{
    //             console.log("不知道为什么会失败")
    //         }
    //     }
    // });

}

function ToggleCommentArea(ths) {
    //nid代表着微博的编号
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

            // var comment_type = v['comment_type'];

            obj = $(ths).parent().next().find("#commentZone");

            obj.append("<p><img style=\"width:30px;height:30px;float: left;margin:5px 3px 0 3px;\" src="+"/"+user__head_img+"></p>");
            obj.append("<span style='color:coral;'>"+user__username+":"+"</span>");
            obj.append("<span style='color:red;'>"+"@"+p_comment__user__username+"</span> "+"<span style='color: #555555'>"+comment+"</span>");
            obj.append("<p>"+date+"<span style='float: right;margin-right: 40px;'>回复</span>"+"</p>");
            obj.append("<hr style='height: 1px;border: none;background-color:lightgray;'/>")

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
    var post_status = $(".cStatus span").text();
    if(post_status == "公开"){
        var the_perm = 0;
    }else if(post_status == "仅自己可见"){
        var the_perm = 1;
    }else{
        var the_perm = 2;
    }
    var permission = the_perm;
    //设置微博类型,比如是发布还是转载收藏的
    var wb_type = 0;// 微博类型默认为公开，当然之后允许用户手动去设置
    //获取用户ID，从而确定是哪个用户创建的此微博,这里面暂时有bug，需要被修正
    var user_id = $(".commentPlace button").attr("target");

    weibo_info["text"] = text;
    weibo_info["user_id"] = user_id;
    weibo_info["wb_type"] = wb_type;
    weibo_info["permission"] = permission;
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
            // console.log(arg);
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
                            // data: new FormData($(".upload_weibo_img")[k]),//在某种程度上等效于$("#afasf")[0]
                            //Ajax的processData设置为false。因为data值是FormData对象，不需要对数据做处理。
                            //contentType设置为false。因为是由<form>表单构造的FormData对象，
                            // 且已经声明了属性enctype="mutipart/form-data"，所以这里设置为false。
                            async:false,
                            url: "/upload_weibo_img/",
                            type: "POST",
                            cache: false,//cache设置为false，上传文件不需要缓存。
                            data: formData,
                            processData: false,
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

function DeleteMyWeibo(ths) {

    var weibo_data = {};

    var weiboId = $(ths).attr("weibo_id");
    var postMan = $(ths).attr("postman");


    weibo_data["weiboId"] = weiboId;
    weibo_data["postMan"] = postMan;

    weibo_data = JSON.stringify(weibo_data);

    $.ajax({
        url:"/delete/",
        type: "POST",
        data: {"weibo_data":weibo_data},
        dataType:"json",
        success:function (arg) {
            if(arg.status){
                alert(arg.message);
                $(ths).parent().parent().parent().parent().empty();
            }else{
                alert(arg.error);
            }
        }
    })

}

function setComment(ths) {
    var comment_data = {};
    //制造一个字典 里面有to_weibo,p_comment,user,comment_type,comment,data等相关信息

    var comment = $(ths).prev().val();      //从input框中获取的文件内容
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

function TextStatusDetect(ths) {
    var text = $("#post_text").val();
    // console.log(text.length);
    if(text.trim()){
        $('.cSubmit button').prop("disabled",false).css("background","orangered");
    }else{
        $('.cSubmit button').prop("disabled",true).css("background","coral");
    }
}


