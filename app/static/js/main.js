$(document).ready(function(){
    $('#form_message').on('submit', function(e){
        e.preventDefault();
        $.ajax({
            url: '/users/post_message',
            type: 'post',
            data: $(this).serialize(),
            dataType: 'json',
            success: function(res){
                if(res.error){
                    $('.m_error').html('*'+res.error)
                } else {
                    $('#form_message').after(res.html);
                }
            }
        })
    })
    $('body').on('submit', '.form_comment', function(e){
        e.preventDefault();
        console.log('hello')
        var messageId = $(this).attr('messageId');
        var form = $(this);
        $.ajax({
            url: '/users/post_comment/' + messageId,
            type: 'post',
            data: $(this).serialize(),
            dataType: 'json',
            success: function(res){
                if(res.error){
                    console.log('hi')
                    form.find('.c_error').html('*'+res.error)
                } else {
                    console.log(res.html);
                    form.siblings().html(res.html);
                }
            }
        })
    })
    $('body').on('click', '.message_delete', function(e){
        e.preventDefault();
        var messageId = $(this).attr('messageId');
        var btnDelete = $(this)
        $.ajax({
            url: '/users/delete_message/' + messageId,
            type: 'get',
            dataType: 'json',
            success: function(res){
                if(res.delete){
                    btnDelete.parents().parents('section').hide();
                }
            }
        })
    })
    $('body').on('click', '.comment_delete', function(e){
        e.preventDefault();
        var commentId = $(this).attr('commentId');
        var btnDelete = $(this)
        $.ajax({
            url: '/users/delete_comment/' + commentId,
            type: 'get',
            dataType: 'json',
            success: function(res){
                if(res.delete){
                    btnDelete.parentsUntil('.overflow-auto').hide();
                }
            }
        })
    })
    $('body').on('click', '.message_edit', function(e){
        e.preventDefault();
        var form = $(this).parentsUntil('section').siblings('form');
        var p = $(this).parentsUntil('section').siblings('p');
        var messageId = $(form).attr('messageId');
        $(p).hide();
        $(form).show();
        $(form).on('change', function(){
            $.ajax({
                url: '/users/edit_message/' + messageId,
                type: 'post',
                data: $(form).serialize(),
                dataType: 'json',
                success: function(res){
                    if(res.error){
                        $(form).find('.m_error').html('*'+res.error)
                    } else {
                        $(form).hide();
                        $(p).html(res.message);
                        $(p).show();
                    }
                }
            })
        })
    })
    $('body').on('click', '.comment_edit', function(e){
        e.preventDefault();
        var form = $(this).parentsUntil('section').siblings('form');
        var p = $(this).parentsUntil('section').siblings('p');
        var commentId = $(form).attr('commentId');
        $(p).hide();
        $(form).show();
        $(form).on('change', function(){
            $.ajax({
                url: '/users/edit_comment/' + commentId,
                type: 'post',
                data: $(form).serialize(),
                dataType: 'json',
                success: function(res){
                    if(res.error){
                        $(form).find('.c_error').html('*'+res.error)
                    } else {
                        $(form).hide();
                        $(p).html(res.comment);
                        $(p).show();
                    }
                }
            })
        })
    })
})