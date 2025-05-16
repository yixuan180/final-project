const emoItems = document.querySelectorAll(".firstemo");
const daySelect = document.getElementById("datechosen");
const submitBtn = document.querySelector(".button.primary");

let selectedEmotion = null;

emotionButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    // 清除所有選擇
    emotionButtons.forEach((b) => b.classList.remove("selected"));
    // 設定當前選擇
    btn.classList.add("selected");
    selectedEmotion = btn.getAttribute("data-index");
    checkFormValid();
  });
});

// 監聽日期下拉選單變更
daySelect.addEventListener("change", () => {
  checkFormValid();
});

// 檢查是否兩個都選擇了
function checkFormValid() {
  if (selectedEmotion && daySelect.value !== "") {
    submitBtn.disabled = false;
  } else {
    submitBtn.disabled = true;
  }
}

// 初始預設：按鈕不可點
submitBtn.disabled = true;

// 額外：點擊送出按鈕
submitBtn.addEventListener("click", (e) => {
  e.preventDefault(); // 防止表單預設行為
  alert(`你選擇的情緒是 ${selectedEmotion}，天數為 ${daySelect.value} 天！`);
  // 可以在這裡加上跳轉或 AJAX 請求
});
