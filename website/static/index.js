function deleteTransaction(transactionId) {
  console.log("DELETING IN JS")
  fetch("/delete-transaction", {
    method: "POST",
    body: JSON.stringify({ transactionId: transactionId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function openPeople(peopleName) {
  var i;
  var x = document.getElementsByClassName("people");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  document.getElementById(peopleName).style.display = "block";
  for(const el of document.getElementsByClassName("people-tabs")){
    el.classList.remove("active");
  }
  document.getElementById("tab_"+peopleName).classList.add("active");
}

function deleteUser(name){
  console.log("DELETING IN JS")
  fetch("/delete-user", {
    method: "POST",
    body: JSON.stringify({ user_name: name }),
  }).then((_res) => {
    window.location.href = "/users";
  });
}

function copyText(elementId){
  var el = document.getElementById(elementId);
  
  let text_to_copy = el.innerText.slice(0, -4).trim();

  // Copy the text inside the text field
  navigator.clipboard.writeText(text_to_copy);
  
  fetch("/flash-copied-text", {
    method: "POST",
    body: JSON.stringify({ text: text_to_copy }),
  }).then((_res) => {
    window.location.href = "/";
  });
}