document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const id = params.get("id");

  const data = JSON.parse(localStorage.getItem("emotionResults") || "[]");
  const place = data.find((d) => d.id === id);

  const display = (value) =>
    !value || (typeof value === "object" && Object.keys(value).length === 0) ? "無" : value;

  if (place) {
    document.getElementById("placeTitle").textContent = display(place.name);
    document.getElementById("placeImage").src = display(place.image_url);
    document.getElementById("placeImage").alt = display(place.name);
    document.getElementById("placeDescription").textContent = display(place.description);
    document.getElementById("placeAddress").textContent = display(place.address);
    document.getElementById("placeCategory").textContent = display(place.category);
    document.getElementById("placeHours").textContent = display(place.opening_hours);
    document.getElementById("placeContact").textContent = display(place.contact_info);

    const placeImage = document.getElementById("placeImage");
    if (!place.image_url || place.image_url.trim() === "" ) {
      placeImage.style.display = "none";
    } else {
      placeImage.style.display = "block";
    }
  } else {
    document.body.innerHTML = "<p style='color:red;'>找不到該景點資訊，請重新操作。</p>";
  }
});


