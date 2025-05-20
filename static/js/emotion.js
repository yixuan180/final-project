const emotionButtons = document.querySelectorAll(".firstemo");
const citySelect = document.getElementById("city");
const submitBtn = document.getElementById("openModalBtn");

const modal = document.getElementById("myModal");
const closeModalBtn = document.getElementById("closeModalBtn");
const modalText = document.getElementById("modalText");

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

// 檢查是否能啟用按鈕
function checkFormValid() {
  submitBtn.disabled = !(selectedEmotion && citySelect.value !== "");
}

citySelect.addEventListener("change", checkFormValid);

// 模擬推薦結果
function getRecommendation(emotion, city) {
  return "推薦景點 A、B、C";
}

// 點擊「開始推薦」顯示 Modal
submitBtn.addEventListener("click", (e) => {
  e.preventDefault();
  if (!selectedEmotion && citySelect.value === "") {
    alert("請選擇一個情緒與縣市！");
    return;
  } else if (!selectedEmotion) {
    alert("請先選擇一個情緒！");
    return;
  } else if (citySelect.value === "") {
    alert("請先選擇一個縣市！");
    return;
  }
  const cityName = citySelect.options[citySelect.selectedIndex].text;
  const rec = getRecommendation(selectedEmotion, citySelect.value);
  modalText.textContent = `你選擇的情緒是 ${selectedEmotion}，縣市為 ${cityName}。\n推薦你：${rec}`;
  modal.style.display = "flex";
});

// 點擊關閉按鈕或遮罩外關閉 Modal
closeModalBtn.addEventListener("click", () => {
  modal.style.display = "none";
});
modal.addEventListener("click", (e) => {
  if (e.target === modal) {
    modal.style.display = "none";
  }
});
