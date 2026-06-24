import re

filepath = '/Users/pochoco/Desktop/원소주기율표/script.js'
with open(filepath, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Replace init3D animation loop and onclick
old_animate = """  // Click handler for explosion
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
  animate();"""

new_animate = """  // Setup explosion state
  let isExploding = false;
  let explodingParts = [];

  // Click handler for explosion
  container.onclick = () => {
    if (isExploding) return; // Prevent multiple explosions
    playExplosionSound();
    isExploding = true;
    
    // Gather all spherical meshes (protons, neutrons, electrons) for explosion
    atomGroup.traverse((child) => {
      if (child.isMesh && child.geometry.type === 'SphereGeometry') {
        // Give each particle a random outward velocity
        let v = new THREE.Vector3(
          (Math.random() - 0.5) * 4,
          (Math.random() - 0.5) * 4,
          (Math.random() - 0.5) * 4
        );
        child.velocity = v;
        // Make sure material can fade
        child.material = child.material.clone();
        child.material.transparent = true;
        explodingParts.push(child);
      } else if (child.isMesh && child.geometry.type === 'RingGeometry') {
        // Hide electron orbit rings immediately
        child.visible = false;
      }
    });

    // Reset the atom after 2.5 seconds
    setTimeout(() => {
      // Clear old atom
      scene.remove(atomGroup);
      atomGroup = new THREE.Group();
      scene.add(atomGroup);
      electronsList = [];
      buildAtom(elementData.num, colorHex, atomGroup, electronsList);
      
      // Also update renderInstance reference
      if (renderInstances[containerId]) {
        renderInstances[containerId].atomGroup = atomGroup;
        renderInstances[containerId].electronsList = electronsList;
      }
      
      isExploding = false;
      explodingParts = [];
    }, 2500);
  };

  let animationId;
  function animate() {
    animationId = requestAnimationFrame(animate);
    
    if (isExploding) {
      explodingParts.forEach(p => {
        // Explode outward
        p.position.add(p.velocity);
        // Gravity
        p.velocity.y -= 0.05;
        // Fade out
        p.material.opacity *= 0.92;
      });
    } else {
      atomGroup.rotation.y += 0.002; 
      atomGroup.rotation.x += 0.001;
      electronsList.forEach(item => {
        item.pivot.rotation.z += item.speed;
        if (Math.abs(item.speed) > Math.abs(item.baseSpeed)) item.speed *= 0.95;
      });
    }

    controls.update();
    renderer.render(scene, camera);
  }
  animate();"""

js_content = js_content.replace(old_animate, new_animate)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Explosion logic injected successfully.")
