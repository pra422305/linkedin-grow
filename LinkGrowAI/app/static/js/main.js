document.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-copy-target]");
  if (!button) return;
  const target = document.getElementById(button.dataset.copyTarget);
  if (!target) return;
  await navigator.clipboard.writeText(target.value || target.textContent);
  button.textContent = "Copied";
  setTimeout(() => (button.textContent = "Copy"), 1200);
});
