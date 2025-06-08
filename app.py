import streamlit as st
import pandas as pd
import numpy as np
from faker import Faker
import random
from io import BytesIO
import matplotlib.pyplot as plt

fake = Faker()

def generate_data(topic, num_records):
    data = []
    if topic == "Healthcare":
        for _ in range(num_records):
            data.append({
                "Patient Name": fake.name(),
                "Age": random.randint(1, 100),
                "Gender": random.choice(["Male", "Female"]),
                "Diagnosis": random.choice(["Diabetes", "Hypertension", "Asthma", "None"]),
                "Admission Date": fake.date_this_year(),
                "Discharged": random.choice(["Yes", "No"])
            })
    elif topic == "Finance":
        for _ in range(num_records):
            data.append({
                "Customer Name": fake.name(),
                "Account Type": random.choice(["Savings", "Checking", "Loan"]),
                "Balance": round(random.uniform(1000, 100000), 2),
                "Credit Score": random.randint(300, 850),
                "Loan Approved": random.choice(["Yes", "No"])
            })
    elif topic == "Education":
        for _ in range(num_records):
            data.append({
                "Student Name": fake.name(),
                "Grade": random.choice(["A", "B", "C", "D"]),
                "Major": random.choice(["CS", "Math", "Physics", "History"]),
                "GPA": round(random.uniform(2.0, 4.0), 2),
                "Graduated": random.choice(["Yes", "No"])
            })
    return pd.DataFrame(data)

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    output.seek(0)
    return output

def show_summary(df):
    st.markdown("### Summary Statistics")
    st.write(df.describe(include='all'))

    st.markdown("### Visualizations")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if numeric_cols:
        for col in numeric_cols:
            fig, ax = plt.subplots()
            df[col].hist(bins=20, ax=ax)
            ax.set_title(f'Distribution of {col}')
            st.pyplot(fig)
    else:
        st.info("No numeric columns to show histograms.")

st.title("SynGen - Synthetic Dataset Generator")

# Sidebar - options
st.sidebar.header("Configuration")
topic = st.sidebar.selectbox("Select dataset topic", ["Healthcare", "Finance", "Education"])
num_records = st.sidebar.slider("Number of records", 10, 1000, 100)

if st.sidebar.button("Generate Dataset"):
    df = generate_data(topic, num_records)
    st.success(f"Generated {num_records} records for {topic} dataset.")
    st.dataframe(df)

    show_summary(df)

    csv = df.to_csv(index=False)
    excel = convert_df_to_excel(df)
    json_data = df.to_json(orient="records", indent=2)

    st.sidebar.markdown("### Download Options")
    st.sidebar.download_button("Download CSV", data=csv, file_name=f"{topic}_data.csv", mime="text/csv")
    st.sidebar.download_button("Download Excel", data=excel, file_name=f"{topic}_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.sidebar.download_button("Download JSON", data=json_data, file_name=f"{topic}_data.json", mime="application/json")
else:
    st.info("Configure options and click 'Generate Dataset' in the sidebar.")

