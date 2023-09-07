function showDropdownMenu(event) {
  var dropdown = event.target.nextElementSibling;
  if (dropdown.style.display === "block") {
    dropdown.style.display = "none";
  } else {
    dropdown.style.display = "block";
  }

  document.addEventListener("click", function (event) {
    if (!event.target.matches('#user_pic')) {
      dropdown.style.display = "none";
    }
  });
}

function toggleNavbar() {
  var navbarCollapse = document.getElementById("navbarCollapse");
  if (navbarCollapse.classList.contains("show")) {
    navbarCollapse.classList.remove("show");
  } else {
    navbarCollapse.classList.add("show");
  }
}

