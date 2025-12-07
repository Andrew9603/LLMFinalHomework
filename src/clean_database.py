from datasketch import MinHash, MinHashLSH
import re
def clean_xml_code(xml_str):
    cleaned = re.sub(r'<!--.*?-->', '', xml_str, flags=re.DOTALL)
    cleaned = '\n'.join([line.strip() for line in cleaned.split('\n')])
    return cleaned
def deduplicate_snippets(snippets, threshold=0.85):
    lsh = MinHashLSH(threshold=threshold, num_perm=128)
    hashes = []
    for idx, text in enumerate(snippets):
        m = MinHash(num_perm=128)
        for word in text.split():
            m.update(word.encode('utf-8'))
        lsh.insert(idx, m)
        hashes.append(m)
    unique_indices = set()
    for idx in range(len(hashes)):
        result = lsh.query(hashes[idx])
        if not result:
            unique_indices.add(idx)
    return [snippets[i] for i in unique_indices] 
cleaned = [clean_xml_code(s) for s in valid_snippets]
unique_snippets = deduplicate_snippets(cleaned)