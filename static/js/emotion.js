const emotionButtons = document.querySelectorAll(".firstemo");
const citySelect = document.getElementById("city");
const openModalBtn = document.getElementById("openModalBtn");

let selectedEmotion = null;

// 點選情緒圖片
emotionButtons.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.preventDefault();
    emotionButtons.forEach((b) => b.classList.remove("selected"));
    btn.classList.add("selected");
    selectedEmotion = btn.getAttribute("data-index");
    checkFormValid();
  });
});

// 監聽城市選擇
citySelect.addEventListener("change", () => {
  checkFormValid();
});

// 檢查是否可啟用按鈕
function checkFormValid() {
  const isValid = selectedEmotion && citySelect.value !== "";
  openModalBtn.disabled = !isValid;
}

// 點擊按鈕事件
openModalBtn.addEventListener("click", (e) => {
  e.preventDefault();

  // 檢查是否選擇完整
  if (!selectedEmotion || citySelect.value === "") {
    alert("請先選擇一個情緒與縣市！");
    return;
  }

  // 開新分頁跳轉，帶上參數
  const queryString = `?emotion=${selectedEmotion}&city=${citySelect.value}`;
  window.open(`./result.html${queryString}`, "_blank");
});
