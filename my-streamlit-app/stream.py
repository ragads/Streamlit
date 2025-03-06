import streamlit as st
import pandas as pd
import nltk
from fuzzywuzzy import process


nltk.download("punkt")


st.title("📢 Aerospace News Query Explorer")


uploaded_file = st.file_uploader("📂 Upload Aerospace News CSV", type=["csv"])

if uploaded_file is not None:
    
    df = pd.read_csv(uploaded_file)

    
    st.write("### 📊 Dataset Summary:")
    st.write(f"📌 **Total Rows:** {df.shape[0]}")
    st.write(f"📌 **Total Columns:** {df.shape[1]}")
    st.write(f"📌 **Unique Authors:** {df['Author Name'].nunique()}")
    st.write(f"📌 **Unique Websites:** {df['Website Name'].nunique()}")

    
    st.write("### 📝 Preview of Uploaded Data:")
    st.dataframe(df.head())

    
    st.write("## 🔎 Search News Titles & Descriptions")
    search_query = st.text_input("Enter a keyword to search in news titles & descriptions:")

    if search_query:
        filtered_df = df[
            df["News Title"].str.contains(search_query, case=False, na=False) |
            df["News Description"].str.contains(search_query, case=False, na=False)
        ]
        st.write(f"### 🔍 Search Results for: '{search_query}'")
        st.dataframe(filtered_df)

    
    st.write("## 🤖 Ask a Dataset Question")
    user_query = st.text_area("💬 Type a question (e.g., 'How many news articles?', 'total rows', 'unique authors'):")

    if user_query:
        user_query = user_query.lower() 

        
        query_mapping = {
            "total rows": f"📝 **Total News Articles:** {df.shape[0]}",
            "total columns": f"🔢 **Total Columns:** {df.shape[1]}",
            "unique authors": f"✍️ **Unique Authors:** {df['Author Name'].nunique()}",
            "number of authors": f"✍️ **Unique Authors:** {df['Author Name'].nunique()}",
            "unique websites": f"🌍 **Unique Websites:** {df['Website Name'].nunique()}",
            "top authors": f"🏆 **Top 5 Authors:**\n{df['Author Name'].value_counts().head(5)}",
            "top websites": f"🏅 **Top 5 Websites:**\n{df['Website Name'].value_counts().head(5)}",
        }

        
        best_match, score = process.extractOne(user_query, query_mapping.keys())

        
        st.write("## 📝 Answer:")
        answer_box = st.empty()
        
        if score > 70: 
            answer_box.info(query_mapping[best_match])
        else:
            answer_box.warning("🤔 Sorry, I didn't understand your question. Try asking about 'total rows', 'top authors', or 'unique websites'!")

else:
    st.warning("⚠️ Please upload a CSV file to start querying the dataset.")