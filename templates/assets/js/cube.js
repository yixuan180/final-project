<<<<<<< HEAD
let currentX = 0;
let currentY = 0;

=======
>>>>>>> yvonne
document.querySelector(".startButton").addEventListener("click", () => {
  const cube = document.querySelector(".cube");
  const resultLabel = document.getElementById("resultLabel");

  resultLabel.classList.remove("show");

<<<<<<< HEAD
  const faceList = [
    { face: "front", x: 0, y: 0, result: "美食" },
    { face: "back", x: 0, y: 180, result: "自然風景" },
    { face: "left", x: 0, y: 90, result: "冒險活動" },
    { face: "right", x: 0, y: -90, result: "文化歷史" },
    { face: "top", x: 90, y: 0, result: "購物娛樂" },
    { face: "bottom", x: -90, y: 0, result: "休閒放鬆" },
  ];

  const chosen = faceList[Math.floor(Math.random() * faceList.length)];

  currentX += 1080 + chosen.x;
  currentY += 1080 + chosen.y;

  currentX %= 360 * 6;
  currentY %= 360 * 6;

  cube.style.transition = "transform 5s ease-in-out";
  cube.style.transform = `rotateX(${currentX}deg) rotateY(${currentY}deg)`;

  setTimeout(() => {
    resultLabel.textContent = `${chosen.result}`;
=======
  const randX = Math.floor(Math.random() * 4) * 90 + 360 * 3;
  const randY = Math.floor(Math.random() * 4) * 90 + 360 * 3;

  cube.style.transition = "transform 5s ease-in-out";
  cube.style.transform = `rotateX(${randX}deg) rotateY(${randY}deg)`;

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
>>>>>>> yvonne
    resultLabel.classList.add("show");
  }, 5000);
});
