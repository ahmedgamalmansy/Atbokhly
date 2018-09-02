$(document).ready(function(){
    /*============================*/
        //user comment function
    /*============================*/
    $(document).on('click', '.commentFun .submit',function (e) {
        var comment = $('#id_comment').val();
        console.log(comment);
        var form = $(this).closest(".commentFun ");
        if (comment != ""){
            $.ajax({
                url: form.attr("first_redirect"),
                data: {
                  'comment': comment
                },
                success: function (data) {
                    console.log(data.comments);
                    console.log(data.comments[0]);
                    console.log(data.comments[1]);
                    console.log(data.comments[2]);
                    console.log(data.comments[3]);
                    console.log(data.comments[4]);
                    if (data.comments[3]==""){
                        $('.latest_comment').append('<div class="col-xs-12 block">'+
                                                        '<div class="image">'+
                                                            '<img src="/static/images/base_profile_photo.jpg" title="'+data.comments[1]+' '+data.comments[2]+'">'+
                                                        '</div>'+
                                                        '<div class="comm" id="comm_'+data.comments[5]+'">'+
                                                            '<pre>'+data.comments[0]+'</pre>'+
                                                            '<p>now'+
                                                            '<a href="#" class="reply">Reply</a>'+
                                                            '<a href="#" redirect="/meal/'+data.comments[5]+'/like-comment" id="l'+data.comments[5]+'" class="comment_like" value="true">Like</a>'+
                                                            '</p>'+
                                                            '<div class="replys">'+
                                                                '<form onsubmit="return false;" class="col-sm-8 col-sm-push-4 replyFun" method="GET" first_redirect="/meal/'+data.comments[5]+'/reply-comment" id="'+data.comments[5]+'">'+
                                                                '<textarea name="comm" id="id_reply_'+data.comments[5]+'" placeholder="رأيك يهمنا..." class="col-xs-10 col-xs-push-2" autocomplete="off"></textarea>'+
                                                                '<button type="submit" class="col-xs-2 col-xs-pull-10 submit text-center">تعليق</button>'+
                                                                '</form>'+
                                                            '</div>'+
                                                        '</div>'+
                                                    '</div>');
                    } else{
                        $('.latest_comment').append('<div class="col-xs-12 block">'+
                                                        '<div class="image">'+
                                                            '<img src="'+data.comments[3]+'" title="'+data.comments[1]+' '+data.comments[2]+'">'+
                                                        '</div>'+
                                                        '<div class="comm" id="comm_'+data.comments[5]+'">'+
                                                            '<pre>'+data.comments[0]+'</pre>'+
                                                            '<p>now'+
                                                            '<a href="#" class="reply">Reply</a>'+
                                                            '<a href="#" redirect="/meal/'+data.comments[5]+'/like-comment" id="l'+data.comments[5]+'" class="comment_like" value="true">Like</a>'+
                                                            '</p>'+
                                                            '<div class="replys">'+
                                                                '<form onsubmit="return false;" class="col-sm-8 col-sm-push-4 replyFun" method="GET" first_redirect="/meal/'+data.comments[5]+'/reply-comment" id="'+data.comments[5]+'">'+
                                                                '<textarea name="comm" id="id_reply_'+data.comments[5]+'" placeholder="رأيك يهمنا..." class="col-xs-10 col-xs-push-2" autocomplete="off"></textarea>'+
                                                                '<button type="submit" class="col-xs-2 col-xs-pull-10 submit text-center">تعليق</button>'+
                                                                '</form>'+
                                                            '</div>'+
                                                        '</div>'+
                                                    '</div>');
                    }
                }
            });
        } else{
            alert('field is required');
        }
        $('#id_comment').val("");
    });


    /*============================*/
        //user comment function
    /*============================*/
    $(document).on('click', '.replyFun .submit',function (e) {
        var form = $(this).closest(".replyFun ");
        var form_id = form.attr("id");
        var field_id = '#id_reply_'+form_id;
        var container = '#container_'+form_id;
        console.log('the text field id =>'+field_id);
        console.log('the container id =>'+container);
        var comment = $(field_id).val();
        console.log('text => '+comment);
        if (comment != ""){
            $.ajax({
                url: form.attr("first_redirect"),
                data: {
                  'reply': comment
                },
                success: function (data) {
                    if (data.comments[3]==""){
                        $('<div class="col-xs-12 block" style="display: block;">'+
                                '<div class="image">'+
                                    '<img src="/static/images/base_profile_photo.jpg" title="'+data.comments[1]+' '+data.comments[2]+'">'+
                                '</div>'+
                                '<div class="comm">'+
                                    '<pre>'+data.comments[0]+'</pre>'+
                                    '<p>now <a href="#" redirect="/meal/'+data.comments[5]+'/like-reply" id="l'+data.comments[5]+'" class="reply_like" value="true">like</a></p>'+
                                '</div>'+
                            '</div>').insertBefore('#'+form_id);

                    } else{
                        $('<div class="col-xs-12 block" style="display: block;">'+
                                '<div class="image">'+
                                    '<img src="'+data.comments[3]+'" title="'+data.comments[1]+' '+data.comments[2]+'">'+
                                '</div>'+
                                '<div class="comm">'+
                                    '<pre>'+data.comments[0]+'</pre>'+
                                    '<p>now <a href="#" redirect="/meal/'+data.comments[5]+'/like-reply" id="l'+data.comments[5]+'" class="reply_like" value="true">Like</a></p>'+
                                '</div>'+
                            '</div>').insertBefore('#'+form_id);
                    }
                }
            });
        } else{
            alert('field is required');
        }
        $(field_id).val("");
    });


    /*============================*/
        //view reply form
    /*============================*/
    $(document).on('click', '.reply',function (e) {
        e.preventDefault();
        var form = $(this).closest('.comm');
        console.log(form.attr('id'));
        $('#'+form.attr('id')+' .replyFun').fadeIn(500);
        $('#'+form.attr('id')+' .replys .view_replys').fadeOut(250);
        $('#'+form.attr('id')+' .replys .block').fadeIn(500);
    });


    /*============================*/
        //view comment replys
    /*============================*/
    $(document).on('click', '.view_replys',function (e) {
//    $('.view_replys').click(function(e){
        e.preventDefault();
        $(this).fadeOut(250);

        var replys = $(this).closest('.comm');
        $('#'+replys.attr('id')+' .replys .block').fadeIn(500);
        $('#'+replys.attr('id')+' .replyFun').fadeIn(500);

        var height_inc = $('#'+replys.attr('id')+' .replys').height()+$('#'+replys.attr('id')+' .replyFun').height();
        var cur_pos = $(window).scrollTop();
        $(window).scrollTop(cur_pos+height_inc);
    });

    /*============================*/
        //like comment function
    /*============================*/
    $(document).on('click', '.comment_like',function (e) {
//    $(".comment_like").click(function(e){
        e.preventDefault();
        var comm_id = $(this).attr('id').substring(1);
        var like    =  $(this).attr('id');
        console.log(comm_id);
        console.log('like'+like);
        var like_val = $(this).attr('value');
        console.log(like_val);

        console.log($(this).attr("redirect"));

        $.ajax({
            url: $(this).attr("redirect"),
            data: {
              'like': like_val
            },
            success: function (data) {
                console.log(data.data);
                if(data.data == 'true'){
                    console.log($('#'+ like));
                    $('#'+ like).css({
                        //color: '#000'
                        fontWeight: 'bold'
                    });
                } else{
                    console.log($('#'+ like));
                    $('#'+ like).css({
                        //color, '#428bca'
                        fontWeight: 'normal'
                    });
                }
            }
        });
        if($(this).attr('value') == 'true'){
            $(this).attr('value', false);
            $(this).removeClass('sss');
        }else{
            $(this).attr('value', true);
            $(this).addClass('sss');
        }
    });

    /*============================*/
        //like reply function
    /*============================*/
    $(document).on('click', '.reply_like',function (e) {
        e.preventDefault();
        var comm_id = $(this).attr('id').substring(1);
        var like    =  $(this).attr('id');
        var like_val = $(this).attr('value');

//      console.log(like_val);
//      console.log($(this).attr("redirect"));
//      console.log(comm_id);
//      console.log('like'+like);

        $.ajax({
            url: $(this).attr("redirect"),
            data: {
              'like': like_val
            },
            success: function (data) {
                console.log('the like value is => ' +data.data);

                if(data.data === 'true'){
//                    console.log('#'+ like);
                    $('#'+ like).css({
                        fontWeight: 'bold'
                    });
                } else{
                    $('#'+ like).css({
                        fontWeight: 'normal'
                    });
                }
            }
        });
        if($(this).attr('value') == 'true'){
            $(this).attr('value', false);
            $(this).removeClass('sss');
        }else{
            $(this).attr('value', true);
            $(this).addClass('sss');
        }
    });
});