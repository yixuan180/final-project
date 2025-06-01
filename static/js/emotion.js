document.addEventListener("DOMContentLoaded", () => {
  const emotionButtons = document.querySelectorAll(".firstemo");
  const citySelect = document.getElementById("city");
  const openModalBtn = document.getElementById("openModalBtn");

  let selectedEmotion = null;

  const emotionMap = {
    "1": "開心",
    "2": "放鬆",
    "3": "焦慮",
    "4": "難過",
  };

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
  citySelect.addEventListener("change", checkFormValid);

  // 檢查是否可啟用按鈕
  function checkFormValid() {
    openModalBtn.disabled = !(selectedEmotion && citySelect.value);
  }

  // 點擊按鈕事件
  openModalBtn.addEventListener("click", (e) => {
    e.preventDefault();

    if (!selectedEmotion || citySelect.value === "") {
      alert("請先選擇一個情緒與縣市！");
      return;
    }

    const emotionName = emotionMap[selectedEmotion];
    const queryString = `?emotion=${emotionName}&city=${citySelect.value}`;
    window.open(`/emotion/emotionResult/${queryString}`, "_blank");
  });

  // 初始檢查一次表單
  checkFormValid();
});
