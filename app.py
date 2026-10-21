import streamlit as st
from search import load_data, build_vocab, search

st.set_page_config(page_title="RxLens", page_icon="💊")

@st.cache_data
def get_data():
    df = load_data()
    return df, build_vocab(df)

df, vocab = get_data()

st.title("💊 RxLens")
st.caption("Find the Jan Aushadhi generic price for a medicine.")

query = st.text_input("Medicine name (spelling mistakes are okay)",
                      placeholder="e.g. paracetmol 500")
paid = st.number_input("Price you were charged for the same pack, ₹ (optional)",
                       min_value=0.0, step=1.0, value=0.0)

if query:
    results, corrected = search(df, vocab, query)
    if results.empty:
        st.warning("Not found in our Jan Aushadhi list. "
                   "Please check the spelling or ask your pharmacist.")
    else:
        if corrected:
            st.caption("Showing results for: " + ", ".join(corrected))
        labels = [f"{r['name']}  ({r['unit_size']})" for r in results.to_dict("records")]
        pick = st.selectbox("Pick the matching product", labels)
        row = results.iloc[labels.index(pick)]
        mrp = float(row["mrp_inr"])

        if paid > 0:
            if paid > mrp:
                saving = paid - mrp
                st.markdown(f"## ₹{paid:.0f} → ₹{mrp:.2f}")
                st.success(f"You could save ₹{saving:.2f} ({saving / paid * 100:.0f}%)")
            else:
                st.markdown(f"## Jan Aushadhi price: ₹{mrp:.2f}")
                st.info("The price you were charged is not higher than the Jan Aushadhi price.")
        else:
            st.markdown(f"## Jan Aushadhi price: ₹{mrp:.2f}")
        st.caption(f"Pack: {row['unit_size']} · Category: {row['group']} · "
                   "Compare with the same pack size.")

st.divider()
st.info("RxLens shows price and medicine-name information only. It is not medical advice. "
        "Never switch medicines without confirming with your doctor or pharmacist.")