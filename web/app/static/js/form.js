// <!------------------------------------------Action after closing form------------------------------------------>
// Function to reset the form fields and uploaded file name
function resetForm() {
  // Reset the form fields to their default values
  document.getElementById('myForm').reset();
  // Reset uploaded file related elements
  uploadedFileName = ''; // Clear the global variable
  const uploadedFileContainer = document.getElementById('uploaded-file-container');
  const dragAndDropZone = document.getElementById('drag-and-drop');
  const uploadedFileNameElement = document.getElementById('uploaded-file-name');
  uploadedFileNameElement.textContent = '';
  uploadedFileContainer.style.display = 'none';
  dragAndDropZone.style.display = 'flex';
}

// Event delegation to handle the close button click event
document.addEventListener('click', function (event) {
  if (event.target && event.target.id === 'closeModal') {
    resetForm();
  }
});

//Clear input in model while clicking outside
$('#modal-form').on('hidden.bs.modal', function () {
  resetForm()
});


// <!--------------------------------------------3rd part-------------------------------------------->
function allowDrop(event) {
  event.preventDefault();
}

function handleDrop(event) {
  event.preventDefault();
  const file = event.dataTransfer.files[0];
  handleFile(file);
  updatePreview(file); // Pass the file object to updatePreview
}

function handleFileSelect(event) {
  const file = event.target.files[0];
  handleFile(file);
  updatePreview(file); // Pass the file object to updatePreview
}

function handleFile(file) {
  const uploadedFileContainer = document.getElementById('uploaded-file-container');
  const dragAndDropZone = document.getElementById('drag-and-drop');

  uploadedFileName = file.name; // Store the uploaded file name in the global variable
  document.getElementById('uploaded-file-name').textContent = uploadedFileName;
  uploadedFileContainer.style.display = 'block';
  dragAndDropZone.style.display = 'none';
  // console.log(file.name)
}

function removeUploadedFile() {
  const uploadedFileContainer = document.getElementById('uploaded-file-container');
  const dragAndDropZone = document.getElementById('drag-and-drop');
  const uploadedFileNameElement = document.getElementById('uploaded-file-name');

  // Clear the global variable for the uploaded file name
  uploadedFileName = '';

  // Reset the file input element
  const fileInput = document.getElementById('file-input');
  fileInput.value = '';
  const newFileInput = fileInput.cloneNode(true);
  fileInput.parentNode.replaceChild(newFileInput, fileInput);

  // Hide the uploaded file container and show the drag and drop zone
  uploadedFileNameElement.textContent = '';
  uploadedFileContainer.style.display = 'none';
  dragAndDropZone.style.display = 'flex';
}

// if remove this it will make ref_num and auto current date broke
// const thaiDatePicker = new Pikaday({
//   field: document.getElementById('thaiDatePicker'),
//   format: 'DD/MM/YYYY',
//   i18n: {
//     previousMonth: 'เดือนก่อนหน้า',
//     nextMonth: 'เดือนถัดไป',
//     months: ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'],
//     weekdays: ['อาทิตย์', 'จันทร์', 'อังคาร', 'พุธ', 'พฤหัสบดี', 'ศุกร์', 'เสาร์'],
//     weekdaysShort: ['อา', 'จ', 'อ', 'พ', 'พฤ', 'ศ', 'ส'],
//   },
//   onSelect: function () {
//     const selectedDate = thaiDatePicker.getDate();
//     const selectedYear = selectedDate.getFullYear();
//     const thaiBuddhistYear = selectedYear + 543;
//     const inputField = document.getElementById('thaiDatePicker');
//     inputField.value = inputField.value.replace(/\d{4}\s*/, thaiBuddhistYear); // Replace the year part of the input value
//   }
// });
// Function to check if a year is in the Thai Buddhist calendar and convert it if necessary
// function convertToThaiBuddhistYear(year) {
//   const currentYear = new Date().getFullYear(); // Get the current Gregorian year
//   return year >= 1900 && year <= currentYear ? year + 543 : year; // Convert to Thai Buddhist year if in range
// }

// Set a default date




$(document).ready(function () {
  $("#myForm").submit(function (event) {
    // prevent default html form submission action
    //event.preventDefault();
    event.preventDefault();
    ori_date = document.getElementById("thaiDatePicker").value
    str_date = ori_date.split("/");
    date = str_date[2] + "-" + str_date[1] + "-" + str_date[0]
    // Create a new FormData object
    var formData = new FormData();
    name_list = document.getElementById("name_list").value
    name_list = name_list.split("\n")
    console.log(name_list)
    // Append the file to the FormData object
    var file = $('input[name="doc_data"]')[0].files[0];
    formData.append('doc_data', file);

    // Add other form data to the FormData object
    formData.append('id', $('#doc_id').val());
    formData.append('subject', $('#descrip').val());
    formData.append('doc_date', date);
    formData.append('ref_num', $('#refer_num').val());
    formData.append('ref_year', str_date[2]);
    formData.append('name_list', name_list);
    formData.append('user_id', $('#usr_id').val());


    console.log(formData);
    var $form = $(this);
    var url = $form.attr("action");
    $.ajax({
      type: 'POST',
      url: url,
      data: formData,
      contentType: false,
      processData: false,
      success: function () {
        Swal.fire({
          position: 'center',
          icon: 'success',
          title: 'บันทึกเอกสารสำเร็จ',
          showConfirmButton: false,
          timer: 1500
        })
        $('#modal-form').modal('toggle');
        resetForm();
        refresh();
        var count_doc = document.getElementById("count_doc").innerHTML;
        document.getElementById("count_doc").innerHTML = parseInt(count_doc) + 1;

      },
      error: function (error) {
        console.error('Error', error);
      }
    });
  });

  // Initialize the Thai date picker
  // Call the setup function to initialize the Thai date picker

});

