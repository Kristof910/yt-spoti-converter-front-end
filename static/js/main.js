console.log(sessionStorage.getItem("access_token"));

if(sessionStorage.getItem("access_token")) {
    connect_link = document.getElementById("connect_button");
    connect_link.innerHTML = "";
    var new_element = document.createElement("p");
    var new_text = document.createTextNode("Spotify account is connected!");
    new_element.appendChild(new_text);
    connect_link.parentNode.replaceChild(new_element, connect_link);

}
