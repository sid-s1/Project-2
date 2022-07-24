const searchField = document.getElementById('home-address');

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