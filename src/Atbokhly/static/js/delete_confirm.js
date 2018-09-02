$(document).ready(function(){
    $('.delete').click(function(e){
        e.preventDefault();
        var item_id = $(this).attr('id');
        var confirm_id = "#confirm_delete_"+item_id
        console.log(item_id);
        console.log(confirm_id);
        $(confirm_id).fadeIn(500);
    });

    $('.close_popup').click(function(e){
        e.preventDefault();
        var item = $(this).closest('.conform_delete_popup');

        console.log(item);
        $(item).fadeOut(500);
    });

});