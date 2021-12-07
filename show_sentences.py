import streamlit as st
import numpy as np
import pandas as pd

@st.cache()
def load_data():
    data = pd.read_pickle("outdir/merged.pkl")
    data = data.dropna()
    return data

data = load_data()


chapter = str(st.sidebar.slider("Chapter", 1, 26))

type_ = st.sidebar.multiselect(
    "Type",
    data.type.unique(),
    data.type.unique()
)

unique_labels = list(set([label for ll in data.annotations for label in ll]))
included_labels = st.sidebar.multiselect(
    "Included labels",
    unique_labels,
    unique_labels
)



filtered_data = data[
    np.logical_and.reduce([
        data.chapter == chapter,
        data.type.isin(type_),
        data.annotations.apply(lambda x: any(label in x for label in included_labels))
    ])
]

for type_, subdf in filtered_data.sort_values("sentence_id").groupby("type"):
    st.subheader(type_)
    for _,sentence in subdf.iterrows():
        st.write(f"""
        **{", ".join(sentence.annotations)}**\n
        {sentence.text}
        """)  
    
    


