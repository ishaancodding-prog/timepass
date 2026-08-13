const yesBtn = document.getElementById('yes-btn');
const noBtn = document.getElementById('no-btn');

let dodges = 0;

const LINES = [
  "Think again...",
  "Are you sure?",
  "Really sure?",
  "Give it another thought!",
  "Don't do this!",
  "Wrong choice!",
  "Try again 😉"
];

// Handles the logic when dodging/hovering over the 'No' button
function dodge() {
  dodges++;

  // Update button text cycle through LINES array
  noBtn.textContent = LINES[dodges % LINES.length];

  // Grow the 'Yes' button incrementally
  yesBtn.style.setProperty('--grow', 1 + dodges * 0.08);

  // Shrink factor for the 'No' button
  const shrink = Math.max(0.4, 1 - dodges * 0.05);

  // Calculate random position on screen
  const x = Math.random() * (window.innerWidth - noBtn.offsetWidth);
  const y = Math.random() * (window.innerHeight - noBtn.offsetHeight);

  noBtn.classList.add('is-loose');
  noBtn.style.transform = `translate(${x}px, ${y}px) scale(${shrink})`;
}

// Event Listeners for Dodge action
noBtn.addEventListener('mouseover', dodge);
noBtn.addEventListener('click', dodge);

// Celebration state on clicking 'Yes'
yesBtn.addEventListener('click', () => {
  document.querySelector('.question').textContent = "Yay! See you then! 🎉";
  document.querySelector('.subtext').textContent = "Best decision ever ❤️";
  noBtn.style.display = 'none';
  yesBtn.style.setProperty('--grow', 1.2);
});
