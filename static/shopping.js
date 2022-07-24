const addStore = document.querySelector('#add-store');
const cancelAddStore = document.querySelector('#cancel-add-store');
const storeSearch = document.querySelector('#store-search');
const storeFlexBox = document.querySelector('#store-flexbox');
const itemFlexBox = document.querySelector('#item-flexbox');
const searchForm = document.querySelector('search-form');
const searchField = document.querySelector('#search-store-field');
const searchButton = document.querySelector('#search-button');
const addItem = document.querySelector('#add-item-btn');
const storeSelect = document.querySelector('#store-select-dropdown');
const addedItem = document.querySelector('#added-item');
let autoComplete;

cancelAddStore.style.display = 'none';
storeSearch.style.display = 'none';
addItem.disabled = true;

cancelAddStore.addEventListener('click', function () {
    cancelAddStore.style.display = 'none';
    storeSearch.style.display = 'none';
    addStore.style.display = 'block';
});

function addStoreFunc() {
    addStore.style.display = 'none';
    storeSearch.style.display = 'flex';
    cancelAddStore.style.display = 'block';
}

function checkAddedItemForCommas() {
    if (!addedItem.value.includes(',')) {
        if (addedItem.value.length > 0) {
            addItem.disabled = false;
            addedItem.classList.remove('error-bordered-input-box');
            addedItem.classList.add('bordered-input-box');
        }
        else {
            addItem.disabled = true;
            addedItem.classList.remove('bordered-input-box');
            addedItem.classList.add('error-bordered-input-box');
        }
    }
    else {
        addItem.disabled = true;
        addedItem.classList.remove('bordered-input-box');
        addedItem.classList.add('error-bordered-input-box');
    }
}

addStore.addEventListener('click', addStoreFunc);

storeSelect.addEventListener('change', function () {
    checkAddedItemForCommas();
    addedItem.addEventListener('input', function () {
        checkAddedItemForCommas();
    });
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