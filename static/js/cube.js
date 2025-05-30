let currentX = 0;
let currentY = 0;
let currentDiceTheme = "";

document.querySelector(".startButton").addEventListener("click", () => {
  const cube = document.querySelector(".cube");
  const resultLabel = document.getElementById("resultLabel");

  const results = [
    "美食之旅",
    "自然風景",
    "文化歷史",
    "冒險活動",
    "購物娛樂",
    "休閒放鬆",
  ];
  const rotations = [
    { x: 0, y: 0 },
    { x: 0, y: 180 },
    { x: 0, y: -90 },
    { x: 0, y: 90 },
    { x: -90, y: 0 },
    { x: 90, y: 0 },
  ];

  const randomIndex = Math.floor(Math.random() * 6);
  const result = results[randomIndex];
  const rotation = rotations[randomIndex];

  currentDiceTheme = result;

  const baseX = rotation.x;
  const baseY = rotation.y;
  const spinX = 1080;
  const spinY = 1080;
  cube.style.transition = "none";
  cube.style.transform = `rotateX(0deg) rotateY(0deg)`;

  resultLabel.classList.remove("show");
  resultLabel.textContent = "";

  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      cube.style.transition = "transform 2s ease-in-out";
      cube.style.transform = `rotateX(${spinX + baseX}deg) rotateY(${
        spinY + baseY
      }deg)`;
    });
  });

  setTimeout(() => {
    resultLabel.textContent = result;
    void resultLabel.offsetWidth;
    resultLabel.classList.add("show");
  }, 2100);
});

function getDiceTheme() {
    return currentDiceTheme;
}

