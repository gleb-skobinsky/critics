function scrollDown() {
  let categories = document.getElementById("latest-materials");
  categories.scrollIntoView({ behavior: "smooth" });
}

function showLoginForm() {
  closeNav();
  document.getElementById("login-overlay").classList.toggle("close");
  document.getElementById("login-form").classList.toggle("close");
  disableScroll();
}

function showLoginFormFromFooter() {
  let upperOfWindow = document.getElementById("main-image");
  upperOfWindow.scrollIntoView({ behavior: "smooth" });
  showLoginForm();
}

function closeLoginForm() {
  document.getElementById("login-overlay").classList.toggle("close");
  document.getElementById("login-form").classList.toggle("close");
  enableScroll();
}

function openNav() {
  document.getElementById("main-drawer").style.width = "250px";
  disableScroll();
}

function enableScroll() {
  document.getElementsByTagName("html")[0].classList.remove("disable-scroll-completely");
  document.body.classList.remove("disable-scroll-completely");
}

function disableScroll() {
  document.getElementsByTagName("html")[0].classList.add("disable-scroll-completely");
  document.body.classList.add("disable-scroll-completely");
}

function closeNav() {
  document.getElementById("main-drawer").style.width = "0";
  enableScroll();
}

function navigateToSearch() {
    window.location.href = "/search"
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
    .getElementById("drawer-closer")
    .addEventListener("click", closeNav, false);
  let searchButtons = document
    .getElementsByName("search-button");
  for (const button of searchButtons) {
    button.addEventListener("click", navigateToSearch, false);
  }
};
