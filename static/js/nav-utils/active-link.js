// DASHBOARD NAV ACTIVE ITEM
const navLinks = document.getElementsByClassName("nav-link");
navLinks.array.forEach((link) => {
  if (window.location.pathname.includes(link.getAttribute("href"))) {
    link.classList.remove("text-gray-700");
    link.classList.add("bg-green-500/30", "text-green-700");
  } else {
    link.classList.remove("bg-green-500/30", "text-green-700");
    link.classList.add("text-gray-700");
  }
});

// CLASSIFICATION NAV ACTIVE ITEM
const classificationNavLinks = document.getElementsByClassName(
  "classification-nav-link"
);
for (let link of classificationNavLinks) {
  if (window.location.pathname.includes(link.getAttribute("href"))) {
    link.parentElement.classList.remove("text-gray-700");
    link.parentElement.classList.add(
      "border-b-2",
      "border-b-black",
      "text-black"
    );
  } else {
    link.parentElement.classList.remove(
      "border-b-2",
      "border-b-black",
      "text-black"
    );
    link.parentElement.classList.add("text-gray-700");
  }
}
