const submit = document.querySelector('#form-btn');
const emailField = document.querySelector('#login-email');
const pwField = document.querySelector('#login-pw');

submit.disabled = true;

function toggleSubmit(event) {
    if (emailField.value === "" || pwField.value === "") {
        submit.disabled = true;
    }
    if (emailField.value !== "" && pwField.value !== "") {
        submit.disabled = false;
    }
}

[emailField, pwField].forEach((element) => {
    element.addEventListener('input', toggleSubmit);
    element.addEventListener('focus', toggleSubmit);
    element.addEventListener('blur', toggleSubmit);
    element.addEventListener('change', toggleSubmit);
});

emailField.addEventListener('input', toggleSubmit);
pwField.addEventListener('input', toggleSubmit);