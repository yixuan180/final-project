document.querySelector(".startButton").addEventListener("click", () => {
  const cube = document.querySelector(".cube");
  const resultLabel = document.getElementById("resultLabel");

  // 先隱藏結果
  resultLabel.classList.remove("show");

  // 隨機旋轉（每 90 度一次）
  const randX = Math.floor(Math.random() * 4) * 90 + 360 * 3;
  const randY = Math.floor(Math.random() * 4) * 90 + 360 * 3;

  cube.style.transition = "transform 5s ease-in-out";
  cube.style.transform = `rotateX(${randX}deg) rotateY(${randY}deg)`;

  // 對應結果（根據角度決定）
  const face = [
    { x: 0, y: 0, label: "美食之旅" }, // front
    { x: 0, y: 180, label: "懷舊古都" }, // back
    { x: 0, y: -90, label: "自然山林" }, // right
    { x: 0, y: 90, label: "浪漫海濱" }, // left
    { x: 90, y: 0, label: "人文探索" }, // top
    { x: -90, y: 0, label: "未知冒險" }, //bottom
  ];
  const randomResult = Math.floor(Math.random() * themes.length);

  // 等待 5 秒後顯示結果
  setTimeout(() => {
    resultLabel.textContent = face[randomResult];
    resultLabel.classList.add("show");
  }, 5000);
});
