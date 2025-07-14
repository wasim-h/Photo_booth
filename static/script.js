const video = document.getElementById("video");
const overlay = document.getElementById("countdown");
const canvases = [
  document.getElementById("canvas1"),
  document.getElementById("canvas2"),
  document.getElementById("canvas3"),
];
const ctxs = canvases.map(c => c.getContext("2d"));
let selectedFilter = "none";
let photoCount = 0;

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
    video.play();
  })
  .catch(err => {
    alert("Camera access denied. Please allow webcam permission.");
    console.error("Camera error:", err);
  });

document.querySelectorAll(".filter-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    selectedFilter = btn.dataset.filter;
    video.style.filter = selectedFilter;
  });
});

document.getElementById("snap-btn").addEventListener("click", async () => {
  if (photoCount >= 3) {
    alert("You've already taken 3 photos.");
    return;
  }

  for (let i = photoCount; i < 3; i++) {
    for (let j = 3; j > 0; j--) {
      overlay.textContent = j;
      overlay.style.display = "block";
      await new Promise(r => setTimeout(r, 500));
    }
    overlay.style.display = "none";
    capturePhoto();
    await new Promise(r => setTimeout(r, 2000));
  }

  uploadPhotos();
});

function capturePhoto() {
  if (photoCount >= 3) return;
  const ctx = ctxs[photoCount];
  const canvas = canvases[photoCount];
  ctx.filter = selectedFilter;
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  canvas.classList.add("visible");
  photoCount++;
}

function uploadPhotos() {
  const formData = new FormData();
  let blobCount = 0;

  canvases.forEach((canvas, i) => {
    canvas.toBlob((blob) => {
      formData.append(`image${i + 1}`, blob, `photo${i + 1}.png`);
      blobCount++;

      if (blobCount === 3) {
        fetch("/upload", {
          method: "POST",
          body: formData,
        })
        .then((res) => res.url)
        .then((redirectURL) => {
          window.location.href = redirectURL;
        });
      }
    }, "image/png");
  });
}
