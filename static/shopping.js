const storeSearch = document.querySelector('#store-search');
const storeFlexBox = document.querySelector('#store-flexbox');
const itemFlexBox = document.querySelector('#item-flexbox');
const searchForm = document.querySelector('search-form');
const searchField = document.querySelector('#search-store-field');
const searchButton = document.querySelector('#search-button');
const addItem = document.querySelector('#add-item-btn');
const storeSelect = document.querySelector('#store-select-dropdown');
const addedItemField = document.querySelector('#added-item');
let autoComplete;

function checkAddedItemFieldForCommas() {
    if (!addedItemField.value.includes(',')) {
        if (addedItemField.value.length > 0) {
            addItem.disabled = false;
            addedItemField.classList.remove('error-bordered-input-box');
            addedItemField.classList.add('bordered-input-box');
        }
        else {
            addItem.disabled = true;
            addedItemField.classList.remove('bordered-input-box');
            addedItemField.classList.add('error-bordered-input-box');
        }
    }
    else {
        addItem.disabled = true;
        addedItemField.classList.remove('bordered-input-box');
        addedItemField.classList.add('error-bordered-input-box');
    }
}

if (storeSelect.value === 'default') {
    addItem.disabled = true;
}

storeSelect.addEventListener('change', function () {
    checkAddedItemFieldForCommas();
    addedItemField.addEventListener('input', function () {
        checkAddedItemFieldForCommas();
    });
});

searchField.addEventListener('focus', function () {
    searchField.style.width = (searchField.value.length + 1) * 8 + "px";
    searchField.style.minWidth = "300px";
});

searchField.addEventListener('blur', function () {
    searchField.style.minWidth = "225px";
    searchField.style.width = (searchField.value.length + 1) * 8 + "px";
});

function initMap() {
    autoComplete = new google.maps.places.Autocomplete(searchField, {
        types: ['cafe', 'convenience_store', 'department_store', 'drugstore', 'supermarket'],
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