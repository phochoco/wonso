import os

filepath = '/Users/pochoco/Desktop/원소주기율표/script.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

bad_string = """    }
  });

  if (isListView) {
    renderList();
  }"""

# Replace all occurrences back to the original `    }`
fixed_content = content.replace(bad_string, "    }")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print(f"Fixed {content.count(bad_string)} corruptions.")
