import json
import os

elements = [
    {"num": 1, "sym": "H", "nameKr": "수소", "nameEn": "Hydrogen", "mass": "1.008", "cat": "nonmetal", "group": 1, "period": 1, "state": "gas",
     "desc": "우주에서 가장 풍부한 원소입니다. 태양과 같은 항성의 주요 연료이며, 미래의 친환경 에너지원으로 주목받고 있습니다.",
     "use": "로켓 연료, 수소차 연료 전지, 마가린 제조", "fact": "수소는 우주 전체 질량의 약 75%를 차지합니다!"},
    {"num": 2, "sym": "He", "nameKr": "헬륨", "nameEn": "Helium", "mass": "4.0026", "cat": "noble-gas", "group": 18, "period": 1, "state": "gas",
     "desc": "가볍고 반응성이 매우 낮은 기체입니다. 목소리를 변하게 하는 파티용 풍선으로 유명하지만, 첨단 산업에서도 널리 쓰입니다.",
     "use": "파티 풍선, MRI 냉각재, 심해 잠수용 산소 혼합물", "fact": "헬륨은 지구보다 태양에서 먼저 발견된 유일한 원소입니다."},
    {"num": 3, "sym": "Li", "nameKr": "리튬", "nameEn": "Lithium", "mass": "6.94", "cat": "alkali-metal", "group": 1, "period": 2, "state": "solid",
     "desc": "가장 가벼운 금속으로, 물에 뜰 정도로 밀도가 낮습니다. 현대 휴대용 전자기기 혁명의 일등 공신입니다.",
     "use": "스마트폰 배터리, 전기차 배터리, 우울증 치료제", "fact": "리튬은 기름 속에 보관하지 않으면 공기 중의 수분과 반응해 폭발할 수 있습니다."},
    {"num": 4, "sym": "Be", "nameKr": "베릴륨", "nameEn": "Beryllium", "mass": "9.0122", "cat": "alkaline-earth", "group": 2, "period": 2, "state": "solid",
     "desc": "강철보다 가벼우면서도 매우 단단한 금속입니다. 독성이 강해 다루기 까다롭지만, 우주항공 분야에서 필수적입니다.",
     "use": "제임스 웹 우주망원경 거울, 인공위성 부품", "fact": "에메랄드와 아쿠아마린의 아름다운 색은 베릴륨 덕분입니다."},
    {"num": 5, "sym": "B", "nameKr": "붕소", "nameEn": "Boron", "mass": "10.81", "cat": "metalloid", "group": 13, "period": 2, "state": "solid",
     "desc": "다이아몬드 다음으로 단단한 물질을 만들 수 있는 준금속입니다. 유리를 튼튼하게 만드는 데 유용합니다.",
     "use": "내열 유리(파이렉스), 바퀴벌레 퇴치제, 테니스 라켓", "fact": "붕소는 식물의 세포벽을 튼튼하게 하는 필수 영양소입니다."},
    {"num": 6, "sym": "C", "nameKr": "탄소", "nameEn": "Carbon", "mass": "12.011", "cat": "nonmetal", "group": 14, "period": 2, "state": "solid",
     "desc": "지구상의 모든 생명체의 뼈대를 이루는 핵심 원소입니다. 배열에 따라 가장 부드러운 흑연이나 가장 단단한 다이아몬드가 됩니다.",
     "use": "연필심(흑연), 보석(다이아몬드), 탄소섬유", "fact": "인체의 약 18%는 탄소로 이루어져 있습니다."},
    {"num": 7, "sym": "N", "nameKr": "질소", "nameEn": "Nitrogen", "mass": "14.007", "cat": "nonmetal", "group": 15, "period": 2, "state": "gas",
     "desc": "지구 대기의 78%를 차지하는 기체입니다. 단백질과 DNA의 필수 구성 요소이며 식물의 성장에 중요합니다.",
     "use": "비료, 과자 봉지 충전재, 액체질소 냉동", "fact": "과자 봉지가 빵빵한 이유는 과자가 부서지거나 상하지 않게 질소를 채워 넣었기 때문입니다."},
    {"num": 8, "sym": "O", "nameKr": "산소", "nameEn": "Oxygen", "mass": "15.999", "cat": "nonmetal", "group": 16, "period": 2, "state": "gas",
     "desc": "우리가 숨 쉬는 데 필수적인 기체로, 지구 지각에서 가장 흔한 원소입니다. 물질이 타는 연소 반응을 돕습니다.",
     "use": "의료용 산소호흡기, 제철 공업, 로켓 산화제", "fact": "지구 지각 질량의 약 46%가 산소로 이루어져 있습니다."},
    {"num": 9, "sym": "F", "nameKr": "플루오린(불소)", "nameEn": "Fluorine", "mass": "18.998", "cat": "halogen", "group": 17, "period": 2, "state": "gas",
     "desc": "가장 반응성이 강한 원소로, 거의 모든 물질과 반응합니다. 치아를 튼튼하게 하거나 프라이팬 코팅에 쓰입니다.",
     "use": "치약, 테플론(프라이팬 코팅), 에어컨 냉매", "fact": "반응성이 너무 강해 유리조차도 녹일 수 있습니다."},
    {"num": 10, "sym": "Ne", "nameKr": "네온", "nameEn": "Neon", "mass": "20.180", "cat": "noble-gas", "group": 18, "period": 2, "state": "gas",
     "desc": "전기를 통하면 밝은 주황-붉은색 빛을 내는 비활성 기체입니다. 밤거리를 밝히는 네온사인으로 유명합니다.",
     "use": "네온사인, 헬륨-네온 레이저", "fact": "우리가 보는 다른 색깔의 '네온사인'은 사실 네온이 아닌 아르곤(파란색) 등 다른 가스를 사용한 것입니다."},
    {"num": 11, "sym": "Na", "nameKr": "나트륨(소듐)", "nameEn": "Sodium", "mass": "22.990", "cat": "alkali-metal", "group": 1, "period": 3, "state": "solid",
     "desc": "은백색의 무른 금속으로, 물과 격렬하게 반응합니다. 우리 몸의 신경 전달에 필수적인 역할을 합니다.",
     "use": "소금(염화나트륨), 베이킹 소다, 가로등(나트륨 램프)", "fact": "순수한 나트륨은 칼로 자를 수 있을 만큼 무릅니다."},
    {"num": 12, "sym": "Mg", "nameKr": "마그네슘", "nameEn": "Magnesium", "mass": "24.305", "cat": "alkaline-earth", "group": 2, "period": 3, "state": "solid",
     "desc": "가볍고 튼튼한 금속으로, 태울 때 매우 밝은 하얀 빛을 냅니다. 식물의 엽록소의 중심핵을 이룹니다.",
     "use": "자동차 휠, 카메라 플래시, 소화제(제산제)", "fact": "마그네슘 불꽃은 너무 밝아서 맨눈으로 보면 시력이 손상될 수 있습니다."},
    {"num": 13, "sym": "Al", "nameKr": "알루미늄", "nameEn": "Aluminum", "mass": "26.982", "cat": "post-transition", "group": 13, "period": 3, "state": "solid",
     "desc": "지각에서 가장 풍부한 금속으로, 가볍고 녹슬지 않아 현대 산업의 핵심 소재입니다.",
     "use": "음료수 캔, 호일, 비행기 동체, 창틀", "fact": "알루미늄은 재활용할 때 처음 만들 때 필요한 에너지의 5%밖에 들지 않습니다."},
    {"num": 14, "sym": "Si", "nameKr": "규소(실리콘)", "nameEn": "Silicon", "mass": "28.085", "cat": "metalloid", "group": 14, "period": 3, "state": "solid",
     "desc": "모래와 유리의 주성분이며, 반도체의 핵심 원료로 정보화 시대를 연 일등 공신입니다.",
     "use": "반도체 칩, 유리, 콘크리트, 태양광 패널", "fact": "지구의 지각은 약 28%가 규소로 이루어져 있습니다."},
    {"num": 15, "sym": "P", "nameKr": "인", "nameEn": "Phosphorus", "mass": "30.974", "cat": "nonmetal", "group": 15, "period": 3, "state": "solid",
     "desc": "생명체의 DNA와 뼈를 구성하는 필수 원소입니다. 백린은 공기 중에서 스스로 불이 붙을 정도로 반응성이 큽니다.",
     "use": "성냥의 머리, 비료, 폭죽", "fact": "최초로 인을 발견한 연금술사는 소변을 끓여서 금을 만들려다 인을 발견했습니다."},
    {"num": 16, "sym": "S", "nameKr": "황", "nameEn": "Sulfur", "mass": "32.06", "cat": "nonmetal", "group": 16, "period": 3, "state": "solid",
     "desc": "노란색의 고체 원소로, 특유의 썩은 달걀 냄새가 나는 화합물을 만듭니다. 온천 냄새의 원인입니다.",
     "use": "화약, 타이어 고무(가황), 살충제, 페니실린", "fact": "양파나 마늘을 자를 때 눈물이 나는 이유는 그 속에 포함된 황 화합물 때문입니다."},
    {"num": 17, "sym": "Cl", "nameKr": "염소", "nameEn": "Chlorine", "mass": "35.45", "cat": "halogen", "group": 17, "period": 3, "state": "gas",
     "desc": "노란색을 띠는 독성 기체로, 강력한 살균 및 표백 효과가 있습니다. 수돗물 소독에 사용됩니다.",
     "use": "수돗물 소독, 락스(표백제), PVC 플라스틱", "fact": "독성이 강하지만, 나트륨과 결합하면 우리가 먹는 소금(염화나트륨)이 됩니다."},
    {"num": 18, "sym": "Ar", "nameKr": "아르곤", "nameEn": "Argon", "mass": "39.948", "cat": "noble-gas", "group": 18, "period": 3, "state": "gas",
     "desc": "대기의 약 1%를 차지하는 비활성 기체입니다. 다른 물질과 거의 반응하지 않아 보호용 가스로 쓰입니다.",
     "use": "백열전구 충전 가스, 용접 보호 가스, 이중창 내부 충전", "fact": "'아르곤'이라는 이름은 그리스어로 '게으르다'는 뜻에서 유래했습니다."},
    {"num": 19, "sym": "K", "nameKr": "칼륨(포타슘)", "nameEn": "Potassium", "mass": "39.098", "cat": "alkali-metal", "group": 1, "period": 4, "state": "solid",
     "desc": "나트륨과 비슷하게 반응성이 매우 큰 무른 금속입니다. 우리 몸의 근육과 신경 기능에 필수적입니다.",
     "use": "비료, 비누, 바나나(풍부한 영양소)", "fact": "바나나에 칼륨이 많아 아주 미세한 방사성을 띠지만, 건강에는 전혀 지장이 없습니다."},
    {"num": 20, "sym": "Ca", "nameKr": "칼슘", "nameEn": "Calcium", "mass": "40.078", "cat": "alkaline-earth", "group": 2, "period": 4, "state": "solid",
     "desc": "우유, 뼈, 치아의 주성분으로 잘 알려져 있으며, 자연에서는 석회석의 형태로 흔하게 발견됩니다.",
     "use": "시멘트, 우유, 뼈와 치아 구성", "fact": "껍질이 있는 달걀 껍데기나 조개껍데기의 주성분도 칼슘 화합물입니다."},
    {"num": 21, "sym": "Sc", "nameKr": "스칸듐", "nameEn": "Scandium", "mass": "44.956", "cat": "transition-metal", "group": 3, "period": 4, "state": "solid",
     "desc": "가볍고 열에 강한 금속입니다. 알루미늄과 합금을 만들면 강도가 크게 높아져 스포츠 용품에 쓰입니다.",
     "use": "고급 자전거 프레임, 야구 배트, 경기장 조명", "fact": "처음 스칸디나비아 반도에서 발견되어 이름이 붙여졌습니다."},
    {"num": 22, "sym": "Ti", "nameKr": "타이타늄", "nameEn": "Titanium", "mass": "47.867", "cat": "transition-metal", "group": 4, "period": 4, "state": "solid",
     "desc": "강철만큼 강하지만 무게는 훨씬 가볍고 녹슬지 않는 '꿈의 금속'입니다. 인체 거부반응이 없습니다.",
     "use": "임플란트, 항공기 엔진, 골프채, 흰색 페인트(이산화타이타늄)", "fact": "이름은 그리스 신화의 강력한 신족인 '타이탄'에서 따왔습니다."},
    {"num": 23, "sym": "V", "nameKr": "바나듐", "nameEn": "Vanadium", "mass": "50.942", "cat": "transition-metal", "group": 5, "period": 4, "state": "solid",
     "desc": "강철에 조금만 섞어도 강도와 탄성이 크게 증가하는 합금 원소입니다.",
     "use": "자동차 엔진 부품, 공구(렌치, 스패너)", "fact": "아름다운 색깔의 화합물을 만들어, 스칸디나비아 미의 여신 '바나디스'의 이름을 땄습니다."},
    {"num": 24, "sym": "Cr", "nameKr": "크로뮴", "nameEn": "Chromium", "mass": "51.996", "cat": "transition-metal", "group": 6, "period": 4, "state": "solid",
     "desc": "단단하고 녹슬지 않아 다른 금속의 도금에 널리 쓰이는 반짝이는 은백색 금속입니다.",
     "use": "스테인리스 스틸, 오토바이 부품 도금, 루비의 붉은색", "fact": "루비가 붉은색을, 에메랄드가 녹색을 띠게 하는 원인이 바로 크로뮴의 불순물 때문입니다."},
    {"num": 25, "sym": "Mn", "nameKr": "망가니즈", "nameEn": "Manganese", "mass": "54.938", "cat": "transition-metal", "group": 7, "period": 4, "state": "solid",
     "desc": "강철의 강도를 높이는 데 필수적인 금속이며, 건전지의 핵심 재료로도 사용됩니다.",
     "use": "철도 레일 합금, 건전지, 알루미늄 캔 합금", "fact": "심해 바닥에는 망가니즈가 감자 모양으로 뭉쳐 있는 '망가니즈 단괴'가 깔려 있습니다."},
    {"num": 26, "sym": "Fe", "nameKr": "철", "nameEn": "Iron", "mass": "55.845", "cat": "transition-metal", "group": 8, "period": 4, "state": "solid",
     "desc": "인류 역사상 가장 중요한 금속이자, 지구의 핵을 이루는 주요 원소입니다. 자성을 띠는 특징이 있습니다.",
     "use": "건축물 뼈대, 자동차, 혈액의 헤모글로빈", "fact": "우리의 피가 붉은 이유는 적혈구 속 헤모글로빈에 철분이 들어 있어 산소와 결합할 때 붉게 변하기 때문입니다."},
    {"num": 27, "sym": "Co", "nameKr": "코발트", "nameEn": "Cobalt", "mass": "58.933", "cat": "transition-metal", "group": 9, "period": 4, "state": "solid",
     "desc": "철처럼 자성을 띠는 금속으로, 강력한 자석이나 특수 합금을 만드는 데 사용됩니다.",
     "use": "리튬 이온 배터리, 푸른색 유리 및 도자기 안료", "fact": "고려청자의 아름다운 푸른빛이나 스테인드글라스의 파란색은 코발트 화합물 덕분입니다."},
    {"num": 28, "sym": "Ni", "nameKr": "니켈", "nameEn": "Nickel", "mass": "58.693", "cat": "transition-metal", "group": 10, "period": 4, "state": "solid",
     "desc": "녹슬지 않는 성질이 강해 동전이나 도금, 스테인리스 스틸의 중요한 재료로 쓰입니다.",
     "use": "동전(백원짜리 등), 충전식 배터리, 수도꼭지 도금", "fact": "미국의 5센트 동전은 니켈이 많이 포함되어 있어 동전 이름 자체가 '니켈'입니다."},
    {"num": 29, "sym": "Cu", "nameKr": "구리", "nameEn": "Copper", "mass": "63.546", "cat": "transition-metal", "group": 11, "period": 4, "state": "solid",
     "desc": "전기와 열이 매우 잘 통하는 붉은색 금속으로, 인류가 가장 먼저 사용하기 시작한 금속 중 하나입니다.",
     "use": "전선, 동전, 파이프, 청동 및 황동 합금", "fact": "구리는 강력한 항균 작용이 있어서 문손잡이나 엘리베이터 버튼에 사용하면 세균 전염을 줄일 수 있습니다."},
    {"num": 30, "sym": "Zn", "nameKr": "아연", "nameEn": "Zinc", "mass": "65.38", "cat": "transition-metal", "group": 12, "period": 4, "state": "solid",
     "desc": "철이 녹스는 것을 막아주는 보호막 역할을 하는 금속입니다. 우리 몸의 면역계에도 중요합니다.",
     "use": "함석판(지붕재), 자외선 차단제(산화아연), 배터리", "fact": "철 위에 아연을 도금한 '함석'은 철에 상처가 나더라도 아연이 먼저 녹슬어 철을 보호합니다."},
    {"num": 47, "sym": "Ag", "nameKr": "은", "nameEn": "Silver", "mass": "107.87", "cat": "transition-metal", "group": 11, "period": 5, "state": "solid",
     "desc": "모든 금속 중 빛 반사율이 가장 높고, 전기와 열을 가장 잘 전달합니다.",
     "use": "장신구, 거울, 고급 식기, 항균 물질", "fact": "과거에는 사진 필름에 은 화합물을 사용하여 빛을 기록했습니다."},
    {"num": 79, "sym": "Au", "nameKr": "금", "nameEn": "Gold", "mass": "196.97", "cat": "transition-metal", "group": 11, "period": 6, "state": "solid",
     "desc": "영원히 녹슬거나 변색되지 않는 아름다운 노란색 귀금속입니다. 연성(늘어나는 성질)이 최고 수준입니다.",
     "use": "장신구, 화폐 척도, 스마트폰 회로 기판, 치과 치료", "fact": "1g의 금은 3km가 넘는 길이의 얇은 선으로 뽑아낼 수 있습니다."},
    {"num": 80, "sym": "Hg", "nameKr": "수은", "nameEn": "Mercury", "mass": "200.59", "cat": "transition-metal", "group": 12, "period": 6, "state": "liquid",
     "desc": "상온에서 유일하게 액체 상태인 금속입니다. 밀도가 매우 높고 맹독성을 가집니다.",
     "use": "과거의 온도계와 혈압계, 형광등", "fact": "철이나 납 같은 무거운 금속도 수은 위에서는 물에 뜬 나무처럼 동동 뜹니다."},
    {"num": 92, "sym": "U", "nameKr": "우라늄", "nameEn": "Uranium", "mass": "238.03", "cat": "actinide", "group": "fblock", "period": 7, "state": "solid",
     "desc": "강력한 방사선을 내뿜는 원소로, 원자력 발전과 핵무기의 핵심 원료입니다.",
     "use": "원자력 발전 연료, 방사선 차폐재(열화우라늄)", "fact": "우라늄 1그램이 낼 수 있는 에너지는 석탄 3톤을 태우는 것과 맞먹습니다."}
]

# 나머지 원소들은 일반화된 데이터로 생성
existing_nums = {e["num"] for e in elements}

# 원소 기본 카테고리 정보
# (번호 리스트)
lanthanides = range(57, 72)
actinides = range(89, 104)

for i in range(1, 119):
    if i not in existing_nums:
        # 그룹, 주기 판별
        group = 1
        period = 1
        cat = "unknown"
        if i in lanthanides:
            cat = "lanthanide"
            period = 6
            group = "fblock"
        elif i in actinides:
            cat = "actinide"
            period = 7
            group = "fblock"
        else:
            # 대략적인 일반 금속 설정
            cat = "transition-metal"
            
        elements.append({
            "num": i,
            "sym": f"El{i}",
            "nameKr": f"원소 {i}",
            "nameEn": f"Element {i}",
            "mass": "0.0",
            "cat": cat,
            "group": group,
            "period": period,
            "state": "unknown",
            "desc": "아직 상세 설명이 업데이트되지 않은 원소입니다. 주기율표의 다양한 원소 중 하나입니다.",
            "use": "연구 중",
            "fact": f"원자 번호 {i}번 원소입니다."
        })

# 실제 심볼/이름 보완
symbol_map = {
    31:"Ga",32:"Ge",33:"As",34:"Se",35:"Br",36:"Kr",
    37:"Rb",38:"Sr",39:"Y",40:"Zr",41:"Nb",42:"Mo",43:"Tc",44:"Ru",45:"Rh",46:"Pd",48:"Cd",49:"In",50:"Sn",51:"Sb",52:"Te",53:"I",54:"Xe",
    55:"Cs",56:"Ba",
    57:"La",58:"Ce",59:"Pr",60:"Nd",61:"Pm",62:"Sm",63:"Eu",64:"Gd",65:"Tb",66:"Dy",67:"Ho",68:"Er",69:"Tm",70:"Yb",71:"Lu",
    72:"Hf",73:"Ta",74:"W",75:"Re",76:"Os",77:"Ir",78:"Pt",81:"Tl",82:"Pb",83:"Bi",84:"Po",85:"At",86:"Rn",
    87:"Fr",88:"Ra",
    89:"Ac",90:"Th",91:"Pa",93:"Np",94:"Pu",95:"Am",96:"Cm",97:"Bk",98:"Cf",99:"Es",100:"Fm",101:"Md",102:"No",103:"Lr",
    104:"Rf",105:"Db",106:"Sg",107:"Bh",108:"Hs",109:"Mt",110:"Ds",111:"Rg",112:"Cn",113:"Nh",114:"Fl",115:"Mc",116:"Lv",117:"Ts",118:"Og"
}

name_kr_map = {
    31:"갈륨",32:"저마늄",33:"비소",34:"셀레늄",35:"브로민",36:"크립톤",
    37:"루비듐",38:"스트론튬",39:"이트륨",40:"지르코늄",41:"나이오븀",42:"몰리브데넘",43:"테크네튬",44:"루테늄",45:"로듐",46:"팔라듐",48:"카드뮴",49:"인듐",50:"주석",51:"안티모니",52:"텔루륨",53:"아이오딘",54:"제논",
    55:"세슘",56:"바륨",
    57:"란타넘",58:"세륨",59:"프라세오디뮴",60:"네오디뮴",61:"프로메튬",62:"사마륨",63:"유로퓸",64:"가돌리늄",65:"터븀",66:"디스프로슘",67:"홀뮴",68:"어븀",69:"툴륨",70:"이터븀",71:"루테튬",
    72:"하프늄",73:"탄탈럼",74:"텅스텐",75:"레늄",76:"오스뮴",77:"이리듐",78:"백금",81:"탈륨",82:"납",83:"비스무트",84:"폴로늄",85:"아스타틴",86:"라돈",
    87:"프랑슘",88:"라듐",
    89:"악티늄",90:"토륨",91:"프로탁티늄",93:"넵투늄",94:"플루토늄",95:"아메리슘",96:"퀴륨",97:"버클륨",98:"캘리포늄",99:"아인슈타이늄",100:"페르뮴",101:"멘델레븀",102:"노벨륨",103:"로렌슘",
    104:"러더포듐",105:"더브늄",106:"시보귬",107:"보륨",108:"하슘",109:"마이트너륨",110:"다름슈타튬",111:"뢴트게늄",112:"코페르니슘",113:"니호늄",114:"플레로븀",115:"모스코븀",116:"리버모륨",117:"테네신",118:"오가네손"
}

name_en_map = {
    1:"Hydrogen",2:"Helium",3:"Lithium",4:"Beryllium",5:"Boron",6:"Carbon",7:"Nitrogen",8:"Oxygen",9:"Fluorine",10:"Neon",
    11:"Sodium",12:"Magnesium",13:"Aluminum",14:"Silicon",15:"Phosphorus",16:"Sulfur",17:"Chlorine",18:"Argon",
    19:"Potassium",20:"Calcium",21:"Scandium",22:"Titanium",23:"Vanadium",24:"Chromium",25:"Manganese",26:"Iron",27:"Cobalt",28:"Nickel",29:"Copper",30:"Zinc",
    31:"Gallium",32:"Germanium",33:"Arsenic",34:"Selenium",35:"Bromine",36:"Krypton",
    37:"Rubidium",38:"Strontium",39:"Yttrium",40:"Zirconium",41:"Niobium",42:"Molybdenum",43:"Technetium",44:"Ruthenium",45:"Rhodium",46:"Palladium",47:"Silver",48:"Cadmium",49:"Indium",50:"Tin",51:"Antimony",52:"Tellurium",53:"Iodine",54:"Xenon",
    55:"Cesium",56:"Barium",
    57:"Lanthanum",58:"Cerium",59:"Praseodymium",60:"Neodymium",61:"Promethium",62:"Samarium",63:"Europium",64:"Gadolinium",65:"Terbium",66:"Dysprosium",67:"Holmium",68:"Erbium",69:"Thulium",70:"Ytterbium",71:"Lutetium",
    72:"Hafnium",73:"Tantalum",74:"Tungsten",75:"Rhenium",76:"Osmium",77:"Iridium",78:"Platinum",79:"Gold",80:"Mercury",81:"Thallium",82:"Lead",83:"Bismuth",84:"Polonium",85:"Astatine",86:"Radon",
    87:"Francium",88:"Radium",
    89:"Actinium",90:"Thorium",91:"Protactinium",92:"Uranium",93:"Neptunium",94:"Plutonium",95:"Americium",96:"Curium",97:"Berkelium",98:"Californium",99:"Einsteinium",100:"Fermium",101:"Mendelevium",102:"Nobelium",103:"Lawrencium",
    104:"Rutherfordium",105:"Dubnium",106:"Seaborgium",107:"Bohrium",108:"Hassium",109:"Meitnerium",110:"Darmstadtium",111:"Roentgenium",112:"Copernicium",113:"Nihonium",114:"Flerovium",115:"Moscovium",116:"Livermorium",117:"Tennessine",118:"Oganesson"
}

# 위치 및 카테고리 매핑 로직 보완
cat_map = {
    "alkali-metal": [3, 11, 19, 37, 55, 87],
    "alkaline-earth": [4, 12, 20, 38, 56, 88],
    "post-transition": [13, 31, 49, 50, 81, 82, 83, 113, 114, 115, 116],
    "metalloid": [5, 14, 32, 33, 51, 52, 84],
    "nonmetal": [1, 6, 7, 8, 15, 16, 34],
    "halogen": [9, 17, 35, 53, 85, 117],
    "noble-gas": [2, 10, 18, 36, 54, 86, 118]
}

def get_group_period(z):
    # 단순화된 위치 계산
    periods = [0, 2, 10, 18, 36, 54, 86, 118]
    p = 1
    for i, max_z in enumerate(periods):
        if z <= max_z:
            p = i
            break
    
    # f블록 처리
    if 57 <= z <= 71: return "fblock", 6
    if 89 <= z <= 103: return "fblock", 7
    
    # 나머지 그룹
    p_start = periods[p-1] + 1
    diff = z - p_start
    if p in [1, 2, 3]:
        if diff < 2: g = diff + 1
        else: g = diff + 11
    else:
        if p == 6 and z >= 72:
            g = z - 68
        elif p == 7 and z >= 104:
            g = z - 100
        else:
            g = diff + 1
        
    return g, p

for el in elements:
    z = el["num"]
    if z in symbol_map:
        el["sym"] = symbol_map[z]
    if z in name_kr_map:
        el["nameKr"] = name_kr_map[z]
    if z in name_en_map:
        el["nameEn"] = name_en_map[z]
    
    if "unknown" in el["cat"] or "transition-metal" in el["cat"]:
        if 57 <= z <= 71: el["cat"] = "lanthanide"
        elif 89 <= z <= 103: el["cat"] = "actinide"
        else:
            for c, nums in cat_map.items():
                if z in nums:
                    el["cat"] = c
                    break
            else:
                el["cat"] = "transition-metal" # 기본값

    g, p = get_group_period(z)
    el["group"] = g
    el["period"] = p

elements.sort(key=lambda x: x["num"])

with open("/Users/pochoco/Desktop/원소주기율표/elements_data.js", "w", encoding="utf-8") as f:
    f.write("const elementsData = ")
    json.dump(elements, f, ensure_ascii=False, indent=2)
    f.write(";")

print("Data generation complete!")
