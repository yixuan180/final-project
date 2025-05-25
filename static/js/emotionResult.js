document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const emotion = params.get("emotion") || "放鬆";
  const city = params.get("city") || "taipei";

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

  const displayValue = (val) => {
    if (!val || (typeof val === "object" && Object.keys(val).length === 0)) return "無";
    return val;
  };

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
      const container = document.getElementById("resultContainer");
      if (data.success) {
        container.innerHTML = data.data
          .map((d) => `
            <div class="re-result">
                <h2>${displayValue(d.name)}</h2>
                <p><strong>地點描述：</strong>${displayValue(d.description)}</p>
                <img src="${displayValue(d.image_url)}" alt="${displayValue(d.name)}" />
                <p><strong>地址：</strong>${displayValue(d.address)}</p>
                <p><strong>分類：</strong>${displayValue(d.category)}</p>
                <p><strong>營業時間：</strong>${displayValue(d.opening_hours)}</p>
                <p><strong>聯絡資訊：</strong>${displayValue(d.contact_info)}</p>
            </div>
            `)

          .join("");
      } else {
        container.innerHTML = `<p style="color:red;">取得資料失敗：${data.message}</p>`;
      }
    })
    .catch((err) => {
      console.error(err);
      document.getElementById("resultContainer").innerHTML =
        "<p style='color:red;'>伺服器錯誤，請稍後再試</p>";
    });
});
