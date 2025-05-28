document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("resultContainer");

  const displayValue = (val) => {
    if (!val || (typeof val === "object" && Object.keys(val).length === 0)) return "無";
    return val;
  };

  // 從 URL 取得參數
  const params = new URLSearchParams(window.location.search);
  const emotion = params.get("emotion") || "放鬆";
  const city = params.get("city") || "taipei";

  // 比對 localStorage 裡是否有相同的結果
  const savedData = localStorage.getItem("emotionResults");
  const savedEmotion = localStorage.getItem("emotionParam");
  const savedCity = localStorage.getItem("cityParam");

  if (savedData && savedEmotion === emotion && savedCity === city) {
    const resultsWithId = JSON.parse(savedData);
    container.innerHTML = resultsWithId
      .map((d) => `
        <div class="re-result">
          <h2>${displayValue(d.name)}</h2>
          <img src="${displayValue(d.image_url)}" alt="${displayValue(d.name)}" style="max-width:100%; height:auto; margin-bottom: 1em;"/>
          <p><strong>地址：</strong>${displayValue(d.address)}</p>
          <p><strong>分類：</strong>${displayValue(d.category)}</p>
          <div style="text-align: center; margin-top: 1em;">
            <a href="emotionDetail.html?id=${d.id}" class="button">查看詳情</a>
          </div>
        </div>
      `).join("");
    return;
  }

  // 城市對應區域表
  const cityToRegionKey = {
    'keelung': '基隆',
    'taipei': '台北',
    'new_taipei': '新北',
    'taoyuan': '桃園',
    'hsinchu_city': '新竹',
    'miaoli': '苗栗',
    'taichung': '臺中',
    'changhua': '彰化',
    'nantou': '南投',
    'yunlin': '雲林',
    'chiayi_city': '嘉義',
    'tainan': '臺南',
    'kaohsiung': '高雄',
    'pingtung': '屏東',
    'yilan': '宜蘭',
    'hualien': '花蓮',
    'taitung': '臺東',
  };

  const regionKey = cityToRegionKey[city] || "台北";

  // 發送 API 請求
  fetch('http://127.0.0.1:8000/emotion/generate-by-emotion/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      emotion: emotion,
      region: regionKey,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        const resultsWithId = data.data.map((d, index) => ({
          ...d,
          id: "emotion_" + index,
        }));

        // 存進 localStorage
        localStorage.setItem("emotionResults", JSON.stringify(resultsWithId));
        localStorage.setItem("emotionParam", emotion);
        localStorage.setItem("cityParam", city);

        container.innerHTML = resultsWithId
          .map((d) => `
            <div class="re-result">
              <h2>${displayValue(d.name)}</h2>
              <img src="${displayValue(d.image_url)}" alt="${displayValue(d.name)}" />
              <p><strong>地址：</strong>${displayValue(d.address)}</p>
              <p><strong>分類：</strong>${displayValue(d.category)}</p>
              <div style="text-align: center; margin-top: 1em;">
                <a href="emotionDetail.html?id=${d.id}" class="button">查看詳情</a>
              </div>
            </div>
          `).join("");
      } else {
        container.innerHTML = `<p style="color:red;">取得資料失敗：${data.message}</p>`;
      }
    })
    .catch((err) => {
      console.error(err);
      container.innerHTML = "<p style='color:red;'>伺服器錯誤，請稍後再試</p>";
    });
});
