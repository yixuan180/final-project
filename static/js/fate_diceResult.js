document.addEventListener("DOMContentLoaded", () => {
  const recommendationContainer = document.getElementById("recommendationContainer");
  const mainTitleElement = document.querySelector("article#main header.major h2");
  const thrownThemeDisplayElement = document.getElementById("thrownThemeDisplay");

  const display = (value) =>
    !value || (typeof value === "object" && Object.keys(value).length === 0) ? "無" : value;

  // 嘗試從 localStorage 讀快取
  const cachedResult = localStorage.getItem("fateDiceResultCache");
  if (cachedResult) {
    const parsed = JSON.parse(cachedResult);
    renderFateResult(parsed);
    return;
  }

  const rawData = sessionStorage.getItem("fateDiceResult");

  if (!rawData) {
    if (mainTitleElement) mainTitleElement.textContent = "沒有推薦結果";
    if (thrownThemeDisplayElement) {
      thrownThemeDisplayElement.textContent = "沒有找到命運骰子推薦結果，請重新擲骰子。";
    }
    if (recommendationContainer) {
      recommendationContainer.innerHTML =
        "<p style='text-align: center; width: 100%;'>沒有找到命運骰子推薦結果，請重新擲骰子。</p>";
    }

    setTimeout(() => {
      window.location.href = "{% url 'fate_dice' %}";
    }, 2000);
    return;
  }

  const parsed = JSON.parse(rawData);

  // 存入 localStorage 快取（下次直接用）
  localStorage.setItem("fateDiceResultCache", JSON.stringify(parsed));

  renderFateResult(parsed);

  // 渲染邏輯封裝成函式
  function renderFateResult(parsed) {
    const data = parsed.data || [];

    if (!parsed.success) {
      if (mainTitleElement) mainTitleElement.textContent = "推薦失敗";
      if (recommendationContainer) {
        recommendationContainer.innerHTML = `<p style="text-align: center; width: 100%;">推薦失敗: ${display(parsed.message)}</p>`;
      }
      return;
    }

    if (thrownThemeDisplayElement) {
      thrownThemeDisplayElement.textContent = display(parsed.message);
    }

    if (data.length === 0) {
      recommendationContainer.innerHTML =
        "<p style='text-align: center; width: 100%;'>很抱歉，沒有找到符合條件的推薦景點。</p>";
      return;
    }

    recommendationContainer.innerHTML = data
      .map(
        (d) => `
        <div class="re-result">
          <h2>${display(d.name)}</h2>
          ${d.image_url ? `<img src="${d.image_url}" alt="${display(d.name)}" style="max-width:100%; height:auto; margin-bottom: 1em;">` : ""}
          <p><strong>地址：</strong>${display(d.address)}</p>
          <p><strong>分類：</strong>${display(d.category)}</p>
          <p><strong>主題：</strong>${display(d.theme)}</p>
          <div style="text-align: center; margin-top: 1em;">
            <a href="${fate_dicedetailUrl}" class="button">查看詳情</a>
          </div>
        </div>`
      )
      .join("");
  }
});


