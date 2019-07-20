 $(function() {
    socket = new WebSocket('ws://{{ websocket_address }}/{{ uuid }}');
    socket.onmessage = function(message) {
        message = JSON.parse(message.data);
        selector = 'tr.' + message['trade_no'];
        price = message['price'];
        $(selector).find('td.price').html(price);


}});
