function fetch_messages(){
    $.ajax({
        method: 'GET',
        url: "/messages",
        success: function(resp){
           window.message_data = JSON.parse(resp);
           render_messages();
        }
    })
}

function render_messages(){
    $("#message-list-div").html($("#messageListTemplate").render(window.message_data));
}

$(document).ready(function(){
    fetch_messages();
});