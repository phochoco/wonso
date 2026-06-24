import json
import urllib.request
import re

JS_FILE = '/Users/pochoco/Desktop/원소주기율표/elements_data.js'
URL = 'https://raw.githubusercontent.com/Bowserinator/Periodic-Table-JSON/master/PeriodicTableJSON.json'

print("Downloading advanced data from Bowserinator's Periodic-Table-JSON...")
try:
    with urllib.request.urlopen(URL) as url:
        data = json.loads(url.read().decode())
except Exception as e:
    print(f"Failed to download data: {e}")
    exit(1)

elements_dict = {}
for el in data['elements']:
    elements_dict[el['number']] = {
        'density': el.get('density', None),
        'electronegativity': el.get('electronegativity_pauling', None),
        'electron_config': el.get('electron_configuration_semantic', ''),
        'shells': ', '.join(map(str, el.get('shells', [])))
    }

print("Reading elements_data.js...")
with open(JS_FILE, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Extract JSON string from JS
match = re.search(r'const elementsData = (\[.*?\]);', js_content, re.DOTALL)
if not match:
    print("Could not find elementsData array in JS file.")
    exit(1)

json_str = match.group(1)
# Clean up JS specific syntax if needed (like trailing commas, missing quotes around keys).
# Our elements_data.js is already valid JSON, but keys might not be quoted if it's raw JS.
# Assuming it's well-formed enough or we can use demjson, but let's try standard json if possible.
# Actually, the previous add_temp_data.py handled it with regex or by rewriting.
# Let's use a simpler approach: evaluating it.
