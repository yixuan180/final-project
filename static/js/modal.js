const openModalBtn = document.getElementById("openModalBtn");
const modal = document.getElementById("myModal");
const closeModalBtn = document.getElementById("closeModalBtn");
const modalText = document.getElementById("modalText");

openModalBtn.addEventListener("click", (e) => {
  e.preventDefault();

  // 你可以把推薦結果放進這裡
  modalText.textContent = "推薦結果：根據您的選擇推薦這裡...";

  modal.style.display = "flex";
});

closeModalBtn.addEventListener("click", () => {
  modal.style.display = "none";
});

// 點擊遮罩外也可以關閉 Modal
modal.addEventListener("click", (e) => {
  if (e.target === modal) {
    modal.style.display = "none";
  }
});
