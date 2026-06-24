import re

with open('/Users/pochoco/Desktop/원소주기율표/script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if line.startswith('function init3D(elementData)'):
        start_idx = i
    if start_idx != -1 and line.startswith('// =========================================='):
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    new_code = """
let renderInstances = {};

function init3D(elementData, containerId = 'atom-3d-container') {
  if (!window.THREE) return;
  const container = document.getElementById(containerId);
  if (!container) return;
  
  if (renderInstances[containerId]) {
    dispose3D(containerId);
  }

  const width = container.clientWidth;
  const height = container.clientHeight;
  const colorStr = getGroupColor(elementData.cat);
  const colorHex = parseInt(colorStr.replace('#', '0x'));

  let scene = new THREE.Scene();
  let camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
  camera.position.z = 35;
  let renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(window.devicePixelRatio);
  container.appendChild(renderer.domElement);

  const controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.enablePan = false;

  let atomGroup = new THREE.Group();
  scene.add(atomGroup);

  const light = new THREE.PointLight(0xffffff, 1.2, 100);
  light.position.set(20, 20, 30);
  scene.add(light);
  scene.add(new THREE.AmbientLight(0x404040));

  let electronsList = [];
  buildAtom(elementData.num, colorHex, atomGroup, electronsList);

  // Click handler for explosion
  container.onclick = () => {
    playExplosionSound();
    triggerAtomBurst(containerId);
  };

  let animationId;
  function animate() {
    animationId = requestAnimationFrame(animate);
    atomGroup.rotation.y += 0.002; 
    atomGroup.rotation.x += 0.001;
    electronsList.forEach(item => {
      item.pivot.rotation.z += item.speed;
      if (Math.abs(item.speed) > Math.abs(item.baseSpeed)) item.speed *= 0.95;
    });
    controls.update();
    renderer.render(scene, camera);
  }
  animate();

  renderInstances[containerId] = {
    scene, camera, renderer, animationId, atomGroup, electronsList
  };
}

function buildAtom(atomicNumber, colorHex, atomGroup, electronsList) {
  const clusterRadiusBase = Math.min(atomicNumber * 0.05, 3.5);
  const nucleusGroup = new THREE.Group();
  for (let i = 0; i < atomicNumber; i++) {
    const pMesh = new THREE.Mesh(new THREE.SphereGeometry(0.8, 16, 16), new THREE.MeshStandardMaterial({ color: colorHex, roughness: 0.3 }));
    pMesh.position.set((Math.random()-0.5)*clusterRadiusBase*2, (Math.random()-0.5)*clusterRadiusBase*2, (Math.random()-0.5)*clusterRadiusBase*2);
    if (pMesh.position.length() > clusterRadiusBase) pMesh.position.setLength(clusterRadiusBase);
    nucleusGroup.add(pMesh);
  }
  atomGroup.add(nucleusGroup);
  electronsList.push({ pivot: nucleusGroup, speed: 0.003, baseSpeed: 0.003 });

  let remaining = atomicNumber, shellCapacities = [2, 8, 18, 32, 32, 18, 8], currentShell = 0;
  while (remaining > 0 && currentShell < shellCapacities.length) {
    let electronsInShell = Math.min(remaining, shellCapacities[currentShell]);
    let orbitRadius = clusterRadiusBase + 4 + (currentShell * 3.5);
    const shellColor = new THREE.Color(`hsl(${(currentShell * 55) % 360}, 80%, 65%)`);
    const orbitRing = new THREE.Mesh(new THREE.RingGeometry(orbitRadius - 0.04, orbitRadius + 0.04, 64), new THREE.MeshBasicMaterial({ color: shellColor, transparent: true, opacity: 0.15, blending: THREE.AdditiveBlending, side: THREE.DoubleSide }));
    orbitRing.rotation.set((currentShell * Math.PI)/3.5, (currentShell * Math.PI)/2.5, 0);
    atomGroup.add(orbitRing);
    for (let i = 0; i < electronsInShell; i++) {
      const pivot = new THREE.Group();
      pivot.rotation.set(orbitRing.rotation.x, orbitRing.rotation.y, 0);
      const electron = new THREE.Mesh(new THREE.SphereGeometry(0.5, 32, 32), new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: shellColor, emissiveIntensity: 0.6 }));
      electron.position.set(Math.cos((i / electronsInShell) * Math.PI * 2) * orbitRadius, Math.sin((i / electronsInShell) * Math.PI * 2) * orbitRadius, 0);
      pivot.add(electron);
      atomGroup.add(pivot);
      electronsList.push({ pivot, speed: 0.02 - (currentShell * 0.002), baseSpeed: 0.02 - (currentShell * 0.002) });
    }
    remaining -= electronsInShell;
    currentShell++;
  }
}

function triggerAtomBurst(containerId = 'atom-3d-container') {
  const inst = renderInstances[containerId];
  if (!inst) return;
  inst.electronsList.forEach(item => { item.speed = 0.3 * (Math.random() > 0.5 ? 1 : -1); });
}

function dispose3D(containerId) {
  if (!containerId) {
    Object.keys(renderInstances).forEach(id => dispose3D(id));
    return;
  }
  const inst = renderInstances[containerId];
  if (inst) {
    cancelAnimationFrame(inst.animationId);
    inst.renderer.dispose();
    const container = document.getElementById(containerId);
    if (container) container.innerHTML = '';
    delete renderInstances[containerId];
  }
}

function onWindowResize() {
  Object.keys(renderInstances).forEach(containerId => {
    const inst = renderInstances[containerId];
    const container = document.getElementById(containerId);
    if (container && inst) {
      inst.camera.aspect = container.clientWidth / container.clientHeight;
      inst.camera.updateProjectionMatrix();
      inst.renderer.setSize(container.clientWidth, container.clientHeight);
    }
  });
}
window.addEventListener('resize', onWindowResize);
"""
    new_lines = lines[:start_idx] + [new_code + '\n'] + lines[end_idx:]
    with open('/Users/pochoco/Desktop/원소주기율표/script.js', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("3D rendering successfully refactored.")
else:
    print("Could not find start/end indices.")
