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

function closeLoginForm() {
  document.getElementById("login-overlay").classList.add("close");
  document.getElementById("login-form").classList.add("close");
}

window.onload = (event) => {
  let mainScrollButton = document.getElementById("scroll-down-icon");
  mainScrollButton.addEventListener("click", scrollDown, false);
  let accountButton = document.getElementById("account-button");
  if (accountButton == null) {
    let loginButton = document.getElementById("login-button");
    loginButton.addEventListener("click", showLoginForm, false);
  }
  let loginButtonFooter = document.getElementById("login-button-footer");
  loginButtonFooter.addEventListener("click", showLoginFormFromFooter, false);
  document
    .getElementById("close-login-window")
    .addEventListener("click", closeLoginForm, false);
};
