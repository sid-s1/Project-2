const storeFlexBox = document.querySelector('#store-flexbox');
const itemFlexBox = document.querySelector('#item-flexbox');
const searchForm = document.querySelector('search-form');
const searchField = document.querySelector('#search-store-field');
const searchButton = document.querySelector('#search-button');
const addItem = document.querySelector('#add-item-btn');
const storeSelect = document.querySelector('#store-select-dropdown');
const addedItemField = document.querySelector('#added-item');
const modal = document.querySelector('.modal');
const formBtn = document.querySelector('#form-btn');
const goBackBtns = document.querySelectorAll('.go-back');
const formsForGoingBack = document.querySelectorAll('.form-for-goBack');
const leavePageForms = document.querySelectorAll('.leave-page');
const leavePageBtns = document.querySelectorAll('.leave-page button')
let autoComplete;
formBtn.disabled = true;

if (storeSelect.value === 'default') {
    addItem.disabled = true;
}

function submitForm() {
    leavePage.submit();
}

function toggleModal() {
    if (modal) {
        modal.classList.toggle('show-modal');
    }
}

if (leavePageForms) {
    for (const leavePage of leavePageForms) {
        leavePage.addEventListener('submit', function (event) {
            event.preventDefault();
        });
    }
    for (const leavePageBtn of leavePageBtns) {
        leavePageBtn.addEventListener('click', function () {
            toggleModal();
            const leavePageForm = leavePageBtn.parentNode;
            setTimeout(function () {
                leavePageForm.submit();
            }, 500);
        });
    }
}

addItem.addEventListener('click', function () {
    const trial = addItem.parentNode;
    const formTrial = trial.parentNode;
    setTimeout(function () {
        formTrial.submit();
    }, 500);
});

if (modal) {
    setTimeout(() => {
        modal.classList.toggle('show-modal');
    }, 500);
}

formsForGoingBack.forEach((element) => {
    element.addEventListener('submit', toggleModal);
});

function formBtnEnable() {
    if (searchField.value) {
        formBtn.disabled = false;
    }
    else {
        formBtn.disabled = true;
    }
}

function disableAddItem() {
    addItem.disabled = true;
    addedItemField.id = 'error-bordered-input-box';
}

[addedItemField, searchField].forEach((element) => {
    element.addEventListener('input', formBtnEnable);
    element.addEventListener('focus', formBtnEnable);
    element.addEventListener('blur', formBtnEnable);
});

function checkAddedItemFieldForCommas() {
    if (!addedItemField.value.includes(',')) {
        if (addedItemField.value.length > 0) {
            addItem.disabled = false;
            addedItemField.removeAttribute('id');
        }
        else {
            disableAddItem();
        }
    }
    else {
        disableAddItem();
    }
}

function changeWidthBlur(event) {
    event.target.style.width = "225px";
    event.target.style.minWidth = "225px";
}

function changeWidthFocus(event) {
    event.target.style.width = (event.target.value.length + 1) * 8 + "px";
    event.target.style.minWidth = "300px";
    formBtn.style.width = "fit-content";
    addItem.style.width = "fit-content";
}

function initMap() {
    autoComplete = new google.maps.places.Autocomplete(searchField, {
        types: ['store', 'convenience_store', 'department_store', 'drugstore', 'supermarket'],
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
}

searchField.addEventListener('blur', function () {
    searchField.style.minWidth = "225px";
});

[searchField, addedItemField].forEach((element) => {
    element.addEventListener('focus', changeWidthFocus);
    element.addEventListener('blur', changeWidthBlur);
});

storeSelect.addEventListener('change', function () {
    checkAddedItemFieldForCommas();
    addedItemField.addEventListener('input', function () {
        checkAddedItemFieldForCommas();
    });
});