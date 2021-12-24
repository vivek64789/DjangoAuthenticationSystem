// validation code for user registration form of register page

// validation start

// const id_username = document.getElementById("id_username");
//
// id_username.addEventListener("keyup", (e) => {
//     console.log("777777", 77777)
//
//     const usernameVal = e.target.value;
//     // console.log("Usernameval", usernameVal);
//
//     if (usernameVal.length > 0) {
//
//         fetch("/validate-username/", {
//             body: JSON.stringify({username: usernameVal}),
//             method: "POST",
//         })
//             .then((res) => res.json())
//             .then((data) => {
//             console.log("data", data)
//         }); // first then is mapping to json and then is mapping to return a data
//     }
// });

$("#id_username").keyup(function (e){
    console.log("Oka ")
    const usernameVal = e.target.value;
    console.log(usernameVal)
    let csrf = $("input[name=csrfmiddlewaretoken]").val();

    mydata = {username:usernameVal,csrfmiddlewaretoken:csrf};
    $.ajax({
       url:"{% url 'validate-username' %}",
        method:"POST",
        data:mydata,
        success: function (data){
           console.log("data")
        },
    });
});
