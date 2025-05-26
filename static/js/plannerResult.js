document.addEventListener("DOMContentLoaded", function () {
  const selectedDays = parseInt(localStorage.getItem("selectedDays")) || 0;
  const container = document.getElementById("resultContainer");

  for (let i = 1; i <= selectedDays; i++) {
    const div = document.createElement("div");
    div.className = "re-result";
    div.innerHTML = `
      <h2>第 ${i} 天</h2>
      <p>早上：</p><br />
      <p>中午：</p><br />
      <p>晚上：</p><br />
    `;
    container.appendChild(div);
  }
});
