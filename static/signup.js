const searchField = document.getElementById('home-address');
const signupEmail = document.querySelector('#signup-email');
const signupFields = document.querySelector('#signup-fields');
const password = document.querySelector('#pw');
const retypedPassword = document.querySelector('#repw');
const signupBtn = document.querySelector('#form-btn');
const checkUcLi = document.querySelector('#uc');
const checkLcLi = document.querySelector('#lc');
const checkDigLi = document.querySelector('#dig');
const checkSpecLi = document.querySelector('#spec');
const checkLenLi = document.querySelector('#eight');
const allPwLis = document.querySelectorAll('.pointers-pw li');
const guidelines = document.querySelector('.pointers-pw');
const warning = document.querySelector('#guidelines-notif');
const tryAgain = document.querySelector('#try-again');
let warningChanged = false;

function changeWidthBlur(event) {
    event.target.style.width = "225px";
    event.target.style.minWidth = "225px";
}

function changeWidthFocus(event) {
    event.target.style.width = (event.target.value.length + 1) * 8 + "px";
    event.target.style.minWidth = "300px";
}

searchField.addEventListener('focus', changeWidthFocus);
searchField.addEventListener('blur', changeWidthBlur);

changeSubmitBtn(signupBtn, false);

for (const pwLi of allPwLis) {
    pwLi.classList.add('list-items');
}

function initMap() {
    autoComplete = new google.maps.places.Autocomplete(searchField, {
        types: ['street_address', 'subpremise', 'intersection', 'premise'],
        fields: ['place_id', 'geometry', 'name']
    });
    autoComplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged() {
    const place = autoComplete.getPlace();
    if (!place.geometry) {
        searchField.placeholder = "Enter a place";
    }
}

function changeSubmitBtn(btn, bool) {
    if (!bool) {
        signupBtn.disabled = true;
    }
    else {
        signupBtn.disabled = false;
    }
}

function warningInputBoxes() {
    password.style.border = "2px solid red";
    retypedPassword.style.border = "2px solid red";
}

function resetInputBoxes() {
    password.style.border = "2px solid black";
    retypedPassword.style.border = "2px solid black";
}

function createWarningMessage() {
    warning.textContent = "Please ensure your password follows the below guidelines, and that both passwords match!";
    warningChanged = true;
}

function validityChecks() {
    passwordValidityChecker();
    if (password.value !== retypedPassword.value) {
        changeSubmitBtn(signupBtn, false);
        warningInputBoxes();
        if (!warningChanged) {
            createWarningMessage();
        }
    }
    else {
        passwordValidityChecker();
        resetInputBoxes();
        warning.textContent = "Please ensure your password follows the below guidelines!";
        warningChanged = false;
    }
}

function passwordValidityChecker() {
    changeSubmitBtn(signupBtn, true);
    if (!checkLc(password.value)) {
        changeSubmitBtn(signupBtn, false);
        checkLcLi.classList.add('list-items');
    }
    else {
        checkLcLi.classList.remove('list-items');
    }
    if (!checkUc(password.value)) {
        changeSubmitBtn(signupBtn, false);
        checkUcLi.classList.add('list-items');
    }
    else {
        checkUcLi.classList.remove('list-items');
    }
    if (!checkSpec(password.value)) {
        changeSubmitBtn(signupBtn, false);
        checkSpecLi.classList.add('list-items');
    }
    else {
        checkSpecLi.classList.remove('list-items');
    }
    if (!checkDig(password.value)) {
        changeSubmitBtn(signupBtn, false);
        checkDigLi.classList.add('list-items');
    }
    else {
        checkDigLi.classList.remove('list-items');
    }
    if (!checkLen(password.value)) {
        changeSubmitBtn(signupBtn, false);
        checkLenLi.classList.add('list-items');
    }
    else {
        checkLenLi.classList.remove('list-items');
    }
}

function checkLc(password) {
    if (/(?=.*[a-z])/.test(password)) {
        return true
    }
    else {
        return false
    }
}

function checkUc(password) {
    if (/(?=.*[A-Z])/.test(password)) {
        return true
    }
    else {
        return false
    }
}

function checkDig(password) {
    if (/(?=.*\d)/.test(password)) {
        return true
    }
    else {
        return false
    }
}

function checkSpec(password) {
    if (/(?=.*[-+_!@#$%^&*.,?])/.test(password)) {
        return true
    }
    else {
        return false
    }
}

function checkLen(password) {
    if (password.length >= 8) {
        return true
    }
    else {
        return false
    }
}

[password, retypedPassword].forEach((element) => {
    element.addEventListener('input', validityChecks);
});