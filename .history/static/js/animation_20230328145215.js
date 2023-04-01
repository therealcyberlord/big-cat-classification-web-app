// Get the canvas element and its 2D context
const canvas = document.getElementById("tiger-canvas");
const ctx = canvas.getContext("2d");

// Set the canvas dimensions to match the window size
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Load the tiger image
const img = new Image();
img.src = "path/to/tiger/image.png";

// Set the initial position of the tiger
let x = -img.width;
let y = canvas.height - img.height;

// Set the speed and direction of the tiger
const speed = 5;
let direction = 1;

// Draw the tiger at its current position
function draw() {
  // Clear the canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw the tiger image
  ctx.drawImage(img, x, y);

  // Move the tiger
  x += speed * direction;

  // Reverse the direction if the tiger goes offscreen
  if (x > canvas.width || x < -img.width) {
    direction *= -1;
  }

  // Request a new frame of animation
  requestAnimationFrame(draw);
}

// Start the animation
img.onload = draw;
