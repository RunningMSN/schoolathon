function registrationValid() {
    var name = document.getElementById("inputName").value;
    var email = document.getElementById("inputEmail").value;
    var fruit = document.getElementById("inputFruit").value;
    var submit_button = document.getElementById("submitButton");
    if (name.length > 0 && email.length > 0 && fruit.length > 0) {
        submit_button.removeAttribute("disabled");
    } else {
        submit_button.setAttribute("disabled", "disabled");
    }
}


function loginValid() {
    var email = document.getElementById("inputEmail").value;
    var fruit = document.getElementById("inputFruit").value;
    var submit_button = document.getElementById("submitButton");
    if (email.length > 0 && fruit.length > 0) {
        submit_button.removeAttribute("disabled");
    } else {
        submit_button.setAttribute("disabled", "disabled");
    }
}