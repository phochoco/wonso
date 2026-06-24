import json
import os

# Dictionary containing { atomic_number: { "melt": K, "boil": K } }
# Where K is in Kelvin. If unknown, it will be None.
temp_data = {
    1: {"melt": 13.99, "boil": 20.27},
    2: {"melt": 0.95, "boil": 4.22},
    3: {"melt": 453.65, "boil": 1615},
    4: {"melt": 1560, "boil": 2742},
    5: {"melt": 2349, "boil": 4200},
    6: {"melt": 3823, "boil": 4300},
    7: {"melt": 63.15, "boil": 77.36},
    8: {"melt": 54.36, "boil": 90.18},
    9: {"melt": 53.48, "boil": 85.03},
    10: {"melt": 24.56, "boil": 27.104},
    11: {"melt": 370.944, "boil": 1156.090},
    12: {"melt": 923, "boil": 1363},
    13: {"melt": 933.47, "boil": 2743},
    14: {"melt": 1687, "boil": 3538},
    15: {"melt": 317.3, "boil": 553.7}, # White phosphorus
    16: {"melt": 388.36, "boil": 717.8},
    17: {"melt": 171.6, "boil": 239.11},
    18: {"melt": 83.81, "boil": 87.30},
    19: {"melt": 336.7, "boil": 1032},
    20: {"melt": 1115, "boil": 1757},
    21: {"melt": 1814, "boil": 3109},
    22: {"melt": 1941, "boil": 3560},
    23: {"melt": 2183, "boil": 3680},
    24: {"melt": 2180, "boil": 2944},
    25: {"melt": 1519, "boil": 2334},
    26: {"melt": 1811, "boil": 3134},
    27: {"melt": 1768, "boil": 3200},
    28: {"melt": 1728, "boil": 3003},
    29: {"melt": 1357.77, "boil": 2835},
    30: {"melt": 692.68, "boil": 1180},
    31: {"melt": 302.9146, "boil": 2477},
    32: {"melt": 1211.40, "boil": 3106},
    33: {"melt": 1090, "boil": 887}, # Sublimes
    34: {"melt": 494, "boil": 958},
    35: {"melt": 265.8, "boil": 332.0},
    36: {"melt": 115.78, "boil": 119.93},
    37: {"melt": 312.45, "boil": 961},
    38: {"melt": 1050, "boil": 1650},
    39: {"melt": 1799, "boil": 3203},
    40: {"melt": 2128, "boil": 4682},
    41: {"melt": 2750, "boil": 5017},
    42: {"melt": 2896, "boil": 4912},
    43: {"melt": 2430, "boil": 4538},
    44: {"melt": 2607, "boil": 4423},
    45: {"melt": 2237, "boil": 3968},
    46: {"melt": 1828.05, "boil": 3236},
    47: {"melt": 1234.93, "boil": 2435},
    48: {"melt": 594.22, "boil": 1040},
    49: {"melt": 429.7485, "boil": 2345},
    50: {"melt": 505.08, "boil": 2875},
    51: {"melt": 903.78, "boil": 1908},
    52: {"melt": 722.66, "boil": 1261},
    53: {"melt": 386.85, "boil": 457.4},
    54: {"melt": 161.40, "boil": 165.05},
    55: {"melt": 301.7, "boil": 944},
    56: {"melt": 1000, "boil": 2118},
    57: {"melt": 1193, "boil": 3737},
    58: {"melt": 1068, "boil": 3716},
    59: {"melt": 1208, "boil": 3403},
    60: {"melt": 1297, "boil": 3347},
    61: {"melt": 1315, "boil": 3273},
    62: {"melt": 1345, "boil": 2076},
    63: {"melt": 1099, "boil": 1800},
    64: {"melt": 1585, "boil": 3250},
    65: {"melt": 1629, "boil": 3396},
    66: {"melt": 1680, "boil": 2840},
    67: {"melt": 1734, "boil": 2873},
    68: {"melt": 1795, "boil": 3141},
    69: {"melt": 1818, "boil": 2223},
    70: {"melt": 1097, "boil": 1469},
    71: {"melt": 1925, "boil": 3675},
    72: {"melt": 2506, "boil": 4876},
    73: {"melt": 3290, "boil": 5731},
    74: {"melt": 3695, "boil": 6203},
    75: {"melt": 3459, "boil": 5903},
    76: {"melt": 3306, "boil": 5285},
    77: {"melt": 2719, "boil": 4403},
    78: {"melt": 2041.4, "boil": 4098},
    79: {"melt": 1337.33, "boil": 3243},
    80: {"melt": 234.3210, "boil": 629.88},
    81: {"melt": 577, "boil": 1746},
    82: {"melt": 600.61, "boil": 2022},
    83: {"melt": 544.7, "boil": 1837},
    84: {"melt": 527, "boil": 1235},
    85: {"melt": 575, "boil": 610},
    86: {"melt": 202, "boil": 211.5},
    87: {"melt": 300, "boil": 950},
    88: {"melt": 973, "boil": 1413},
    89: {"melt": 1323, "boil": 3471},
    90: {"melt": 2023, "boil": 5061},
    91: {"melt": 1841, "boil": 4300},
    92: {"melt": 1405.3, "boil": 4218},
    93: {"melt": 912, "boil": 4273},
    94: {"melt": 912.5, "boil": 3505},
    95: {"melt": 1449, "boil": 2880},
    96: {"melt": 1613, "boil": 3383},
    97: {"melt": 1259, "boil": 2900},
    98: {"melt": 1173, "boil": 1743},
    99: {"melt": 1133, "boil": 1269},
    100: {"melt": 1800, "boil": None},
    101: {"melt": 1100, "boil": None},
    102: {"melt": 1100, "boil": None},
    103: {"melt": 1900, "boil": None},
    104: {"melt": 2400, "boil": 5800},
    105: {"melt": None, "boil": None},
    106: {"melt": None, "boil": None},
    107: {"melt": None, "boil": None},
    108: {"melt": None, "boil": None},
    109: {"melt": None, "boil": None},
    110: {"melt": None, "boil": None},
    111: {"melt": None, "boil": None},
    112: {"melt": 283, "boil": 340},
    113: {"melt": 700, "boil": 1400},
    114: {"melt": 340, "boil": 420},
    115: {"melt": 700, "boil": 1400},
    116: {"melt": 700, "boil": 1100},
    117: {"melt": 600, "boil": 883},
    118: {"melt": 320, "boil": 350}
}

target_file = "/Users/pochoco/Desktop/원소주기율표/elements_data.js"
if os.path.exists(target_file):
    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = content.replace("const elementsData = ", "").replace(";", "").strip()
    elements = json.loads(content)
    
    for el in elements:
        num = el["num"]
        if num in temp_data:
            el["melt"] = temp_data[num]["melt"]
            el["boil"] = temp_data[num]["boil"]
        else:
            el["melt"] = None
            el["boil"] = None

    with open(target_file, "w", encoding="utf-8") as f:
        f.write("const elementsData = ")
        json.dump(elements, f, ensure_ascii=False, indent=2)
        f.write(";")
    
    print("Updated elements with melt and boil temperatures.")
else:
    print("File not found")
