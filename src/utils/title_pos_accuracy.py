import pandas as pd
import ast
import re
from collections import defaultdict

# ====================== CONFIGURATION ======================
TREAT_NOUN_PROPN_SAME = True

# Dependencies to completely ignore
IGNORE_DEPS = {'punct', 'det', 'cc', 'case', 'mark', 'dep', ''}

# Lenient dependency groups
DEP_GROUPS = {
    'modifier': {'compound', 'amod', 'nmod', 'appos'},
    'object':   {'dobj', 'pobj', 'iobj'},
    'subject':  {'nsubj', 'csubj'},
    'root':     {'ROOT', 'root'}
}

# ====================== HELPER FUNCTIONS ======================
def normalize_label(label):
    if not isinstance(label, str): return ''
    label = label.strip().upper()
    label = re.sub(r'[,.!]+$', '', label).strip()
    norm_map = {
        'nsubje': 'nsubj', 'nusbj': 'nsubj', 'root ': 'ROOT',
        'coumpound': 'compound', 'compopund': 'compound',
        'subj': 'nsubj', 'amode': 'amod', 'admod': 'amod',
        'VEBR': 'VERB', 'Noun': 'NOUN',
    }
    return norm_map.get(label, label)

def normalize_pos(pos):
    pos = normalize_label(pos)
    if TREAT_NOUN_PROPN_SAME and pos in ['NOUN', 'PROPN']:
        return 'NOUN'
    return pos

def normalize_dep(dep):
    if not isinstance(dep, str): return ''
    dep = dep.strip().upper()
    dep = re.sub(r'[,.!]+$', '', dep).strip()
    
    for group_name, labels in DEP_GROUPS.items():
        if dep in labels:
            return group_name.upper()
    return dep

# ====================== LOAD & MERGE ======================
df_spacy = pd.read_csv("data/processed/title_pos_sample_500.csv").rename(columns={'Unnamed: 0': 'id'})
df_gold  = pd.read_csv("data/processed/title_pos_sample_200_gold.csv").rename(columns={'Unnamed: 0': 'id'})

df_spacy = df_spacy.add_prefix('spacy_')
df_gold  = df_gold.add_prefix('gold_')

df = pd.merge(df_spacy, df_gold, left_on='spacy_id', right_on='gold_id', how='inner')
df = df.drop(columns=['gold_id'])
df = df.rename(columns={'spacy_id': 'id', 'spacy_title': 'title'})

# ====================== PARSING ======================
def parse_spacy(row):
    try:
        s = str(row['spacy_pos_title_with_deps']).strip()
        if s.startswith('[') and s.endswith(']'):
            parsed = ast.literal_eval(s)
            return [(t[0], normalize_pos(t[1]), normalize_dep(t[2])) for t in parsed]
        return []
    except:
        return []

def parse_and_normalize_gold(row):
    gold = []
    for i in range(1, 19):
        col = f'gold_word_{i}'
        if col in df.columns and pd.notna(row[col]):
            val = str(row[col]).strip()
            if val:
                parts = [p.strip() for p in val.split(',')]
                if len(parts) >= 2:
                    token = parts[0].strip()
                    pos = normalize_pos(parts[1])
                    dep = normalize_dep(parts[2]) if len(parts) > 2 else ''
                    gold.append((token, pos, dep))
    return gold

df['spacy_parsed'] = df.apply(parse_spacy, axis=1)
df['gold_normalized'] = df.apply(parse_and_normalize_gold, axis=1)

# ====================== ACCURACY CALCULATION ======================
pos_correct = dep_correct = full_correct = total_tokens = 0
mismatches = 0

# Per-POS and Per-Dep statistics
pos_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
dep_stats = defaultdict(lambda: {'correct': 0, 'total': 0})

for _, row in df.iterrows():
    sp = row['spacy_parsed']
    go = row['gold_normalized']
    
    if len(sp) != len(go):
        mismatches += 1
        length = min(len(sp), len(go))
    else:
        length = len(sp)
    
    for i in range(length):
        total_tokens += 1
        s_tok, s_pos, s_dep = sp[i]
        g_tok, g_pos, g_dep = go[i]
        
        pos_match = s_pos == g_pos
        dep_match = False
        
        if s_dep in IGNORE_DEPS and g_dep in IGNORE_DEPS:
            dep_match = True
        elif s_dep == g_dep:
            dep_match = True
        else:
            for group in DEP_GROUPS.values():
                if s_dep in group and g_dep in group:
                    dep_match = True
                    break
        
        if pos_match: 
            pos_correct += 1
            pos_stats[s_pos]['correct'] += 1
        if dep_match: 
            dep_correct += 1
            dep_stats[s_dep]['correct'] += 1
        
        if pos_match and dep_match: 
            full_correct += 1
        
        pos_stats[s_pos]['total'] += 1
        dep_stats[s_dep]['total'] += 1

print("=== OVERALL LENIENT ACCURACY ===")
print(f"Treat NOUN/PROPN as same : {TREAT_NOUN_PROPN_SAME}")
print(f"Total titles             : {len(df)}")
print(f"Length mismatches        : {mismatches}")
print(f"Total tokens             : {total_tokens}")
print(f"POS Accuracy             : {pos_correct/total_tokens*100:.2f}%")
print(f"Dependency Accuracy      : {dep_correct/total_tokens*100:.2f}%")
print(f"Full (POS+Dep) Accuracy  : {full_correct/total_tokens*100:.2f}%")

print("\n=== ACCURACY PER POS TAG ===")
print(f"{'POS':<8} {'Accuracy':<10} {'Correct/Total'}")
for pos in sorted(pos_stats.keys()):
    stats = pos_stats[pos]
    acc = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
    print(f"{pos:<8} {acc:6.2f}%     {stats['correct']}/{stats['total']}")

print("\n=== ACCURACY PER DEPENDENCY TYPE ===")
print(f"{'Dep':<12} {'Accuracy':<10} {'Correct/Total'}")
for dep in sorted(dep_stats.keys()):
    stats = dep_stats[dep]
    acc = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
    print(f"{dep:<12} {acc:6.2f}%     {stats['correct']}/{stats['total']}")

# ====================== SAVE FILES ======================
df.to_csv("data/processed/title_pos_accuracy_comparison_lenient.csv", index=False)

# Token-level comparison
comparison_rows = []
for _, row in df.iterrows():
    sp = row['spacy_parsed']
    go = row['gold_normalized']
    max_len = max(len(sp), len(go))
    for i in range(max_len):
        s_tok = s_pos = s_dep = g_tok = g_pos = g_dep = ''
        if i < len(sp): s_tok, s_pos, s_dep = sp[i]
        if i < len(go): g_tok, g_pos, g_dep = go[i]
        comparison_rows.append({
            'id': row['id'],
            'title': row['title'],
            'token_index': i+1,
            'spacy_token': s_tok,
            'spacy_pos': s_pos,
            'spacy_dep': s_dep,
            'gold_token': g_tok,
            'gold_pos': g_pos,
            'gold_dep': g_dep,
            'pos_match': s_pos == g_pos,
            'dep_match': (s_dep == g_dep or 
                         (s_dep in IGNORE_DEPS and g_dep in IGNORE_DEPS) or
                         any(s_dep in g and g_dep in g for g in DEP_GROUPS.values())),
            'full_match': (s_pos == g_pos) and 
                         (s_dep == g_dep or 
                          (s_dep in IGNORE_DEPS and g_dep in IGNORE_DEPS) or
                          any(s_dep in g and g_dep in g for g in DEP_GROUPS.values()))
        })

comparison_df = pd.DataFrame(comparison_rows)
comparison_df.to_csv("data/processed/token_level_comparison_lenient.csv", index=False)

print("\nFiles saved:")
print("→ title_pos_accuracy_comparison_lenient.csv")
print("→ token_level_comparison_lenient.csv")