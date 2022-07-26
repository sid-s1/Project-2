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
changeSubmitBtn(signupBtn, false);

function initMap() {
    autoComplete = new google.maps.places.Autocomplete(searchField, {
        types: ['street_address'],
        componentRestrictions: { 'country': ['AU'] },
        fields: ['place_id', 'geometry', 'name']
    });
    autoComplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged() {
    const place = autoComplete.getPlace();
    if (!place.geometry) {
        searchField.placeholder = "Enter a place";
    }
    else {
        const p = document.createElement('p');
        p.textContent = place.name;
        document.body.appendChild(p);
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
    const warning = document.createElement('p');
    warning.textContent = "Both passwords must match!";
    warning.id = 'warning';
    signupFields.appendChild(warning);
}

password.addEventListener('input', function () {
    passwordValidityChecker();
    const warningNotif = document.querySelector('#warning');
    if (password.value !== retypedPassword.value) {
        changeSubmitBtn(signupBtn, false);
        warningInputBoxes();
        if (!warningNotif) {
            createWarningMessage();
        }
    }
    else {
        passwordValidityChecker();
        resetInputBoxes();
        warning.remove();
    }
});

retypedPassword.addEventListener('input', function () {
    passwordValidityChecker();
    const warningNotif = document.querySelector('#warning');
    if (password.value !== retypedPassword.value) {
        changeSubmitBtn(signupBtn, false);
        warningInputBoxes();
        if (!warningNotif) {
            createWarningMessage();
        }
    }
    else {
        passwordValidityChecker();
        resetInputBoxes();
        warning.remove();
    }
});

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


function changeSubmitBtn(btn, bool) {
    if (!bool) {
        signupBtn.disabled = true;
        signupBtn.classList.remove('centered-btn');
        signupBtn.classList.add('disabled-btn');
    }
    else {
        signupBtn.disabled = false;
        signupBtn.classList.remove('disabled-btn');
        signupBtn.classList.add('centered-btn');
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
