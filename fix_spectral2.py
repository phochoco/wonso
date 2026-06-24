import json

filepath = '/Users/pochoco/Desktop/원소주기율표/elements_data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    js_content = f.read()

import re
match = re.search(r'const elementsData = (\[[\s\S]*?\]);', js_content)
data_str = match.group(1)
elements = json.loads(data_str)

for el in elements:
    if el.get('nameEn') == 'Tantalum':
        el['spectral_img'] = 'https://upload.wikimedia.org/wikipedia/commons/e/ee/Tantalum_spectrum_visible.png'
    elif el.get('nameEn') == 'Radon':
        el['spectral_img'] = 'https://upload.wikimedia.org/wikipedia/commons/c/ce/Radon_spectrum.png'
    elif el.get('nameEn') == 'Americium':
        el['spectral_img'] = 'https://upload.wikimedia.org/wikipedia/commons/b/b2/Americium_spectrum_visible.png'

new_data_str = json.dumps(elements, ensure_ascii=False, indent=2)
new_js_content = js_content.replace(data_str, new_data_str)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_js_content)

print("Done fixing remaining 3.")
