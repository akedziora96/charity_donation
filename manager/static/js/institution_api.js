// function show_id()
// {
//     const ids = get_checked_chexboxes();
//     console.log(ids)}
//     // const params = new URLSearchParams();
//     // ids.forEach(id => params.append("id", id))
//     //
//     // const address = '/get_institution_api?'+ params.toString();
//     // fetch(address)
//     //     .then(response => response.json())
//     //     .then(data => {
//     //         if(isEmpty(data)) {
//     //             document.querySelector('#category-submit').disabled = true
//     //         }
//     //         else {
//     //             document.querySelector('#category-submit').disabled = false
//     //         }
//     //     }
//         //     data.forEach(inst => {
//         //
//         //         let emptyJson = true
//         //         console.log(emptyJson)
//         //         if(!jQuery.isEmptyObject(data)) {
//         //             emptyJson = false
//         //         }
//         //         console.log(emptyJson)
//         //         if(emptyJson) {
//         //             document.querySelector('#category-submit').disabled = true
//         //         }
//         //         else {
//         //             document.querySelector('#category-submit').disabled = false
//         //         }
//         //     })
//         // })
//         // )}
//
//
// function get_checked_chexboxes()
// {
//     var markedCheckbox = document.querySelectorAll('input[type="radio"]:checked');
//     var ids = [];
//     markedCheckbox.forEach(box => ids.push(box.value));
//     return ids
// }
//
// $( document ).ready(function() {
//     document.querySelectorAll('#institution_radio_checkbox').
//     forEach(checkbox_radio => {
//         console.log(checkbox_radio)
//         })
//     });
//
//
//
// // function isEmpty(obj) {
// //     return Object.keys(obj).length === 0;
// // }