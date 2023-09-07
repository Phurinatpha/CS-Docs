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


// <!------------------------------------------1st part------------------------------------------>
// Populate day and year options dynamically
function populateDaysAndYears() {
  const daySelect = document.getElementById("daySelect");
  const yearSelect = document.getElementById("yearSelect");

  // Populate day options (1 to 31)
  for (let day = 1; day <= 31; day++) {
    const option = document.createElement("option");
    option.value = day;
    option.textContent = day;
    daySelect.appendChild(option);
  }

  // Populate year options (from the current year to 1900)
  const currentYear = new Date().getFullYear();
  for (let year = currentYear; year >= 1900; year--) {
    const option = document.createElement("option");
    option.value = year;
    option.textContent = year;
    yearSelect.appendChild(option);
  }
}

// Call the function to populate days and years when the page loads
populateDaysAndYears();


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

