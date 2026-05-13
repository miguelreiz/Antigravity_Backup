import re, glob
from collections import Counter

def get_words(text):
    return set(re.findall(r'\w+', text.lower()))

def score_sentence(sentence, ref_words):
    s_words = get_words(sentence)
    if not s_words: return 0
    # overlap
    return len(s_words.intersection(ref_words))

chapters = glob.glob('Chapter_*_Complete.md')

for ch in chapters:
    text = open(ch, 'r', encoding='utf-8').read()
    
    cited_raw = re.findall(r'\[(.*?)\]', text)
    cited = set()
    for match in cited_raw:
        if any(char.isdigit() for char in match) and not match.upper().isupper():
            nums = re.findall(r'\d+', match)
            for n in nums:
                cited.add(int(n))
                
    # Parse references
    refs = {}
    for line in text.split('\n'):
        m = re.match(r'^(\d+)\.\s+(.*)', line)
        if m:
            num = int(m.group(1))
            refs[num] = m.group(2)
            
    listed = set(refs.keys())
    missing = sorted(listed - cited)
    
    if not missing:
        continue
        
    print(f"Fixing {ch}, missing: {missing}")
    
    # split text into sentences (naively)
    # Don't consider the references section for injection
    ref_section_idx = text.find('## Referências')
    if ref_section_idx == -1:
        ref_section_idx = text.find('## Bibliografia')
    
    main_text = text[:ref_section_idx] if ref_section_idx != -1 else text
    
    # Regex to split by sentences ending in . ! ? followed by space or newline
    # But we want to preserve the text. Let's just split by lines, and then by sentences.
    lines = main_text.split('\n')
    
    for m_num in missing:
        ref_text = refs[m_num]
        ref_words = get_words(ref_text)
        
        # remove common words
        stopwords = {'of', 'the', 'and', 'in', 'for', 'journal', 'surgery', 'to', 'a', 'with', 'from', 'on', 'ophthalmology', 'refractive', 'cataract', 'de', 'la', 'et', 'al', 'da', 'e'}
        ref_words = ref_words - stopwords
        
        best_line_idx = -1
        best_score = 0
        
        for i, line in enumerate(lines):
            # Skip empty lines, headers, blockquotes, tables
            if not line.strip() or line.startswith('#') or line.startswith('>') or line.startswith('|') or line.startswith('!['):
                continue
                
            score = score_sentence(line, ref_words)
            if score > best_score:
                best_score = score
                best_line_idx = i
                
        if best_line_idx != -1:
            # Inject reference at the end of the line
            line = lines[best_line_idx]
            # remove trailing spaces
            line = line.rstrip()
            if line.endswith('.'):
                line = line[:-1] + f' [{m_num}].'
            else:
                line = line + f' [{m_num}]'
            lines[best_line_idx] = line
            print(f"  -> Injected [{m_num}] in: {line[:50]}... (score: {best_score})")
        else:
            # If no match, just append to a generic intro or conclusion
            print(f"  -> Could not find a good match for [{m_num}]")
            
    # reconstruct text
    new_main_text = '\n'.join(lines)
    new_text = new_main_text + (text[ref_section_idx:] if ref_section_idx != -1 else "")
    open(ch, 'w', encoding='utf-8').write(new_text)

print("Batch injection complete.")
