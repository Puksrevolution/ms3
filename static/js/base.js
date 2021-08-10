document.querySelector('#copyright-year').innerText = new Date().getFullYear();

$(document).ready(function () {
    var scriptElement = $('#baseScript')[0];
    var path = scriptElement.getAttribute('data-path');
    $('a[href="'+path+'"]').addClass("active");
});

$("submit").click(function () {
    alert('Are you sure you want to delete this recipe?');
});

var button = document.getElementById("button");

function SendMessage(element, message) {
  document.getElementById(element).innerHTML = message;
  console.log("This is fake data!", "Green button is disabled now.");
}

new SweetConfirm(button, () => {
  SendMessage(
    "message",
    "OK! Fake data was sent to console.<br/>Refresh page for try again!"
  );
});

var button = document.getElementById("button");

function SendMessage(element, message) {
  document.getElementById(element).innerHTML = message;
  console.log("This is fake data!", "Green button is disabled now.");
}

new SweetConfirm(button, () => {
  SendMessage(
    "message",
    "OK! Fake data was sent to console.<br/>Refresh page for try again!"
  );
},{
  bg: "#0f4c81",
  bgSize: "215% 100%",
  bgPositionIn: "right bottom",
  bgPositionOut: "left bottom",
  trans: {
    init: true,
    in: 0.5,
    out: 0.5,
  },
  gradient: {
    deg: "135deg",
    from_color: "#0f4c81 50%",
    to_color: "#fa7268 50%"
  },
  question: "? Are you sure?",
  success: {
    message: "? Success!",
    color: "#00b16a"
  },
  timeout: 3000
});