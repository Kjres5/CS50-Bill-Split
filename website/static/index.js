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
}

function addUser(name){
  document.getElementById("new_user").value = "";
  let el = document.createElement("li");
  el.classList.add("list-group-item");
  el.id = name;
  let close_btn = document.createElement("button");
  close_btn.classList.add("close");
  close_btn.setAttribute("type", "button");
  close_btn.addEventListener("click", (e)=>deleteUser(name));
  close_btn.innerHTML = '<span aria-hidden="true">&times;</span>';
  let sp = document.createElement("span");
  sp.innerHTML = name;
  el.appendChild(sp);
  el.appendChild(close_btn);
  let inp = document.createElement("input");
  inp.setAttribute("name", "users");
  inp.setAttribute("value", name);
  inp.style = "display: none";
  el.appendChild(inp);
  document.getElementById("users").appendChild(el);
}


function deleteUser(name){
  document.getElementById(name).remove();
}

