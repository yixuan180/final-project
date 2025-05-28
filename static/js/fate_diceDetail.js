document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const id = params.get("id");

  // 從 localStorage 讀取命運骰子的快取資料
  const rawData = localStorage.getItem("fateDiceResultCache");

  const display = (value) =>
    !value || (typeof value === "object" && Object.keys(value).length === 0) ? "無" : value;

  if (!rawData) {
    document.body.innerHTML =
      "<p style='color:red;'>找不到命運骰子的快取結果，請返回重新擲骰。</p>";
    return;
  }

  const parsed = JSON.parse(rawData);
  const dataList = parsed.data || [];

  const place = dataList.find((d) => String(d.id) === String(id));


  if (!place) {
    document.body.innerHTML = "<p style='color:red;'>找不到該景點資訊，請返回重新擲骰。</p>";
    return;
  }

  // 把資料填進網頁元素
  document.getElementById("placeTitle").textContent = display(place.name);
  document.getElementById("placeImage").src = display(place.image_url);
  document.getElementById("placeImage").alt = display(place.name);
  document.getElementById("placeDescription").textContent = display(place.description);
  document.getElementById("placeAddress").textContent = display(place.address);
  document.getElementById("placeCategory").textContent = display(place.category);
  document.getElementById("placeHours").textContent = display(place.opening_hours);
  document.getElementById("placeContact").textContent = display(place.contact_info);
});

