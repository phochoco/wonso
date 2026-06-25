import re

filepath = '/Users/pochoco/Desktop/원소주기율표/index.html'
with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace old URL with the new vercel URL in OG and Twitter tags
html = html.replace('https://periodic-table-explorer.vercel.app/', 'https://wonso-nine.vercel.app/')

# Add Canonical link and JSON-LD before </head>
seo_injection = """  <link rel="canonical" href="https://wonso-nine.vercel.app/">
  <!-- Structured Data (JSON-LD) -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "인터랙티브 3D 원소주기율표",
    "url": "https://wonso-nine.vercel.app/",
    "description": "118개 원소를 3D로 탐험하세요! 상세한 한글 설명과 실생활 쓰임새까지 한곳에.",
    "applicationCategory": "EducationalApplication",
    "operatingSystem": "All",
    "offers": {
      "@type": "Offer",
      "price": "0"
    }
  }
  </script>
</head>"""

if '<link rel="canonical"' not in html:
    html = html.replace('</head>', seo_injection)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html SEO updated")
