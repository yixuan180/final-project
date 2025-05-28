document.addEventListener("DOMContentLoaded", function () {
document.querySelector(".startRec button").addEventListener("click", function (event) {
    event.preventDefault();

    // 獲取地點與骰子結果
    const city = document.getElementById("datechosen").value;
    const theme = getDiceTheme();

    if (!city) {
    alert("請選擇縣市！");
    return;
    }
    if (!theme) { 
        alert("請先點擊「點擊開始」擲出旅遊主題！");
        return;
    }

    const formData = new URLSearchParams();
    formData.append("region", city);
    formData.append("theme", theme); // 雖然後端目前沒有用 theme 篩選，但保持傳遞

    fetch("http://127.0.0.1:8000/fate_dice/roll_dice/", {
    method: "POST",
    headers: {
        "Content-Type": "application/x-www-form-urlencoded", // 更改為表單數據類型
    },
    body: formData, // 直接傳遞 formData
    })
    .then((response) => {
        if (!response.ok) {
        // 處理非 2xx 響應
        return response.json().then((errorData) => {
            throw new Error(errorData.message || "Fate Dice API 請求失敗");
        });
        }
        return response.json();
    })
    .then((data) => {
        console.log("Fate Dice API 回應:", data);
        if (data.success) {
            // 同步存進 sessionStorage + localStorage
            sessionStorage.setItem("fateDiceResult", JSON.stringify(data));
            localStorage.setItem("fateDiceResultCache", JSON.stringify(data));

            // 成功獲取數據後，導向到結果頁面
            window.location.href = "./fate_diceResult.html";
        } else {
            alert("命運骰子推薦失敗: " + data.message);
        }
    })
    .catch((error) => {
        console.error("Fate Dice API 錯誤:", error);
        alert("發生錯誤: " + error.message);
    });
});
});