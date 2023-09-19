// Generate pagination

//const table = document.getElementById('document-list');
var rowsPerPage = 10; // Number of rows per page
var currentPage = 1;   // Current page
var maxVisiblePages = 9; // Maximum number of visible pagination links
var pageNumbers = document.getElementById('pageNumbers');
// Function to highlight the current page link
function highlightCurrentPageLink() {
    const pageLinks = pageNumbers.getElementsByTagName('a');
    for (let i = 0; i < pageLinks.length; i++) {
        const pageLink = pageLinks[i];
        const pageNumber = parseInt(pageLink.textContent);
        if (pageNumber === currentPage) {
            pageLink.classList.add('current-page');
        } else {
            pageLink.classList.remove('current-page');
        }
    }
}

// Function to show the specified page
function showPage(page) {
    const rows = document.getElementById("count_doc").innerHTML;
    console.log("rows :",rows)
    const totalPages = Math.floor(rows / rowsPerPage);

    // Hide all rows
    //for (let i = 0; i < rows.length; i++) {
       // rows[i].style.display = 'none';
   // }

    // Show rows for the current page
   // for (let i = (page - 1) * rowsPerPage; i < page * rowsPerPage && i < rows.length; i++) {
     //   rows[i].style.display = '';
    //}

    // Generate pagination links
    pageNumbers.innerHTML = '';

    if (totalPages > maxVisiblePages) {
        // Calculate start and end page numbers to display
        let startPage = Math.max(1, page - Math.floor(maxVisiblePages / 2));
        let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

        if (endPage - startPage < maxVisiblePages - 1) {
            startPage = Math.max(1, endPage - maxVisiblePages + 1);
        }

        // Add "Previous" link
        if (startPage > 1) {
            const prevLink = document.createElement('a');
            prevLink.href = '#';
            prevLink.textContent = '1';
            prevLink.addEventListener('click', () => {
                currentPage = 1;
                showPage(currentPage);
                highlightCurrentPageLink();
            });
            pageNumbers.appendChild(prevLink);
            pageNumbers.appendChild(document.createTextNode(' ... '));

        }

        // Add page links
        for (let i = startPage; i <= endPage; i++) {
            const pageLink = document.createElement('a');
            pageLink.href = '#';
            pageLink.textContent = i;
            pageLink.addEventListener('click', () => {
                currentPage = i;
                showPage(currentPage);
                highlightCurrentPageLink();
            });
            pageNumbers.appendChild(pageLink);
        }

        // Add "Next" link
        if (endPage < totalPages) {
            pageNumbers.appendChild(document.createTextNode(' ... '));
            const nextLink = document.createElement('a');
            nextLink.href = '#';
            nextLink.textContent = totalPages;
            nextLink.addEventListener('click', () => {
                currentPage = totalPages;
                showPage(currentPage);
                highlightCurrentPageLink();
            });
            pageNumbers.appendChild(nextLink);
        }
    } else {
        // Display all page links if there are fewer than maxVisiblePages
        for (let i = 1; i <= totalPages; i++) {
            const pageLink = document.createElement('a');
            pageLink.href = '#';
            pageLink.textContent = i;
            pageLink.addEventListener('click', () => {
                currentPage = i;
                showPage(currentPage);
                highlightCurrentPageLink();
            });
            pageNumbers.appendChild(pageLink);
        }
    }

    // Highlight the current page link
    highlightCurrentPageLink();
}

// Show the initial page
// showPage(currentPage);

// // Handle previous page click
// document.getElementById('prevPage').addEventListener('click', () => {
//    if (currentPage > 1) {
//        currentPage--;
//        showPage(currentPage);
//     }
// });

// // Handle next page click
//     document.getElementById('nextPage').addEventListener('click', () => {
//     const rows = table.getElementsByTagName('tr');
//     const totalPages = Math.ceil(rows.length / rowsPerPage);

//     if (currentPage < totalPages) {
//        currentPage++;
//         showPage(currentPage);
//    }
// });