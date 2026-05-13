import re, glob
chapters = glob.glob('Chapter_*_Complete.md')
res = []
for ch in chapters:
    text = open(ch, 'r', encoding='utf-8').read()
    
    cited_raw = re.findall(r'\[(.*?)\]', text)
    cited = set()
    for match in cited_raw:
        if any(char.isdigit() for char in match) and not match.upper().isupper():
            nums = re.findall(r'\d+', match)
            for n in nums:
                cited.add(int(n))
                
    listed = set(map(int, re.findall(r'^(\d+)\.\s+', text, re.MULTILINE)))
    
    missing = sorted(listed - cited)
    unlisted = sorted(cited - listed)
    
    if missing or unlisted:
        res.append(f'{ch}: \n  Faltam no texto: {missing}\n  Não estão na bibliografia: {unlisted}')

print('\n'.join(res))