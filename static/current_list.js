const editBtns = document.querySelectorAll('.edit-item-btn');
const deleteBtns = document.querySelectorAll('.delete-item-btn');
const itemName = document.querySelector('#item-name');
const oldItemName = document.querySelector('#old-item-name');
const delItemName = document.querySelector('#item-name-del');
const storeId = document.querySelector('#store-id');
const delStoreId = document.querySelector('#store-id-del');
const cancelEdit = document.querySelector('#cancel-edit');
const cancelDel = document.querySelector('#cancel-delete');
const modal = document.querySelector('.modal');
const deleteModal = document.querySelector('.delete-modal');

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