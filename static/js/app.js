const sidebar = document.getElementById("sidebar");
const cyclePill = document.getElementById("cycle-pill");
const chatLog = document.getElementById("chat-log");
const workspace = document.getElementById("workspace");

document.getElementById("menu-toggle").addEventListener("click", () => {
  sidebar.classList.toggle("collapsed");
});

async function getState() {
  const response = await fetch("/api/state");
  return response.json();
}

function appendChat(label, payload) {
  const line = document.createElement("div");
  line.textContent = `${label}: ${JSON.stringify(payload)}`;
  chatLog.appendChild(line);
  chatLog.scrollTop = chatLog.scrollHeight;
}

document.getElementById("send-chat").addEventListener("click", async () => {
  const input = document.getElementById("chat-input");
  const q = input.value.trim();
  if (!q) return;
  appendChat("you", q);
  const response = await fetch(`/api/chat?q=${encodeURIComponent(q)}`);
  const payload = await response.json();
  appendChat("black-origin", payload.reply);
  input.value = "";
});

const root = document.getElementById("planet-canvas");
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, root.clientWidth / root.clientHeight, 0.1, 1000);
camera.position.z = 2.8;
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(root.clientWidth, root.clientHeight);
root.appendChild(renderer.domElement);

const globe = new THREE.Mesh(
  new THREE.SphereGeometry(0.8, 32, 32),
  new THREE.MeshStandardMaterial({ color: 0x1f58ff, wireframe: true })
);
scene.add(globe);
const light = new THREE.PointLight(0xffffff, 1.3, 100);
light.position.set(2, 3, 4);
scene.add(light);

const nodeGroup = new THREE.Group();
scene.add(nodeGroup);

function renderNodes(nodes) {
  while (nodeGroup.children.length) nodeGroup.remove(nodeGroup.children[0]);
  nodes.slice(0, 18).forEach((node, i) => {
    const m = new THREE.Mesh(new THREE.SphereGeometry(0.03, 8, 8), new THREE.MeshBasicMaterial({ color: 0xffa14d }));
    const angle = (i / Math.max(nodes.length, 1)) * Math.PI * 2;
    m.position.set(Math.cos(angle) * 1.15, Math.sin(angle * 2) * 0.3, Math.sin(angle) * 1.15);
    nodeGroup.add(m);
  });
}

async function refresh() {
  const state = await getState();
  cyclePill.textContent = `Cycle ${state.kernel.cycle}`;
  workspace.textContent = JSON.stringify({
    topics: state.planetary_index.topics,
    causalLinks: state.causal_graph.links.slice(-3),
    prediction: state.world_model.predictions.slice(-1)[0] || null,
    improvements: state.research_memory.improvements.slice(-2)
  }, null, 2);
  renderNodes(state.planetary_graph.nodes || []);
}

function animate() {
  requestAnimationFrame(animate);
  globe.rotation.y += 0.005;
  nodeGroup.rotation.y -= 0.003;
  renderer.render(scene, camera);
}
animate();
refresh();
setInterval(refresh, 4000);
