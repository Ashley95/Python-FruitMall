function addCart(goods_id){
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url: '/shopping/addCart/',
        type: 'POST',
        data: {'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function(msg){
            if(msg.code == 200){
                $('#num_' + goods_id).text(msg.c_num)
            }else{
                alert(msg.msg)
            }
        },
        error: function (msg) {
            alert('请求失败')
        }
    });
}

function subCart(goods_id){
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url: '/shopping/subCart/',
        type: 'POST',
        data: {'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (data) {
            if(data.code == 200){
                $('#num_' + goods_id).text(data.c_num)
            }else{
                alert(data.msg)
            }
        },
        error: function (data) {
            alert('请求失败')
        }
    });
}

function changeSelectStatus(cart_id) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url: '/shopping/changeSelectStatus/',
        type: 'POST',
        data: {'cart_id': cart_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (data) {
            if (data.code == 200){
                if(data.is_select){
                    $('#cart_id_' + cart_id).html('√')
                }else{
                    $('#cart_id_' + cart_id).html('×')
                }
            }
        },
        error: function (data) {
            alert('请求失败')
        }
    });
}

function change_order(order_id) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url: '/shopping/changeOrderStatus/',
        type: 'POST',
        data: {'order_id': order_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function(msg){
            if(msg.code == '200'){
                location.href = '/shopping/mine/'
            }
        },
        error: function(msg){
            alert('订单状态修改失败')
        }
    });
}

function all_select(i){
    csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url:'/shopping/changeCartAllSelect/',
        type: 'POST',
        data: {'all_select':i},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {
            if(msg.code == '200'){
                count_price()
                for(var i=0; i<msg.ids.length; i++){
                    if(msg.flag){
                        s= '<span onclick="cartchangeselect(' + msg.ids[i] + ')">x</span>'
                        $('#changeselect_'+ msg.ids[i]).html(s)

                        $('#all_select_id').attr({'onclick': 'all_select(1)'})
                        $('#select_id').html('√')
                    }else{
                        s= '<span onclick="cartchangeselect(' + msg.ids[i] + ')">√</span>'
                        $('#changeselect_'+ msg.ids[i]).html(s)

                        $('#all_select_id').attr({'onclick': 'all_select(0)'})
                        $('#select_id').html('x')
                    }
                }
            }
        },
        error:function(msg){
            alert('请求失败')
        }
    });
}

function count_price(){

    $.get('/shopping/countPrice/', function(msg){
        if(msg.code == '200'){
            $('#count_price').html('总价:' + msg.count_price)
        }
    })
}

$.get('/shopping/countPrice', function(msg){
    if (msg.code == '200'){
        $('#count_price').html('总价:' + msg.count_price)
    }
})
