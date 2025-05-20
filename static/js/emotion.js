const emotionButtons = document.querySelectorAll(".firstemo");
const daySelect = document.getElementById("datechosen");
const submitBtn = document.getElementById("submitBtn");

let selectedEmotion = null;

// 點選情緒圖片
emotionButtons.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.preventDefault(); // 阻止 <a> 跳轉

    // 移除所有選擇
    emotionButtons.forEach((b) => b.classList.remove("selected"));

    // 標示選取
    btn.classList.add("selected");

    selectedEmotion = btn.getAttribute("data-index");

    checkFormValid();
  });
});

// 監聽下拉選單
daySelect.addEventListener("change", () => {
  checkFormValid();
});

// 檢查表單狀態
function checkFormValid() {
  if (selectedEmotion && daySelect.value !== "") {
    submitBtn.disabled = false;
  } else {
    submitBtn.disabled = true;
  }
}

// 初始禁用按鈕
submitBtn.disabled = true;

// 按鈕點擊事件
submitBtn.addEventListener("click", (e) => {
  e.preventDefault();

  if (!selectedEmotion || daySelect.value === "") {
    alert("請先選擇一個情緒與縣市！");
    return;
  }

  alert(`你選擇的情緒是 ${selectedEmotion}，縣市為 ${daySelect.value}！`);
});
