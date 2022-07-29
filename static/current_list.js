const editBtns = document.querySelectorAll('.edit-item-btn');
const deleteBtns = document.querySelectorAll('.delete-item-btn');
const itemName = document.querySelector('#item-name');
const oldItemName = document.querySelector('#old-item-name');
const delItemName = document.querySelector('#item-name-del');
const storeId = document.querySelector('#store-id');
const delStoreId = document.querySelector('#store-id-del');
const delStorePrompts = document.querySelectorAll('.delete-store-prompt');
const storeDeleteValue = document.querySelector('#store-confirm-del');
const cancelEdit = document.querySelector('#cancel-edit');
const cancelDel = document.querySelector('#cancel-delete');
const cancelStoreDel = document.querySelector('#cancel-store-delete');
const modal = document.querySelector('.modal');
const deleteModal = document.querySelector('.delete-modal');
const deleteStoreModal = document.querySelector('.delete-store-modal');
const pageRefreshes = document.querySelectorAll('.modal form');
const pgRefreshBtns = document.querySelectorAll('.pg-refresh-btns');


for (const delStorePrompt of delStorePrompts) {
    delStorePrompt.addEventListener('click', function () {
        deleteStoreModal.classList.toggle('show-modal');
        const storeIdDeletion = delStorePrompt.previousElementSibling.value;
        storeDeleteValue.value = storeIdDeletion;
    });
}

for (const pageRefresh of pageRefreshes) {
    pageRefresh.addEventListener('submit', function (event) {
        event.preventDefault();
    });
}

for (const pgRefreshBtn of pgRefreshBtns) {
    pgRefreshBtn.addEventListener('click', function () {
        modal.classList.remove('show-modal');
        deleteModal.classList.remove('show-modal');
        deleteStoreModal.classList.remove('show-modal');
        const containerDiv = pgRefreshBtn.parentNode;
        const formToSubmit = containerDiv.parentNode;
        setTimeout(function () {
            formToSubmit.submit();
        }, "500");
    });
}

for (const editBtn of editBtns) {
    editBtn.addEventListener('click', function () {
        modal.classList.toggle('show-modal');
        const itemAndIds = editBtn.previousElementSibling.value;
        const itemAndIdsArr = itemAndIds.split(',');
        itemName.value = itemAndIdsArr[0];
        oldItemName.value = itemAndIdsArr[0];
        storeId.value = itemAndIdsArr[1];
    });
}

for (const deleteBtn of deleteBtns) {
    deleteBtn.addEventListener('click', function () {
        deleteModal.classList.toggle('show-modal');
        const itemAndIds = deleteBtn.previousElementSibling.value;
        const itemAndIdsArr = itemAndIds.split(',');
        delItemName.value = itemAndIdsArr[0];
        delStoreId.value = itemAndIdsArr[1];
    });
}

cancelEdit.addEventListener('click', function () {
    modal.classList.toggle('show-modal');
});

cancelDel.addEventListener('click', function () {
    deleteModal.classList.toggle('show-modal');
});

cancelStoreDel.addEventListener('click', function () {
    deleteStoreModal.classList.toggle('show-modal');
});