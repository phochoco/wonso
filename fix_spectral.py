import json
import re
import urllib.request
import urllib.parse
import time
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

filepath = '/Users/pochoco/Desktop/원소주기율표/elements_data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    js_content = f.read()

match = re.search(r'const elementsData = (\[[\s\S]*?\]);', js_content)
if not match:
    print("Could not find elementsData array")
    exit(1)

data_str = match.group(1)
elements = json.loads(data_str)

def get_wikimedia_url(wiki_url):
    filename = wiki_url.split('/')[-1]
    filename = urllib.parse.unquote(filename)
    api_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(filename)}&prop=imageinfo&iiprop=url&format=json"
    
    req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/100.0.4896.127'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            pages = data['query']['pages']
            for page_id in pages:
                if 'imageinfo' in pages[page_id]:
                    return pages[page_id]['imageinfo'][0]['url']
    except Exception as e:
        print(f"Error fetching {filename}: {e}")
    return ""

changed = 0
for el in elements:
    if el.get('spectral_img') and 'wikipedia.org/wiki/File:' in el['spectral_img']:
        print(f"Fixing {el['nameEn']}...")
        direct_url = get_wikimedia_url(el['spectral_img'])
        if direct_url:
            el['spectral_img'] = direct_url
            changed += 1
        time.sleep(1.0) # sleep 1 second

new_data_str = json.dumps(elements, ensure_ascii=False, indent=2)
new_js_content = js_content.replace(data_str, new_data_str)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_js_content)

print(f"Fixed {changed} spectral images.")
