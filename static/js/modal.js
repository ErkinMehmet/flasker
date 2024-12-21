// Arrays to hold the modal elements and buttons
const customModal = [];
const openCustomModalBtn = [];
const closeBtn = [];
const closeModalBtn = [];
const closeModalBtn2 = [];
// Loop to process each modal
for (let i = 1; i <= 3; i++) {
  customModal.push(document.getElementById("modal" + i));  // Get the modal
  openCustomModalBtn.push(document.getElementById("modalbtn" + i));  // Get the open button
  closeBtn.push(document.getElementsByClassName("custom-close2")[i - 1]);  // Get the close button in each modal
  closeModalBtn.push(document.getElementsByClassName("annulerbtn")[i - 1]);  // Get the custom close button


  // Open modal when the open button is clicked
  openCustomModalBtn[i - 1].onclick = function() {
    customModal[i - 1].style.display = "block";
  }

  // Close modal when the close button (×) is clicked
  closeBtn[i - 1].onclick = function() {
    customModal[i - 1].style.display = "none";
    window.location.href = window.location.origin + window.location.pathname;
  }



  // Close modal when clicking outside of the modal
  window.onclick = function(event) {
    if (event.target === customModal[i - 1]) {
      customModal[i - 1].style.display = "none";
      window.location.href = window.location.origin + window.location.pathname;
    }
  }
}
