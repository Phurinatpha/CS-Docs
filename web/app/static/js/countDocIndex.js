//Counting table row
// Get the tbody element
var tbody = document.getElementById("document-list");
// Get the number of rows in the tbody
var rowCount = tbody.getElementsByTagName("tr").length;

// Get the span element with ID "all-doc"
var allDoc = document.getElementById("all-doc");

//Add row count
allDoc.textContent = rowCount;