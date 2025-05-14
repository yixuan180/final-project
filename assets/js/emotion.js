const emoItems = document.querySelectorAll(".firstemo");

emoItems.forEach((item) => {
  item.addEventListener("click", () => {
    // 移除所有項目的選取樣式
    emoItems.forEach((el) => el.classList.remove("selected"));
    // 為點擊的項目加上選取樣式
    item.classList.add("selected");
  });
});
