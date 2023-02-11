function email_check(){
    var text = document.getElementById("Email").value;
    console.log(text.length)
    if((text.includes("@") == false || text.includes(".com") == false && text.includes(".net") == false && text.includes(".org") == false) && text.length != 0){
        document.getElementById("error").innerHTML = "Invalid email";
        document.getElementById("error").style.display = "block";
        document.getElementById(Email).style.border = "red";
        return false;

    }
    else if(text.length == 0){
        document.getElementById("error").innerHTML = "" ;
        document.getElementById("error").style.display = "none";
        return true;
    }

    else{
        document.getElementById("error").innerHTML = "";
        document.getElementById("error").style.display = "none";
        return true;
    }

}
function password(){
    var state = document.getElementById("password_id_icon");
    if (state.type === "password"){
        state.type = "text";
        document.getElementById("icon").classList.remove('fa-eye')  
        document.getElementById("icon").classList.add('fa-eye-slash')
    }
    else{
        state.type = "password";
        document.getElementById("icon").classList.remove('fa-eye-slash')
        document.getElementById("icon").classList.add('fa-eye')  
    }
}

function form_submit(){
    if(email_check() == true){
        document.getElementById("form").submit();
    }
}