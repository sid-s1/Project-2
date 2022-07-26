const editBtns = document.querySelectorAll('.edit-item-btn');
const deleteBtns = document.querySelectorAll('.delete-item-btn');
const itemName = document.querySelector('#item-name');
const oldItemName = document.querySelector('#old-item-name');
const storeId = document.querySelector('#store-id');
const cancelEdit = document.querySelector('#cancel-edit');
const modal = document.querySelector('.modal');

for (const editBtn of editBtns) {
    editBtn.addEventListener('click', function () {
        // $("#editModal").modal();
        const itemAndIds = editBtn.previousElementSibling.value;
        const itemAndIdsArr = itemAndIds.split(',');
        itemName.value = itemAndIdsArr[0];
        oldItemName.value = itemAndIdsArr[0];
        storeId.value = itemAndIdsArr[1];
    });
}

cancelEdit.addEventListener('click', function () {
    $("#editModal").modal('hide');
});

// for (const deleteBtn of deleteBtns) {
//     deleteBtn.addEventListener('click',function (){

//     });
// }