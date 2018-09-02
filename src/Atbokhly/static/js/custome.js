$(window).load(function(){
    /*============================*/
        //customize the navbar
    /*============================*/
    $("#toggle_btn").click(function(){
        var nav_left = $('nav').css("right");
        if (nav_left == "0px"){
            $("nav").css({
                right: "-250px"
            });
            $("#form_arrow").attr('class', 'fa fa-arrow-circle-left');
        } else {
            $("nav").css({
                right: "0px"
            });
            $("#form_arrow").attr('class', 'fa fa-arrow-circle-right');
        }

    });

    /*============================*/
        //preloader
    /*============================*/
    $(".preloader").fadeOut(100,function(){
        $("body").css({
            overflow: 'auto'
        });
        $(this).remove();
    }); 
});

$(document).ready(function(){

    $('#id_date_birth').attr('type','date');
    $('#id_phone').attr('autocomplete','off');

    /*============================*/
        //register function
    /*============================*/
    $('.custom-checkbox input').click(function(){
        console.log(this.value);
        if(this.value == 'cheif'){
            $('#id_cv').fadeIn(200);
            $('#id_cv').attr('required', 'required');
        } else{
            $('#id_cv').fadeOut(200);
            $('#id_cv').removeAttr("required");
        }
    });

    /*============================*/
        //rate function
    /*============================*/
    $(".in").click(function(){
        var rate = $(this).val();
        console.log(rate);
//        $(".info").html(rate);
        var form = $(this).closest(".rating");
        if(rate <= 5){
            $.ajax({

                url: form.attr("first_redirect"),
                data: {
                  'rating': rate
                },
                success: function (data) {
                    alert("rated successfully ^_^");
                    console.log(data);
                    $('#user_rate').remove();
                    $('.rate .container').append('<p id="user_rate"><span id="user_rate">تقييمك للوجبه <i class="fa fa-arrow-left"></i> </span>'+data.user_rate+'</p>');
//                    window.location = form.attr("second_redirect");
                    $('#meal_rate').html('<span>التقييم</span><i class="fa fa-star fa-lg"></i>'+data.meal_rate);
                }
            });
        } else{
            alert("please choose a right rate value");
        }
    });

    /*============================*/
        //validate update account function
    /*============================
    $('.update_form').submit(function(){
        var email = $('#id_email').val();
        var form = $(this);
        //alert(form);
        //alert(form.attr("first_redirect"));
        $.ajax({
            url: form.attr("first_redirect"),
            data: {
              'email': email
            },
            success: function (data) {
                if(data.response == 'true'){
                    //alert(data.old_email);
                    //$('#id_email').val(data.old_email);
                    $('.email_error').html('<div class="col-xs-12 alert alert-danger"><a class="close" href="#" data-dismiss="alert">×</a><strong>this email already exist</strong></div><label>Email Address:</label><input type="email" name="email" value="'+email+'" required="" maxlength="100" id="id_email">');
                    return false;
                }
                else{
                    form.removeAttr('onsubmit');
                    $("#submit").click();
                    window.location = form.attr("second_redirect");
                    window.location = "/Home/chief";
                }
            }
        });
    });
    /*============================*/
        //user like function
    /*============================*/
    $(".like").click(function(){
        var like = $(this).val();
        console.log(like);
        var form = $(this).closest(".likeFun");
        $.ajax({
            url: form.attr("first_redirect"),
            data: {
              'like': like
            },
            success: function (data) {
                console.log(data.data);
                if(data.data == 'true'){
                    $('.ff').attr('class', 'fa fa-thumbs-up ff liked');
                    $('.arrow').css('display','none');
                } else{
                    $('.ff').attr('class', 'fa fa-thumbs-up ff');
                    $('.arrow').css('display','block');
                }
            }
        });
        if($(this).val() == 'true'){
            $(this).val(false);
        }else{
            $(this).val(true);
        }
    });


    /*============================*/
        //delete transaction function
    /*============================*/
    $(".delete_trans").click(function(){
        var block = "#"+this.id.slice(0,-1);
        var form = $(this).closest(".delFun");
        $.ajax({
            url: form.attr("first_redirect"),
            success: function (data) {
                $(block).remove();
            }
        });
    });
    /*============================*/
        //clear transactions function
    /*============================*/
    $('#clear').click(function(){
        $('.clear_confirm').fadeIn(300);
    });
    $('#form_close_btn').click(function(){
        $('.clear_confirm').fadeOut(300);
    });
    $('#close_form').click(function(){
        $('.clear_confirm').fadeOut(300);
    });
    $("#clear_all").click(function(){
        var form = $(this).closest(".clear_form");
        $.ajax({
            url: form.attr("first_redirect"),
            success: function (data) {
                $('.clear_confirm').fadeOut(300);
                $('.transaction').remove();
//                $('#clear').remove();
            }
        });
    });
    /*============================*/
        //delete confiirmation
    /*============================*/
    $("#delete").click(function(){
        $(".delete").css('display','block');
    });
    $("#close").click(function(){
        $(".delete").css('display','none');
    });
    
    /*============================*/
        //nicescroll
    /*============================*/
    /*$("html").niceScroll({
        cursorborder: '1px solid #eee',
        cursorspeed: '80',
        mousescrollstep: '40',
        cursorcolor:"#1B435D",
        cursorwidth:"10px",
        zindex: '999999'
    });
    */
    $(".meals_imgs").niceScroll({
        cursorborder: '1px solid #eee',
        cursorspeed: '80',
        mousescrollstep: '40',
        cursorcolor:"#1B435D",
        cursorwidth:"10px"
    });
    $("textarea").niceScroll({
        cursorborder: 'none',
        cursorspeed: '80',
        mousescrollstep: '40',
        cursorcolor:"#1B435D",
        cursorwidth:"10px",
        cursorborderradius: '0px',
        railalign: 'left',
    });

    $("nav").niceScroll({
        cursorborder: '1px solid #eee',
        cursorspeed: '80',
        mousescrollstep: '40',
        cursorcolor:"#1B435D",
        cursorwidth:"10px"
    });

    $('.sellect-origin-list').niceScroll({
        cursorborder: '2px solid #eee',
        cursorspeed: '80',
        mousescrollstep: '40',
        cursorcolor:"#1B435D",
        cursorwidth:"10px"
    });
    $('.meal_ing').niceScroll({
        cursorborder: 'none',
        cursorspeed: '80',
        mousescrollstep: '40',
        cursorcolor:"#1B435D",
        cursorwidth:"10px",
        cursorborderradius: '0px'
    });
    

    /*============================*/
        //manage signing forms
    /*============================*/
    
    $('#sign').click(function(){
        var x = $('.signingForm').css("display");
        if (x == "none"){
            $('.signingForm').css({
                display: 'block'
            });
        } else{
            $('.signingForm').css({
                display: 'none'
            });
        }
        
    });
    
    $('#login').click(function(){
        $("#signupform").css({
            display: 'none'
        });
        
        $('#loginform').css({
            display: 'block'
        });
    });
    
    $('#signup').click(function(){
        $("#signupform").css({
            display: 'block'
        });
        
        $('#loginform').css({
            display: 'none'
        });
    });
    
    /*============================*/
        //navbar-fixed action
    /*============================*/
    $(window).on('scroll',function(){
        var cur_pos = $(this).scrollTop();
        if (cur_pos >200){
            $('.scroll_up').fadeIn(500);
        } else{
            $('.scroll_up').fadeOut(500);
        }
    });
    
    /*=====================================================*/
        //change classes for active and inactive filters
    /*=====================================================*/
    
    $('.filters li').click(function(){
        var ulist = $('.filters');
        ulist.find('li').removeClass('active');
        $(this).addClass('active');
    });
    
    /*=====================================================*/
        //اhandle the fancybox
    /*=====================================================*/
    $("[data-fancybox]").fancybox({
        loop : true,
        buttons : [
            'slideShow',
            'fullScreen',
            'thumbs',
            //'share',
            'download',
            'zoom',
            'close'
        ],
        transitionEffect : "slide",
        transitionDuration : 1000,
        animationEffect : "zoom-in-out",
    });
    
    /*===============================*/
        //initialze swipper
    /*===============================*/
    var mySwiper = new Swiper ('.swiper-container', {
        // Optional parameters
        speed: 400,
        direction: 'horizontal',
        loop: true,

        // If we need pagination
        pagination: {
            el: '.swiper-pagination',
            type: 'bullets',
            clickable: true
        },
        autoplay: {
            delay: 2000,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        
      });
    
    var mySwiper1 = new Swiper ('.swiper-container-2', {
        slidesPerView: 6,
        spaceBetween: 100,
        loop: true,
        autoplay: {
            delay: 2000,
        },
        // Responsive breakpoints
        breakpoints: {
          1024: {
            slidesPerView: 4,
            spaceBetween: 40,
          },
          768: {
            slidesPerView: 3,
            spaceBetween: 30,
          },
          640: {
            slidesPerView: 2,
            spaceBetween: 20,
          },
          480: {
            slidesPerView: 1,
            spaceBetween: 15,
          },
          320: {
            slidesPerView: 1,
            spaceBetween: 10,
          }
        }
      });
    
    /*========================================*/
        //manage scroll top and counter 
    /*========================================*/
    
    $('.scroll_up').click(function(){
        $('html, body').animate({
            scrollTop: '0px',
        }, 1000,"swing");
    });
});
