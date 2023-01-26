const usernameField = document.querySelector("#username");
const feedBackArea = document.querySelector(".invalid-feedback");
const emailField = document.querySelector("#email");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const fnameField = document.querySelector("#fname");
const fnameFeedBackArea = document.querySelector(".fnameFeedBackArea");
const lnameField = document.querySelector("#lname");
const lnameFeedBackArea = document.querySelector(".lnameFeedBackArea")
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const passwordField = document.querySelector("#pass1");
const submitBtn = document.querySelector(".submit-btn");


showPasswordToggle.addEventListener("click", (e) => {
    if (showPasswordToggle.textContent == "SHOW") {
        showPasswordToggle.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
    } else {
        showPasswordToggle.textContent = "SHOW";
        passwordField.setAttribute("type", "password");
    }
});


usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;


    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display = "none";
    

    if (usernameVal.length > 0) {
        fetch('/validate-username', {
            body: JSON.stringify({ username: usernameVal }),
            method: "POST",
        }).then((res) => res.json())
          .then((data) => {
            console.log("data", data);
        
            if (data.username_error) {
                submitBtn.disabled = true;
                usernameField.classList.add("is-invalid");
                feedBackArea.style.display = "block";
                feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
            } else {
                submitBtn.removeAttribute("disabled");
            }
        });
    }



});

fnameField.addEventListener("keyup", (e) => {
    console.log("77777", 777777);
    const fnameVal = e.target.value;

    fnameField.classList.remove("is-invalid");
    fnameFeedBackArea.style.display = "none";
    

    if (fnameVal.length > 0) {
        fetch('/validate-firstname', {
            body: JSON.stringify({ fname: fnameVal }),
            method: "POST",
        }).then((res) => res.json())
          .then((data) => {
            console.log("data", data);
            if (data.fname_error) {
                submitBtn.disabled = true;
                fnameField.classList.add("is-invalid");
                fnameFeedBackArea.style.display = "block";
                fnameFeedBackArea.innerHTML = `<p>${data.fname_error}</p>`;
            } else {
                submitBtn.removeAttribute("disabled");
            }
        });
    }



});

lnameField.addEventListener("keyup", (e) => {
    console.log("77777", 777777);
    const lnameVal = e.target.value;

    lnameField.classList.remove("is-invalid");
    lnameFeedBackArea.style.display = "none";
    

    if (lnameVal.length > 0) {
        fetch('/validate-lastname', {
            body: JSON.stringify({ lname: lnameVal }),
            method: "POST",
        }).then((res) => res.json())
          .then((data) => {
            console.log("data", data);
            if (data.lname_error) {
                submitBtn.disabled = true;
                lnameField.classList.add("is-invalid");
                lnameFeedBackArea.style.display = "block";
                lnameFeedBackArea.innerHTML = `<p>${data.lname_error}</p>`;
            } else {
                submitBtn.removeAttribute("disabled");             q
            }
        });
    }



});

emailField.addEventListener("keyup", (e) => {

    const emailVal = e.target.value;

    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";


    if (emailVal.length > 0) {
        fetch('/validate-email', {
            body: JSON.stringify({ email: emailVal }),
            method: "POST",
        }).then((res) => res.json())
          .then((data) => {
            console.log("data", data);
            if (data.email_error) {
                submitBtn.disabled = true;
                emailField.classList.add("is-invalid");
                emailFeedBackArea.style.display = "block";
                emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
            } else {
                submitBtn.removeAttribute("disabled");
            }
        });
    }

})