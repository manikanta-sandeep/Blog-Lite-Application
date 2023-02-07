function changeLanguage(language) {
    var element = document.getElementById("url");
    element.value = language;
    element.innerHTML = language;
  }
  
  function showDropdown(j) {
    document.getElementById("myDropdown-"+j).classList.toggle("show");
  }
  
  // Close the dropdown if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches(".dropbtn")) {
      var drop = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < drop.length; i++) {
        var openDropdown = drop[i];
        if (openDropdown.classList.contains("show")) {
          openDropdown.classList.remove("show");
        }
      }
    }
  };
  