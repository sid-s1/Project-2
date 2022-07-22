const addStore = document.querySelector('#add-store');
const cancelAddStore = document.querySelector('#cancel-add-store');
const storeSearch = document.querySelector('#store-search');
const storeFlexBox = document.querySelector('#store-flexbox');
const itemFlexBox = document.querySelector('#item-flexbox');

cancelAddStore.style.display = 'none';
storeSearch.style.display = 'none';

cancelAddStore.addEventListener('click', function () {
    cancelAddStore.style.display = 'none';
    storeSearch.style.display = 'none';
    addStore.style.display = 'block';
});

addStore.addEventListener('click', function () {
    addStore.style.display = 'none';
    storeSearch.style.display = 'flex';
    cancelAddStore.style.display = 'block';

    const searchForm = document.createElement('form');
    const searchField = document.createElement('input');
    const searchButton = document.createElement('button');
    searchField.classList.add('bordered-input-box');
    searchButton.textContent = 'Search Store';
    searchButton.classList.add('centered-btn');
    searchButton.setAttribute('id', 'form-btn');

    searchForm.classList.add('flex-for-col');
    searchForm.append(searchField, searchButton);
    storeFlexBox.append(searchForm);

});