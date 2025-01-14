const navLinks = document.getElementsByClassName("nav-link");
for (let link of navLinks) {
  if (window.location.pathname.includes(link.getAttribute("href"))) {
    link.classList.remove("text-gray-700");
    link.classList.add("bg-green-500/30", "text-green-700");
  } else {
    link.classList.remove("bg-green-500/30", "text-green-700");
    link.classList.add("text-gray-700");
  }
}
