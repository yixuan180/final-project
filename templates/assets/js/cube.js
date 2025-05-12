let currentX = 0;
let currentY = 0;

document.querySelector(".startButton").addEventListener("click", () => {
  const cube = document.querySelector(".cube");
  const resultLabel = document.getElementById("resultLabel");

  resultLabel.classList.remove("show");

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
    resultLabel.classList.add("show");
  }, 5000);
});
