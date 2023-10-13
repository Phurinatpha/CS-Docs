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

// Set the session timeout duration in milliseconds (e.g., 1 hour)
const sessionTimeoutDuration = 3600000; // 1 hr in milliseconds
// const sessionTimeoutDuration = 5000; // 5 seconds in milliseconds


// Function to log the user out
function logout() {
  user_logout();
  // Perform any necessary logout actions (e.g., clearing session, redirecting)
  // window.location.href = '/logout'; // Redirect to the logout route
}

// Function to reset the session timeout timer
// function resetSessionTimeout() {
//     clearTimeout(sessionTimeoutTimer); // Clear the previous timer
//     sessionTimeoutTimer = setTimeout(logout, sessionTimeoutDuration);
// }

// Initialize the session timeout timer on page load
let sessionTimeoutTimer = setTimeout(logout, sessionTimeoutDuration);

// Add event listeners to reset the timer on user activity
// document.addEventListener('mousemove', resetSessionTimeout);
// document.addEventListener('keydown', resetSessionTimeout);
