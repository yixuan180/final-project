document.addEventListener("DOMContentLoaded", function () {
  const itineraryDataString = sessionStorage.getItem("itineraryData");
  const itineraryMessage = sessionStorage.getItem("itineraryMessage");
  const resultContainer = document.getElementById("resultContainer");
  const resultHeaderP = document.querySelector("#main header p");

  if (resultHeaderP) {
    if (itineraryMessage) {
      resultHeaderP.innerHTML = `<i class="fa-solid fa-location-dot"></i>&nbsp;${itineraryMessage}`;
    } else {
      resultHeaderP.innerHTML = `<i class="fa-solid fa-location-dot"></i>&nbsp;這是您的客製化行程`;
    }
  }

  if (itineraryDataString && resultContainer) {
    try {
      const itineraryData = JSON.parse(itineraryDataString);
      console.log("從 sessionStorage 讀取的行程資料:", itineraryData);

      if (Array.isArray(itineraryData) && itineraryData.length > 0) {
        itineraryData.forEach((dayPlan, index) => {
          const dayBox = document.createElement("div");
          dayBox.classList.add("re-result"); 

          dayBox.innerHTML = `<h2>${dayPlan.day || `第 ${index + 1} 天`}</h2>`;
          dayBox.innerHTML += `<hr class="day-divider" />`;

          // 輔助函數：解析並格式化時間段內容
          const formatTimeSlot = (timeSlotContent) => {
            if (!timeSlotContent) return '';

            let htmlContent = '<ul class="activity-list">';

            // 解析景點名稱和說明
            const parts = timeSlotContent.split('. ');
            
            parts.forEach(part => {
                if (part.trim() === '') return; 

                let displayPart = part.trim();
                let feeMatch = displayPart.match(/\(([^)]*?元|免費)\)/);

                let feeInfo = '';
                if (feeMatch) {
                    feeInfo = ` <span class="fee-info">${feeMatch[0]}</span>`;
                    displayPart = displayPart.replace(feeMatch[0], '').trim(); 
                }

                // 嘗試提取地點
                let locationMatch = displayPart.match(/前往([^，、。]*?)，/);
                let location = '';
                if (locationMatch && locationMatch[1].length < 20) { 
                    location = `<strong>${locationMatch[1].trim()}</strong>：`;
                    displayPart = displayPart.replace(`前往${locationMatch[1].trim()}，`, '').trim();
                } else {
                    location = '';
                }

                htmlContent += `<li>${location}${displayPart}${feeInfo}</li>`;
            });

            htmlContent += '</ul>';
            return htmlContent;
          };

          // 早上
          if (dayPlan.morning) {
            dayBox.innerHTML += `<div class="time-slot"><h3>早上：</h3>${formatTimeSlot(dayPlan.morning)}</div>`;
          }
          // 中午
          if (dayPlan.afternoon) {
            dayBox.innerHTML += `<div class="time-slot"><h3>中午：</h3>${formatTimeSlot(dayPlan.afternoon)}</div>`;
          }
          // 晚上
          if (dayPlan.evening) {
            dayBox.innerHTML += `<div class="time-slot"><h3>晚上：</h3>${formatTimeSlot(dayPlan.evening)}</div>`;
          }

          if (!dayPlan.morning && !dayPlan.afternoon && !dayPlan.evening) {
            dayBox.innerHTML += "<p>這一天沒有詳細行程安排。</p>";
          }

          resultContainer.appendChild(dayBox);
        });
      } else {
        resultContainer.innerHTML = "<p>很抱歉，根據您的偏好條件，未能生成推薦行程。</p>";
        if (resultHeaderP) {
          resultHeaderP.innerHTML = `<i class="fa-solid fa-circle-exclamation"></i>&nbsp;未找到符合條件的行程`;
        }
      }
    } catch (error) {
      console.error("解析行程資料時發生錯誤:", error);
      if (resultContainer) {
        resultContainer.innerHTML = "<p>載入行程時發生錯誤，請稍後再試。</p>";
      }
      if (resultHeaderP) {
        resultHeaderP.innerHTML = `<i class="fa-solid fa-times-circle"></i>&nbsp;資料載入失敗`;
      }
    }
  } else {
    if (resultContainer) {
      resultContainer.innerHTML = "<p>沒有找到行程資料，請返回智慧旅行排程頁面重新排程。</p>";
    }
    if (resultHeaderP) {
      resultHeaderP.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i>&nbsp;行程生成失敗`;
    }
  }

  sessionStorage.removeItem("plannerRequestData");
  sessionStorage.removeItem("itineraryData");
  sessionStorage.removeItem("itineraryMessage");
});