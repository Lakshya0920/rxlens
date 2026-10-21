import streamlit as st
from search import load_data, build_vocab, search
from gemma import read_label

st.set_page_config(page_title="MedLens", page_icon="💊")

@st.cache_data
def get_data():
    df = load_data()
    return df, build_vocab(df)

df, vocab = get_data()

st.title("💊 MedLens")
st.caption("Find the Jan Aushadhi generic price for a medicine.")

photo = st.file_uploader("📷 Or upload a photo of the medicine strip or box",
                         type=["jpg", "jpeg", "png"])
if photo is not None:
    photo_id = f"{photo.name}-{photo.size}"
    if st.session_state.get("last_photo") != photo_id:
        with st.spinner("Gemma is reading the label..."):
            try:
                read = read_label(photo.getvalue(), photo.type)
            except Exception as e:
                read = ""
                st.error("Could not read the photo. You can type the name instead.")
                st.caption(f"Technical detail: {e}")
        st.session_state["last_photo"] = photo_id
        if read:
            st.session_state["q"] = read
        else:
            st.warning("No medicine name could be read from this photo. Please type it below.")
    st.image(photo, width=240)

query = st.text_input("Medicine name (spelling mistakes are okay)",
                      placeholder="e.g. paracetmol 500", key="q")
st.caption("If you used a photo, check the name above. The AI can misread blurry photos.")
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
st.info("MedLens shows price and medicine-name information only. It is not medical advice. "
        "Never switch medicines without confirming with your doctor or pharmacist.")