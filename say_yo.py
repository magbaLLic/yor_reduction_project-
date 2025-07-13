import gzip, json, re, csv, collections
from tqdm import tqdm

FILE = 'fake_faker.json.gz'        
RE_YOR = re.compile(r'\b\w+[ıiuü]yor\b', re.I)
RE_YO  = re.compile(r'\b\w+[ıiuü]yo\'?\b', re.I)

cnt = collections.Counter()

open_func = gzip.open if FILE.endswith('.gz') else open
with open_func(FILE, 'rt', encoding='utf8') as fp: 
    for line in tqdm(fp, desc='Tweet taranıyor'):
        tw  = json.loads(line)
        txt = tw['text'].lower()
        # kaba Türkçe filtresi
        if not any(ch in txt for ch in 'ığşçöü'):
            continue
        hr = tw['created_at'][11:13]      
        if RE_YOR.search(txt):
            cnt[(hr,'yor')] += 1
        if RE_YO.search(txt):
            cnt[(hr,'yo')] += 1
        RE_YO = re.compile(r'\b\w+[ıiuü]yo\'?\b(?![a-zçğıöşü])', re.I)
       

with open('saat_sayim.csv', 'w', newline='', encoding='utf8') as f:
    w = csv.writer(f); w.writerow(['saat','yo','yor'])
    for h in range(24):
        w.writerow([h, cnt.get((f'{h:02}','yo'), 0), cnt.get((f'{h:02}','yor'), 0)])

print('✓ saat_sayim.csv oluşturuldu')
