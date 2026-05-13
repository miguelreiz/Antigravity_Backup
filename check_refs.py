import re, glob
chapters = glob.glob('Chapter_*_Complete.md')
res = []
for ch in chapters:
    text = open(ch, 'r', encoding='utf-8').read()
    cited = set(map(int, re.findall(r'\[(\d+)\]', text)))
    listed = set(map(int, re.findall(r'^(\d+)\.\s+', text, re.MULTILINE)))
    missing = sorted(listed - cited)
    unlisted = sorted(cited - listed)
    res.append(f'{ch}: Missing in text: {missing}, Not in bibliography: {unlisted}')
print('\n'.join(res))
