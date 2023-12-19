function scrollDown() {
  let categories = document.getElementById("article-categories");
  categories.scrollIntoView({ behavior: "smooth" });
}

function showLoginForm() {
  document.getElementById("login-overlay").classList.remove("close");
  document.getElementById("login-form").classList.remove("close");
}

function showLoginFormFromFooter() {
  let upperOfWindow = document.getElementById("main-image");
  upperOfWindow.scrollIntoView({ behavior: "smooth" });
  showLoginForm();
}

function showNotImplAlert() {
  window.alert("Feature not yet implemented!");
}

function closeLoginForm() {
  document.getElementById("login-overlay").classList.add("close");
  document.getElementById("login-form").classList.add("close");
}

function openNav() {
  document.getElementById("main-drawer").style.width = "250px";
}

function closeNav() {
  document.getElementById("main-drawer").style.width = "0";
}

window.onload = (event) => {
  let mainScrollButton = document.getElementById("scroll-down-icon");
  if (mainScrollButton != null) {
    mainScrollButton.addEventListener("click", scrollDown, false);
  }
  let accountButton = document.getElementById("account-button");
  if (accountButton == null) {
    let loginButtons = document.getElementsByName("login-button");
    for (const button of loginButtons) {
        button.addEventListener("click", showLoginForm, false);
    }
  }
  let loginButtonFooter = document.getElementById("login-button-footer");
  loginButtonFooter.addEventListener("click", showLoginFormFromFooter, false);
  document
    .getElementById("close-login-window")
    .addEventListener("click", closeLoginForm, false);
  document
    .getElementById("drawer-opener")
    .addEventListener("click", openNav, false);
  document
    .getElementById("drawer-opener")
    .addEventListener("touchstart", openNav, false);
  document
    .getElementById("drawer-closer")
    .addEventListener("click", closeNav, false);
  document
    .getElementById("languages-button")
    .addEventListener("click", showNotImplAlert, false);
  document
    .getElementById("search-button")
    .addEventListener("click", showNotImplAlert, false);
};
