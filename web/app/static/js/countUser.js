function userCount() {
    // Get the tbody element
    var tbody = document.getElementById("document-list");
    // Get the number of rows in the tbody
    var rowCount = tbody.getElementsByTagName("tr").length;

    // Get the span element with ID "all-doc"
    var userFound = document.getElementById("user-count");
    // Add row count
    userFound.textContent = rowCount;
}

// Call the function to update the count initially
userCount();