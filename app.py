import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def get_politician_summary(politician_name, df):
    df_filtered = df[df['Name'].str.contains(politician_name, case=False, na=False)]

    sentiment_counts = df_filtered['Sentiment'].value_counts().to_dict()

    parliamentary_work = df_filtered[['Activity', 'Description']].dropna().drop_duplicates().head(10)

    initiatives = df_filtered[['Scheme/Initiative', 'Description.1']].dropna().drop_duplicates().head(10)

    
    return {
        "sentiment_score": sentiment_counts,
        "parliamentary_work_summary": parliamentary_work,
        "initiatives_summary": initiatives,
    }

def main():
    st.title("Politician Report Card")

    file_path = 'final_dataset.csv'  
    df = pd.read_csv(file_path)

    politician_name = st.text_input("Enter the name of the politician:")

    if st.button("Generate Report"):
        if politician_name:
            summary = get_politician_summary(politician_name, df)

            st.subheader("Sentiment Scores")
            st.write(summary["sentiment_score"])

            
            st.subheader("Parliamentary Work")
            st.write(summary["parliamentary_work_summary"].to_html(index=False, escape=False), unsafe_allow_html=True)

            st.subheader("Initiative")
            st.write(summary["initiatives_summary"].to_html(index=False, escape=False), unsafe_allow_html=True)

            if summary["sentiment_score"]:
                plt.figure(figsize=(8, 8))
                plt.pie(
                    summary["sentiment_score"].values(),
                    labels=summary["sentiment_score"].keys(),
                    autopct='%1.1f%%',
                    startangle=140,
                    colors=sns.color_palette('viridis', len(summary["sentiment_score"]))
                )
                plt.title('Sentiment Distribution')
                st.pyplot(plt)
            else:
                st.write("No sentiment data available.")
        else:
            st.error("Please enter a valid politician name.")

if __name__ == '__main__':
    main()
