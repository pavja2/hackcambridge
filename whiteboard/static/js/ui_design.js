var message_data = {"results": "nonsense"};
var rendered = false;

(function poll(){
    setTimeout(function(){
        $.ajax({
            url: "/messages",
            type: "GET",
            success: function(data){
                $.observable(message_data).setProperty("results", JSON.parse(data));
                activate_buttons();
                if(!rendered) {
                    render_messages();
                }
            },
            complete: poll,
            timeout: 2000
        })}, 1000);
})();

function render_messages(){
    $("#message_list_div").html($("#messageListTemplate").render(message_data.results.results));
    activate_buttons();
}
function activate_buttons(){
    $(".share-button").click(function(){
        var id = $(this).attr('data-message-id');
           $.ajax({
               method: "POST",
               url: "/share_message",
               data: { "id" : id}
           });
        $(this).hide();
    });

    $(".hide-button").click(function(){
        var id = $(this).attr('data-message-id');
        $.ajax({
            method: "POST",
            url: "/hide_message",
            data: {"id" : id}
        });
    });
}

$(document).ready(function(){
    render_messages();
});