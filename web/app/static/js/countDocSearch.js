//Counting table row
// Get the tbody element
var tbody = document.getElementById("document-list");
// Get the number of rows in the tbody
var rowCount = tbody.getElementsByTagName("tr").length;

// Get the span element with ID "all-doc"
var docFound = document.getElementById("doc-founded");
var subDocFound = document.getElementById("all-founded");

//Add row count
docFound.textContent = rowCount;
subDocFound.textContent = rowCount;