document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const id = params.get("id");

  const rawData = localStorage.getItem("fateDiceResultCache");

  const display = (value) =>
    !value || (typeof value === "object" && Object.keys(value).length === 0)
      ? "無"
      : value;

  if (!rawData) {
    document.body.innerHTML =
      "<p style='color:red;'>找不到命運骰子的快取結果，請返回重新擲骰。</p>";
    return;
  }

  const parsed = JSON.parse(rawData);
  const dataList = parsed.data || [];

  const place = dataList.find((d) => String(d.id) === String(id));

  if (!place) {
    document.body.innerHTML =
      "<p style='color:red;'>找不到該景點資訊，請返回重新擲骰。</p>";
    return;
  }

  // 填資料
  document.getElementById("placeTitle").textContent = display(place.name);
  document.getElementById("placeImage").src = display(place.image_url);
  document.getElementById("placeImage").alt = display(place.name);
  document.getElementById("placeDescription").textContent = display(place.description);
  document.getElementById("placeAddress").textContent = display(place.address);
  document.getElementById("placeCategory").textContent = display(place.category);
  document.getElementById("placeHours").textContent = display(place.opening_hours);
  document.getElementById("placeContact").textContent = display(place.contact_info);

  // 初始化地圖
  const map = L.map("map").setView([23.6978, 120.9605], 7); // 台灣中心點
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> 貢獻者',
  }).addTo(map);

  function cleanAddress(address) {
  // 移除門牌號（14-1號、88號）
  let result = address.replace(/\d+(-\d+)?號?/g, "");
  // 移除「幾鄰」像 11鄰、14-1鄰
  result = result.replace(/\d+(-\d+)?鄰/g, "");
  // 移除單獨的「鄰」字（沒有數字）
  result = result.replace(/鄰/g, "");
  // 移除單獨的「巷」字（沒有數字）
  result = result.replace(/巷/g, "");
  // 移除單獨的「弄」字（沒有數字）
  result = result.replace(/弄/g, "");
  // 移除單獨的「之」字（沒有數字）
  result = result.replace(/之/g, "");
  return result.trim();
  }

  // 智能查詢地圖函式
  function smartGeocode(address, placeName) {
    fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.length > 0) {
          const { lat, lon, display_name } = data[0];
          map.setView([lat, lon], 15);
          L.marker([lat, lon])
            .addTo(map)
            .bindPopup(`<b>${placeName}</b><br>${display_name}`)
            .openPopup();
        } else {
          const fallback = cleanAddress(address);
          if (fallback !== address) {
            console.warn("第一次找不到位置，改用簡化地址再查一次：", fallback);
            smartGeocode(fallback, placeName);
          } else {
            console.warn("❌ 地址查不到，也無法再簡化：", address);
          }
        }
      })
      .catch((err) => {
        console.error("❌ 查詢地圖時發生錯誤：", err);
      });
  }

  // 啟動地圖定位查詢
  const address = display(place.address);
  if (address && address !== "無") {
    smartGeocode(address, place.name);
  } else {
    console.warn("❌ 地址為空，無法標示地圖");
  }
});
