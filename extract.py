import json
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re

url = "https://www.staraca.com/chinese/edu/HOT.asp?tid=1847"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('big5', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    
    courses = []
    # Find all links that look like course links
    for a in soup.find_all('a'):
        href = a.get('href', '')
        if 'educon.asp?ID=' in href:
            title = a.get_text(strip=True)
            if title and len(title) > 2:
                # Basic cleanup
                title = re.sub(r'\s+', ' ', title)
                courses.append({
                    'title': title,
                    'url': 'https://www.staraca.com/chinese/edu/' + href
                })
    
    # Deduplicate by url
    seen = set()
    unique_courses = []
    for c in courses:
        if c['url'] not in seen:
            seen.add(c['url'])
            unique_courses.append(c)

    with open('courses.json', 'w', encoding='utf-8') as f:
        json.dump(unique_courses, f, ensure_ascii=False, indent=2)
except Exception as e:
    with open('courses.json', 'w', encoding='utf-8') as f:
        json.dump({'error': str(e)}, f)
