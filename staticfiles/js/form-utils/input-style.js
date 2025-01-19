const inputFields = document.querySelectorAll(".styled-form input");

for (let input of inputFields) {
  input.classList.add(
    "py-2",
    "px-4",
    "bg-gray-100",
    "rounded-lg",
    "border",
    "border-b-none"
  );
}
