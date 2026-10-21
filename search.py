import re
import pandas as pd
from rapidfuzz import process, fuzz

STOP = {"tablets", "tablet", "tabs", "tab", "film", "coated", "capsules", "caps", "capsule",
        "injection", "inj", "syrup", "suspension", "infusion", "cream", "ointment", "gel",
        "drops", "solution", "powder", "for", "with", "and", "per", "the", "sustain",
        "release", "enteric", "oral", "eye", "nasal", "lotion", "sachet", "vial"}

def load_data(path="data/jan_aushadhi_products.csv"):
    df = pd.read_csv(path)
    df["name_search"] = (df["name_search"].fillna("")
                         .str.replace(r"\s+", " ", regex=True).str.strip())
    return df

def _words(text):
    return [w for w in re.findall(r"[a-z]{4,}", text.lower()) if w not in STOP]

def build_vocab(df):
    vocab = set()
    for s in df["name_search"]:
        vocab.update(_words(s))
    return sorted(vocab)

def search(df, vocab, query, limit=6):
    """Return (rows, corrected_words). Empty rows = not found."""
    q = query.lower()
    q_words = [w for w in re.findall(r"[a-z]{3,}", q) if w not in STOP]
    q_nums = re.findall(r"\d+(?:\.\d+)?", q)
    if not q_words:
        return df.iloc[0:0], []
    corrected = []
    for w in q_words:
        m = process.extractOne(w, vocab, scorer=fuzz.ratio, score_cutoff=78)
        if m is None:
            return df.iloc[0:0], []
        corrected.append(m[0])
    mask = pd.Series(True, index=df.index)
    for w in corrected:
        mask &= df["name_search"].str.contains(w, regex=False)
    res = df[mask].copy()
    if res.empty:
        return res, corrected
    def strength_bonus(name):
        return sum(1 for n in q_nums
                   if re.search(rf"(?<![\d.]){re.escape(n)}(?![\d.])", name))
    res["_b"] = res["name_search"].map(strength_bonus)
    res["_single"] = res["name_search"].str.contains(r"\+").map(lambda x: 0 if x else 1)
    res = res.sort_values(["_b", "_single", "mrp_inr"], ascending=[False, False, True])
    return res.drop(columns=["_b", "_single"]).head(limit), corrected