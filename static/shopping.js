const addStore = document.querySelector('#add-store');
const cancelAddStore = document.querySelector('#cancel-add-store');
const storeSearch = document.querySelector('#store-search');
const storeFlexBox = document.querySelector('#store-flexbox');
const itemFlexBox = document.querySelector('#item-flexbox');
const searchForm = document.querySelector('search-form');
const searchField = document.querySelector('#search-store-field');
const searchButton = document.querySelector('#search-button');
let autoComplete;

cancelAddStore.style.display = 'none';
storeSearch.style.display = 'none';

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

addStore.addEventListener('click', addStoreFunc);

function initMap() {
    autoComplete = new google.maps.places.Autocomplete(searchField, {
        types: ['establishment'],
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