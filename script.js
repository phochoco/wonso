/* global elementsData */

const ptable = document.getElementById('ptable');
const groupRow = document.getElementById('groupRow');
const periodCol = document.getElementById('periodCol');
const fblockGrid = document.getElementById('fblockGrid');
const modalOverlay = document.getElementById('modalOverlay');
const modalBody = document.getElementById('modalBody');
const searchInput = document.getElementById('searchInput');
const clearBtn = document.getElementById('clearBtn');

let currentFilter = 'all';
let audioCtx;

// 3D Rendering Global Variables
let scene, camera, renderer, atomGroup, animationId;
let electronsList = [];
let initTimeout;

const viewGridBtn = document.getElementById('view-grid-btn');
const viewListBtn = document.getElementById('view-list-btn');
const listViewContainer = document.getElementById('listViewContainer');
const tableScroll = document.querySelector('.table-scroll');
const listTbody = document.getElementById('listTbody');
const compareToggle = document.getElementById('compare-mode-toggle');

let isListView = false;
let isCompareMode = false;
let currentSortCol = 'num';
let sortAsc = true;

if (viewGridBtn && viewListBtn) {
  viewGridBtn.addEventListener('click', () => {
    isListView = false;
    viewGridBtn.classList.add('active');
    viewListBtn.classList.remove('active');
    tableScroll.style.display = 'block';
    listViewContainer.style.display = 'none';
  });
  viewListBtn.addEventListener('click', () => {
    isListView = true;
    viewListBtn.classList.add('active');
    viewGridBtn.classList.remove('active');
    tableScroll.style.display = 'none';
    listViewContainer.style.display = 'block';
    renderList();
  });
}

if (compareToggle) {
  compareToggle.addEventListener('change', (e) => {
    isCompareMode = e.target.checked;
    // Reset selections
    document.querySelectorAll('.el-card').forEach(c => {
      c.style.boxShadow = '';
      c.style.transform = '';
    });
    compareSelection = [];
  });
}

function initAudio() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
  if (audioCtx.state === 'suspended') {
    audioCtx.resume();
  }
}

function playCardClickSound() {
  initAudio();
  const osc = audioCtx.createOscillator();
  const gainNode = audioCtx.createGain();
  
  osc.type = 'sine';
  osc.frequency.setValueAtTime(800, audioCtx.currentTime);
  osc.frequency.exponentialRampToValueAtTime(2000, audioCtx.currentTime + 0.1);
  
  gainNode.gain.setValueAtTime(0, audioCtx.currentTime);
  gainNode.gain.linearRampToValueAtTime(0.08, audioCtx.currentTime + 0.02);
  gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.15);
  
  osc.connect(gainNode);
  gainNode.connect(audioCtx.destination);
  
  osc.start();
  osc.stop(audioCtx.currentTime + 0.2);
}

function playExplosionSound() {
  initAudio();
  const bufferSize = audioCtx.sampleRate * 0.6;
  const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
  const data = buffer.getChannelData(0);
  for (let i = 0; i < bufferSize; i++) {
    data[i] = Math.random() * 2 - 1;
  }
  
  const noiseSource = audioCtx.createBufferSource();
  noiseSource.buffer = buffer;
  
  const filter = audioCtx.createBiquadFilter();
  filter.type = 'lowpass';
  filter.frequency.setValueAtTime(1500, audioCtx.currentTime);
  filter.frequency.exponentialRampToValueAtTime(100, audioCtx.currentTime + 0.6);
  
  const gainNode = audioCtx.createGain();
  gainNode.gain.setValueAtTime(0.25, audioCtx.currentTime);
  gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.6);
  
  noiseSource.connect(filter);
  filter.connect(gainNode);
  gainNode.connect(audioCtx.destination);
  
  noiseSource.start();
}

const tempSlider = document.getElementById('temp-slider');
const tempKVal = document.getElementById('temp-k-val');
const tempCVal = document.getElementById('temp-c-val');
let tempUpdateTicking = false;

if (tempSlider) {
  tempSlider.addEventListener('input', (e) => {
    const k = parseInt(e.target.value);
    const c = k - 273;
    tempKVal.textContent = k;
    tempCVal.textContent = c;
    
    if (!tempUpdateTicking) {
      window.requestAnimationFrame(() => {
        updateElementsState(k);
        tempUpdateTicking = false;
      });
      tempUpdateTicking = true;
    }
  });
}

function updateElementsState(kelvin) {
  document.querySelectorAll('.el-card:not(.el-placeholder)').forEach(card => {
    const num = parseInt(card.dataset.num);
    const el = elementsData.find(e => e.num === num);
    if (!el) return;
    
    card.classList.remove('state-solid', 'state-liquid', 'state-gas', 'state-unknown');
    const dot = card.querySelector('.el-state-dot');
    if (dot) dot.className = 'el-state-dot'; // reset
    
    if (el.melt === null && el.boil === null) {
      card.classList.add('state-unknown');
      if (dot) dot.classList.add('unknown');
      return;
    }

    if (el.boil !== null && kelvin >= el.boil) {
      card.classList.add('state-gas');
      if (dot) dot.classList.add('gas');
    } else if (el.melt !== null && kelvin >= el.melt) {
      card.classList.add('state-liquid');
      if (dot) dot.classList.add('liquid');
    } else {
      card.classList.add('state-solid');
      if (dot) dot.classList.add('solid');
    }
  });
}

function initStars() {
  const starsContainer = document.getElementById('stars');
  for (let i = 0; i < 150; i++) {
    const star = document.createElement('div');
    star.className = 'star';
    const size = Math.random() * 2 + 1;
    star.style.width = `${size}px`;
    star.style.height = `${size}px`;
    star.style.left = `${Math.random() * 100}%`;
    star.style.top = `${Math.random() * 100}%`;
    star.style.setProperty('--dur', `${Math.random() * 3 + 2}s`);
    star.style.setProperty('--delay', `${Math.random() * 5}s`);
    star.style.setProperty('--op', `${Math.random() * 0.5 + 0.3}`);
    starsContainer.appendChild(star);
  }
}

function initLabels() {
  // Group labels 1-18
  for (let i = 1; i <= 18; i++) {
    const el = document.createElement('div');
    el.className = 'group-label';
    el.textContent = i;
    groupRow.appendChild(el);
  }
  // Period labels 1-7
  for (let i = 1; i <= 7; i++) {
    const el = document.createElement('div');
    el.className = 'period-label';
    el.textContent = i;
    periodCol.appendChild(el);
  }
  // f-block labels
  const f1 = document.createElement('div');
  f1.className = 'fblock-period-label'; f1.textContent = '6';
  const f2 = document.createElement('div');
  f2.className = 'fblock-period-label'; f2.textContent = '7';
  fblockGrid.appendChild(f1);
  // We'll append elements then handle grid placement in CSS/JS
}

function renderTable() {
  // Clear grids
  ptable.innerHTML = '';
  fblockGrid.innerHTML = '';
  // Re-add f-block period labels
  const f1 = document.createElement('div');
  f1.className = 'fblock-period-label'; f1.textContent = '6';
  f1.style.gridColumn = '1'; f1.style.gridRow = '1';
  fblockGrid.appendChild(f1);
  const f2 = document.createElement('div');
  f2.className = 'fblock-period-label'; f2.textContent = '7';
  f2.style.gridColumn = '1'; f2.style.gridRow = '2';
  fblockGrid.appendChild(f2);

  // Add placeholders for Lanthanide / Actinide in main table
  const laPlaceholder = document.createElement('div');
  laPlaceholder.className = 'el-placeholder';
  laPlaceholder.style.gridColumn = '3';
  laPlaceholder.style.gridRow = '6';
  laPlaceholder.innerHTML = '57-71<br>La-Lu';
  ptable.appendChild(laPlaceholder);

  const acPlaceholder = document.createElement('div');
  acPlaceholder.className = 'el-placeholder';
  acPlaceholder.style.gridColumn = '3';
  acPlaceholder.style.gridRow = '7';
  acPlaceholder.innerHTML = '89-103<br>Ac-Lr';
  ptable.appendChild(acPlaceholder);

  // Render elements
  elementsData.forEach(el => {
    const card = document.createElement('div');
    card.className = 'el-card';
    card.dataset.cat = el.cat;
    card.dataset.num = el.num;
    
    let isFblock = el.group === 'fblock';

    if (!isFblock) {
      card.style.gridColumn = el.group;
      card.style.gridRow = el.period;
      ptable.appendChild(card);
    } else {
      let col = (el.num >= 57 && el.num <= 71) ? el.num - 57 + 2 : el.num - 89 + 2;
      let row = el.period === 6 ? 1 : 2;
      card.style.gridColumn = col;
      card.style.gridRow = row;
      fblockGrid.appendChild(card);
    }

    // Inner HTML for card
    card.innerHTML = `
      <div class="el-number">${el.num}</div>
      <div class="el-state-dot ${el.state}"></div>
      <div class="el-symbol">${el.sym}</div>
      <div class="el-name-kr">${el.nameKr}</div>
      <div class="el-name-en">${el.nameEn}</div>
      <div class="el-mass">${el.mass}</div>
    `;

    card.addEventListener('click', () => openModal(el));
  });
}

function renderLegend() {
  const legendCont = document.getElementById('legend');
  const cats = [
    {id: 'alkali-metal', name: '알칼리 금속'},
    {id: 'alkaline-earth', name: '알칼리 토금속'},
    {id: 'transition-metal', name: '전이 금속'},
    {id: 'post-transition', name: '전이 후 금속'},
    {id: 'metalloid', name: '준금속'},
    {id: 'nonmetal', name: '비금속'},
    {id: 'halogen', name: '할로겐'},
    {id: 'noble-gas', name: '비활성 기체'},
    {id: 'lanthanide', name: '란타넘족'},
    {id: 'actinide', name: '악티늄족'}
  ];
  let html = '';
  cats.forEach(c => {
    html += `<div class="legend-item">
      <div class="legend-dot" data-cat="${c.id}"></div>
      <span>${c.name}</span>
    </div>`;
  });
  html += `<div style="width: 1px; height: 12px; background: rgba(255,255,255,0.2); margin: 0 10px;"></div>`;
  html += `
    <div class="legend-state"><div class="legend-dot-circle gas"></div>기체</div>
    <div class="legend-state"><div class="legend-dot-circle liquid"></div>액체</div>
    <div class="legend-state"><div class="legend-dot-circle solid"></div>고체</div>
  `;
  legendCont.innerHTML = html;
  
  // Apply bg colors to dots based on CSS vars
  document.querySelectorAll('.legend-dot').forEach(dot => {
    const cat = dot.dataset.cat;
    dot.style.background = `var(--c-${cat.replace('-metal','').replace('alkaline-earth','earth').replace('post-transition','post').replace('noble-gas','noble').replace('lanthanide','lantha')})`;
    if(cat === 'nonmetal') dot.style.background = 'var(--c-nonmetal)';
    if(cat === 'halogen') dot.style.background = 'var(--c-halogen)';
    if(cat === 'actinide') dot.style.background = 'var(--c-actinide)';
  });
}

function getGroupColor(cat) {
  const varName = `--c-${cat.replace('-metal','').replace('alkaline-earth','earth').replace('post-transition','post').replace('noble-gas','noble').replace('lanthanide','lantha')}`;
  let color = getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
  if(!color) {
    if(cat === 'nonmetal') color = 'var(--c-nonmetal)';
    else if(cat === 'halogen') color = 'var(--c-halogen)';
    else if(cat === 'actinide') color = 'var(--c-actinide)';
    else color = '#4dabf7';
  }
  return color;
}

let compareSelection = [];

function openCompareModal(el1, el2) {
  const modalOverlay = document.getElementById('modalOverlay');
  const compareBox = document.getElementById('compareModalBox');
  const compareContainer = document.getElementById('compareContainer');
  const modalBox = document.getElementById('modalBox');

  modalBox.style.display = 'none';
  compareBox.style.display = 'block';

  const catColor1 = getGroupColor(el1.cat);
  const catColor2 = getGroupColor(el2.cat);
  let catName1 = document.querySelector(`.fb[data-cat="${el1.cat}"]`)?.textContent.split(' ')[0] || '분류 없음';
  let catName2 = document.querySelector(`.fb[data-cat="${el2.cat}"]`)?.textContent.split(' ')[0] || '분류 없음';

  compareContainer.innerHTML = `
    <div class="compare-split">
      <div class="compare-side">
        <h2 style="color: ${catColor1}; margin-bottom: -5px;">${el1.sym} - ${el1.nameKr}</h2>
        <span class="cat-badge" style="color: ${catColor1}; border: 1px solid ${catColor1}; padding: 3px 10px; border-radius: 12px; font-size: 0.7rem; align-self: flex-start;">${catName1}</span>
        <div class="compare-3d-container" id="compare-3d-1"></div>
        <table class="compare-table">
          <tr><td>원자번호</td><td>${el1.num}</td></tr>
          <tr><td>원자량</td><td>${el1.mass}</td></tr>
          <tr><td>밀도</td><td>${el1.density !== null ? el1.density + ' g/cm³' : '-'}</td></tr>
          <tr><td>녹는점</td><td>${el1.melt !== null ? el1.melt + ' K' : '-'}</td></tr>
          <tr><td>끓는점</td><td>${el1.boil !== null ? el1.boil + ' K' : '-'}</td></tr>
          <tr><td>전기음성도</td><td>${el1.electronegativity !== null ? el1.electronegativity : '-'}</td></tr>
        </table>
      </div>
      <div class="compare-side">
        <h2 style="color: ${catColor2}; margin-bottom: -5px;">${el2.sym} - ${el2.nameKr}</h2>
        <span class="cat-badge" style="color: ${catColor2}; border: 1px solid ${catColor2}; padding: 3px 10px; border-radius: 12px; font-size: 0.7rem; align-self: flex-start;">${catName2}</span>
        <div class="compare-3d-container" id="compare-3d-2"></div>
        <table class="compare-table">
          <tr><td>원자번호</td><td>${el2.num}</td></tr>
          <tr><td>원자량</td><td>${el2.mass}</td></tr>
          <tr><td>밀도</td><td>${el2.density !== null ? el2.density + ' g/cm³' : '-'}</td></tr>
          <tr><td>녹는점</td><td>${el2.melt !== null ? el2.melt + ' K' : '-'}</td></tr>
          <tr><td>끓는점</td><td>${el2.boil !== null ? el2.boil + ' K' : '-'}</td></tr>
          <tr><td>전기음성도</td><td>${el2.electronegativity !== null ? el2.electronegativity : '-'}</td></tr>
        </table>
      </div>
    </div>
  `;

  modalOverlay.classList.add('open');
  document.body.style.overflow = 'hidden';

  setTimeout(() => {
    init3D(el1, 'compare-3d-1');
    init3D(el2, 'compare-3d-2');
  }, 300);
}

function openModal(el) {
  if (isCompareMode) {
    playCardClickSound();
    const card = document.querySelector(`.el-card[data-num="${el.num}"]`);
    if (compareSelection.find(e => e.num === el.num)) return; // already selected
    
    compareSelection.push(el);
    card.style.boxShadow = '0 0 0 3px #fff, 0 0 20px #fff';
    card.style.transform = 'scale(1.1)';
    
    if (compareSelection.length === 2) {
      openCompareModal(compareSelection[0], compareSelection[1]);
      // reset selection visually
      document.querySelectorAll('.el-card').forEach(c => {
        c.style.boxShadow = '';
        c.style.transform = '';
      });
      compareSelection = [];
    }
    return;
  }

  playCardClickSound();
  
  const modalBox = document.getElementById('modalBox');
  const compareBox = document.getElementById('compareModalBox');
  if (modalBox) modalBox.style.display = 'block';
  if (compareBox) compareBox.style.display = 'none';

  const catColor = getGroupColor(el.cat);
  const stateKr = el.state === 'gas' ? '기체' : el.state === 'liquid' ? '액체' : el.state === 'solid' ? '고체' : '불명';
  let catName = document.querySelector(`.fb[data-cat="${el.cat}"]`)?.textContent.split(' ')[0] || '분류 없음';

  const html = `
    <div id="atom-3d-container">
      <div class="atom-hint">마우스/터치로 드래그하여 회전, 휠로 확대/축소</div>
    </div>
    <div class="modal-header">
      <div class="modal-symbol-block" style="--modal-color: ${catColor}; --modal-glow: color-mix(in srgb, ${catColor} 30%, transparent);">
        <div class="modal-number">${el.num}</div>
        <div class="modal-sym">${el.sym}</div>
        <div class="modal-names">
          <div class="modal-name-kr">${el.nameKr}</div>
          <div class="modal-name-en">${el.nameEn}</div>
        </div>
        <div class="modal-mass-small">${el.mass}</div>
      </div>
      <div class="modal-info">
        <h2 class="modal-title-kr">${el.nameKr}</h2>
        <div class="modal-title-en">${el.nameEn} (Element ${el.num})</div>
        <div class="modal-cat-badge" style="--modal-color: ${catColor};">${catName}</div>
        <div class="modal-meta">
          <span class="meta-chip">상태 <strong>${stateKr}</strong></span>
          <span class="meta-chip">족/주기 <strong>${el.group === 'fblock' ? '-' : el.group + '족'} ${el.period}주기</strong></span>
          <span class="meta-chip">녹는점 <strong>${el.melt !== null ? el.melt+'K' : '불명'}</strong></span>
          <span class="meta-chip">끓는점 <strong>${el.boil !== null ? el.boil+'K' : '불명'}</strong></span>
          <span class="meta-chip">밀도 <strong>${el.density !== null ? el.density + ' g/cm³' : '불명'}</strong></span>
          <span class="meta-chip">전기음성도 <strong>${el.electronegativity !== null ? el.electronegativity : '불명'}</strong></span>
          <span class="meta-chip">전자 배치 <strong>${el.electron_config || '불명'}</strong></span>
        </div>
      </div>
    </div>
    <div class="modal-desc">${el.desc}</div>
    <div class="modal-section">
      <div class="modal-section-title">💡 재미있는 사실</div>
      <div class="modal-fact" style="--modal-color: ${catColor};">${el.fact}</div>
    </div>
    <div class="modal-section">
      <div class="modal-section-title">🛠️ 실생활 쓰임새</div>
      <div class="modal-use-container">
        <div class="use-3d-card" style="--modal-color: ${catColor};">
          <div class="use-emoji">${el.emoji || '🧪'}</div>
        </div>
        <div class="modal-use">
          ${el.use.split(',').map(u => `<span class="use-tag">${u.trim()}</span>`).join('')}
        </div>
      </div>
    </div>
    
    <details class="advanced-data-accordion" style="--modal-color: ${catColor};">
      <summary class="accordion-summary">🔬 심화 화학·역사 정보 열람</summary>
      <div class="accordion-content">
        ${el.summary ? `<p class="advanced-summary">${el.summary}</p>` : ''}
        <div class="advanced-grid">
          <div class="adv-item">
            <span class="adv-label">발견자</span>
            <span class="adv-value">${el.discovered_by || '불명'}</span>
          </div>
          <div class="adv-item">
            <span class="adv-label">명명자</span>
            <span class="adv-value">${el.named_by || '불명'}</span>
          </div>
          <div class="adv-item">
            <span class="adv-label">외형(겉보기)</span>
            <span class="adv-value">${el.appearance || '불명'}</span>
          </div>
          <div class="adv-item">
            <span class="adv-label">몰 열용량</span>
            <span class="adv-value">${el.molar_heat !== null ? el.molar_heat + ' J/(mol·K)' : '불명'}</span>
          </div>
          <div class="adv-item">
            <span class="adv-label">전자 친화도</span>
            <span class="adv-value">${el.electron_affinity !== null ? el.electron_affinity + ' kJ/mol' : '불명'}</span>
          </div>
          <div class="adv-item">
            <span class="adv-label">제1 이온화 에너지</span>
            <span class="adv-value">${el.ionization_energies !== null ? el.ionization_energies + ' kJ/mol' : '불명'}</span>
          </div>
        </div>
        ${el.spectral_img ? `
        <div class="spectral-img-container">
          <span class="adv-label" style="display:block; margin-bottom:8px; margin-top:16px;">방출 스펙트럼 (Spectral Image)</span>
          <img src="${el.spectral_img}" alt="Spectrum of ${el.nameEn}" class="spectral-img" loading="lazy">
        </div>
        ` : ''}
      </div>
    </details>
    
    <div class="modal-nav">
      <button class="modal-nav-btn" onclick="navModal(-1, ${el.num})" ${el.num <= 1 ? 'disabled' : ''}>◀ 이전</button>
      <button class="modal-nav-btn" onclick="navModal(1, ${el.num})" ${el.num >= 118 ? 'disabled' : ''}>다음 ▶</button>
    </div>
  `;

  modalBody.innerHTML = html;
  modalOverlay.classList.add('open');
  document.body.style.overflow = 'hidden';

  const container = document.getElementById('atom-3d-container');
  container.innerHTML = ''; 
  if (window.atomTimeout) clearTimeout(window.atomTimeout);
  window.atomTimeout = setTimeout(() => init3D(el, 'atom-3d-container'), 300);
}

function closeModal() {
  const modalOverlay = document.getElementById('modalOverlay');
  const compareBox = document.getElementById('compareModalBox');
  const modalBox = document.getElementById('modalBox');

  modalOverlay.classList.remove('open');
  document.body.style.overflow = '';
  setTimeout(() => {
    modalBox.style.display = 'block';
    compareBox.style.display = 'none';
  }, 300);
  dispose3D();
}


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

  // Setup explosion state
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

// ==========================================

window.navModal = function(dir, currentNum) {
  const nextNum = currentNum + dir;
  const nextEl = elementsData.find(e => e.num === nextNum);
  if (nextEl) openModal(nextEl);
}

function handleOverlayClick(e) {
  if (e.target === modalOverlay) closeModal();
}

function renderList() {
  if (!listTbody) return;
  const q = searchInput.value.toLowerCase().trim();
  
  let filtered = elementsData.filter(el => {
    let matchCat = (currentFilter === 'all' || el.cat === currentFilter);
    let matchSearch = true;
    if (q) {
      matchSearch = el.nameKr.includes(q) || 
                    el.sym.toLowerCase().includes(q) || 
                    el.num.toString() === q ||
                    el.nameEn.toLowerCase().includes(q) ||
                    (el.use && el.use.toLowerCase().includes(q)) ||
                    (el.desc && el.desc.toLowerCase().includes(q)) ||
                    (el.fact && el.fact.toLowerCase().includes(q));
    }
    return matchCat && matchSearch;
  });

  filtered.sort((a, b) => {
    let valA = a[currentSortCol];
    let valB = b[currentSortCol];
    
    if (valA === null || valA === undefined) valA = sortAsc ? Infinity : -Infinity;
    if (valB === null || valB === undefined) valB = sortAsc ? Infinity : -Infinity;
    
    if (typeof valA === 'string' && typeof valB === 'string') {
      return sortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
    }
    return sortAsc ? valA - valB : valB - valA;
  });

  listTbody.innerHTML = '';
  filtered.forEach(el => {
    const tr = document.createElement('tr');
    tr.style.cursor = 'pointer';
    tr.onclick = () => openModal(el);
    const catColor = getGroupColor(el.cat);
    let catName = document.querySelector(`.fb[data-cat="${el.cat}"]`)?.textContent.split(' ')[0] || '분류 없음';
    
    tr.innerHTML = `
      <td>${el.num}</td>
      <td style="color: ${catColor}; font-weight: bold;">${el.sym}</td>
      <td>${el.nameKr} <span style="font-size:0.7em; color:#888;">${el.nameEn}</span></td>
      <td><span class="cat-badge" style="background: color-mix(in srgb, ${catColor} 20%, transparent); color: ${catColor}; border: 1px solid ${catColor};">${catName}</span></td>
      <td>${el.mass}</td>
      <td>${el.melt !== null ? el.melt + ' K' : '-'}</td>
      <td>${el.boil !== null ? el.boil + ' K' : '-'}</td>
      <td>${el.density !== null ? el.density : '-'}</td>
    `;
    listTbody.appendChild(tr);
  });
}

// Table sort headers
document.querySelectorAll('.el-table th').forEach(th => {
  th.addEventListener('click', () => {
    const col = th.dataset.sort;
    if (currentSortCol === col) {
      sortAsc = !sortAsc;
    } else {
      currentSortCol = col;
      sortAsc = true;
    }
    renderList();
  });
});

function setFilter(cat, btnElement) {
  currentFilter = cat;
  document.querySelectorAll('.filter-bar .fb').forEach(btn => btn.classList.remove('active'));
  if(btnElement) btnElement.classList.add('active');

  filterCards();
}

function filterCards() {
  const q = searchInput.value.toLowerCase().trim();
  
  document.querySelectorAll('.el-card').forEach(card => {
    const num = parseInt(card.dataset.num);
    const el = elementsData.find(e => e.num === num);
    if(!el) return;

    let matchCat = (currentFilter === 'all' || el.cat === currentFilter);
    let matchSearch = true;
    
    if (q) {
      matchSearch = el.nameKr.includes(q) || 
                    el.sym.toLowerCase().includes(q) || 
                    el.num.toString() === q ||
                    el.nameEn.toLowerCase().includes(q) ||
                    (el.use && el.use.toLowerCase().includes(q)) ||
                    (el.desc && el.desc.toLowerCase().includes(q)) ||
                    (el.fact && el.fact.toLowerCase().includes(q));
    }

    if (matchCat && matchSearch) {
      card.classList.add('highlighted');
      card.classList.remove('dimmed');
    } else {
      card.classList.add('dimmed');
      card.classList.remove('highlighted');
    }
  });

  if (isListView) {
    renderList();
  }
}

searchInput.addEventListener('input', (e) => {
  if (e.target.value.trim() !== '') {
    clearBtn.classList.add('visible');
  } else {
    clearBtn.classList.remove('visible');
  }
  filterCards();
});

window.clearSearch = function() {
  searchInput.value = '';
  clearBtn.classList.remove('visible');
  filterCards();
  searchInput.focus();
}

// Init
initStars();
initLabels();
renderTable();
renderLegend();

if (tempSlider) { updateElementsState(parseInt(tempSlider.value)); }

// Register Service Worker for PWA
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./service-worker.js').catch(err => {
      console.log('ServiceWorker registration failed: ', err);
    });
  });
}


// Auto-switch to list view on mobile
if (window.innerWidth <= 768) {
  viewListBtn.click();
}

