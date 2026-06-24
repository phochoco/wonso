# ⚛️ 인터랙티브 3D 원소주기율표 (Interactive 3D Periodic Table)

![Periodic Table Preview](https://images.unsplash.com/photo-1603126852329-847e3ab88ce4?auto=format&fit=crop&w=1200&q=80)

118개 원소를 시각적으로 탐험할 수 있는 완벽한 인터랙티브 3D 원소주기율표 웹 어플리케이션입니다. 
딱딱한 표 형식에서 벗어나, 생동감 넘치는 3D 원자 모델과 온도 변화에 따른 상태 시뮬레이션, 그리고 위키백과 수준의 상세한 한글 데이터를 제공합니다.

## ✨ 주요 기능 (Key Features)

- **상호작용형 3D 원자 렌더링**: 원소를 클릭하면 전자가 궤도를 도는 3D 원자 모델이 나타납니다. 마우스로 회전시키고 터치하면 폭발하는 시각 효과가 적용되어 있습니다.
- **다이내믹 온도계 슬라이더**: 0K부터 6000K까지 온도를 조절하면, 각 원소의 녹는점과 끓는점에 따라 고체/액체/기체 상태가 실시간 색상으로 변화합니다.
- **강력한 데이터 시각화**: 
  - 방출 스펙트럼(Spectral Image) 제공
  - 발견자, 명명자, 몰 열용량, 전자 친화도 등 심층 학술 데이터 포함
  - 118개 전 원소 위키백과 설명 100% 한글화 번역 탑재
- **비교 모드 (Compare Mode)**: 두 개의 원소를 동시에 선택하여 3D 모델과 상세 스펙을 나란히 놓고 비교할 수 있습니다.
- **모바일/PWA 완벽 지원**: 반응형 리스트 뷰 및 데스크톱/모바일 설치형 웹 앱(PWA) 지원.

## 🛠 기술 스택 (Tech Stack)

- **Frontend**: HTML5, Vanilla JavaScript, CSS3 (CSS Variables, Grid/Flexbox)
- **3D Graphics**: [Three.js](https://threejs.org/) (r128)
- **Data Source**: 오픈소스 Periodic-Table-JSON 기반 확장 데이터 (파이썬 `deep-translator` 및 위키미디어 API 활용 한글화 및 자동 추출)
- **PWA**: Service Worker 및 Manifest 내장

## 🚀 로컬 실행 방법 (How to run locally)

별도의 빌드 과정(npm, Webpack 등) 없이 브라우저에서 바로 실행 가능한 순수 바닐라 웹 프로젝트입니다.

1. 레포지토리를 클론합니다.
```bash
git clone https://github.com/pochoco/wonso.git
```
2. 폴더로 이동합니다.
```bash
cd wonso
```
3. 로컬 서버를 띄워서 `index.html`을 실행합니다. (VS Code의 Live Server 확장 프로그램 등을 추천합니다.)
```bash
# Python이 설치되어 있다면 아래 명령어로 실행 가능합니다.
python3 -m http.server 8000
```
4. 브라우저에서 `http://localhost:8000` 으로 접속합니다.

## 📄 라이선스 (License)

이 프로젝트는 MIT License를 따릅니다. 누구나 자유롭게 활용하고 수정할 수 있습니다.
