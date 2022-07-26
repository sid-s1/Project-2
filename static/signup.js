const searchField = document.getElementById('home-address');
const signupEmail = document.querySelector('#signup-email');
const signupFields = document.querySelector('#signup-fields');
const password = document.querySelector('#pw');
const retypedPassword = document.querySelector('#repw');
const signupBtn = document.querySelector('#form-btn');
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

password.addEventListener('input', function () {
    const warningNotif = document.querySelector('#warning');
    if (password.value !== retypedPassword.value) {
        changeSubmitBtn(signupBtn, false);
        password.style.border = "2px solid red";
        retypedPassword.style.border = "2px solid red";
        if (!warningNotif) {
            const warning = document.createElement('p');
            warning.textContent = "Both passwords must match!";
            warning.id = 'warning';
            signupFields.appendChild(warning);
        }
    }
    else {
        if (passwordValidityChecker(password.value)) {
            changeSubmitBtn(signupBtn, true);
        }
        password.style.border = "2px solid black";
        retypedPassword.style.border = "2px solid black";
        warning.remove();
    }
});

retypedPassword.addEventListener('input', function () {
    const warningNotif = document.querySelector('#warning');
    if (password.value !== retypedPassword.value) {
        changeSubmitBtn(signupBtn, false);
        password.style.border = "2px solid red";
        retypedPassword.style.border = "2px solid red";
        if (!warningNotif) {
            const warning = document.createElement('p');
            warning.textContent = "Both passwords must match!";
            warning.id = 'warning';
            signupFields.appendChild(warning);
        }
    }
    else {
        if (passwordValidityChecker(password.value)) {
            changeSubmitBtn(signupBtn, true);
        }
        password.style.border = "2px solid black";
        retypedPassword.style.border = "2px solid black";
        warning.remove();
    }
});

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

function passwordValidityChecker(password) {
    if (!/(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[-+_!@#$%^&*.,?])/.test(password)) {
        return false
    }
    else {
        return true
    }
}