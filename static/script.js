const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

recognition.lang = 'en-US';
recognition.interimResults = false;

document.getElementById("voice").addEventListener("click", () => {
  recognition.start();
});

recognition.addEventListener('result', (e) => {
  let last = e.results.length - 1;
  let text = e.results[last][0].transcript;
  console.log(text)
  console.log('Confidence: ' + e.results[0][0].confidence);
  document.getElementById("u_input").value = text
  // We will use the Socket.IO here later…
});

function synthVoice(text) {
  const synth = window.speechSynthesis;
  const utterance = new SpeechSynthesisUtterance();
  utterance.text = text;
  synth.speak(utterance);
}

window.onload = function exampleFunction() {
    $.post('/initialize',
    {
    initialize_bot: "Initialize",
  },
    function(data,status){
        console.log(typeof data)
        data_object =  JSON.parse(data);
        var botText = data_object["bot_response"];
        $('#chatbox').find(".new-cells").remove();
        $('#chatbox').append('<div class="alert alert-dark new-cells" role="alert" >' + "<b>Bowhead Bot: </b>" + botText + '</div>');
        $('#u_input').show();
        $('#voice').show();
        $('#send_button').show();
        $('#initialize_hint').hide();
        });

}
$('#initialize_button').click(function(){
    $.post('/initialize',
    {
    initialize_bot: "Initialize",
  },
    function(data,status){
        console.log(typeof data)
        data_object =  JSON.parse(data);
        var botText = data_object["bot_response"];
        $('#chatbox').find(".new-cells").remove();
        $('#chatbox').append('<div class="alert alert-dark new-cells" role="alert" >' + "<b>Bowhead Bot: </b>" + botText + '</div>');
        $('#u_input').show();
        $('#voice').show();
        $('#send_button').show();
        $('#initialize_hint').hide();
        });
           });


$('#send_button').click(function(){
    var userText = $('#u_input').val();
    $('#chatbox').append('<div class="alert alert-primary new-cells" role="alert">' + "<b>User: </b>" + userText + '</div>');
    $.post('/process',
    {
    user_input: userText,
  },
    function(data,status){
        console.log(typeof data)
        data_object =  JSON.parse(data);
        var botText = data_object["bot_response"];
        $('#chatbox').append('<div class="alert alert-dark new-cells" role="alert">' + "<b>Bowhead Bot: </b>" + botText + '</div>');
        var element = $('#chatbox div.new-cells:last')[0];
        console.log(element);
        element.scrollIntoView();
        });
     $(this).val("");

            });

$("#u_input").keypress(function(e) {
  if (e.which == 13) {
    var userText = $('#u_input').val();
    $('#chatbox').append('<div class="alert alert-primary new-cells" role="alert">' + "<b>User: </b>" + userText + '</div>');
    var element = $('#chatbox div.new-cells:last')[0];
    console.log(element);
    element.scrollIntoView();
    console.log('success')
    $.post('/process',
    {
    user_input: userText,
  },
    function(data,status){
        console.log(typeof data)
        data_object =  JSON.parse(data);
        var botText = data_object["bot_response"];
        $('#chatbox').append('<div class="alert alert-dark new-cells" role="alert">' + "<b>Bowhead Bot: </b>" + botText + '</div>');
        var element = $('#chatbox div.new-cells:last')[0];
        console.log(element);
        element.scrollIntoView();
        });

    $(this).val("");
  }
});



