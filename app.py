import streamlit as st
import pandas as pd
import os
from io import BytesIO
import openpyxl

# Configure the Streamlit app's appearance and layout
st.set_page_config(page_title="Data Sweeper", layout="wide")
st.title("Data Sweeper")
st.write("Transform your files between CSV to Excel format with built-in data cleaning and visualization!")

# File uploader widget that accepts CSV and Excel files
uploaded_files = st.file_uploader("Choose a file (CSV or Excel)", type=['csv', 'xlsx'], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        # Extract the file extension to determine if it's CSV or Excel
        file_extension = os.path.splitext(file.name)[-1].lower()

        # Read the uploaded file into a pandas DataFrame based on its extension
        if file_extension == ".csv":
            df = pd.read_csv(file)
        elif file_extension == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_extension}")
            continue

       
      # Display uploaded file information (name and size)     
        st.write(f"file name: {file.name}")
        st.write("file size:  {file.size/1024}")
        
        # Preview the first 5 rows of the uploaded file
        st.write("🔍 **Preview of the Uploaded File:**")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🛠 **Data Cleaning Options**")
        if st.checkbox(f"Clean Data for `{file.name}`"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove Duplicates from `{file.name}`"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ **Duplicates removed successfully!**")

            with col2:
                if st.button(f"Fill Missing Values for `{file.name}`"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ **Missing values filled successfully!**")

        # Data Visualization
        st.subheader("📊 **Data Visualization**")
        if st.checkbox(f"Show Visualization for `{file.name}`"):
            numeric_cols = df.select_dtypes(include="number")
            if len(numeric_cols.columns) >= 2:
                st.bar_chart(numeric_cols.iloc[:, :2])
            else:
                st.write("⚠️ **Not enough numeric columns for visualization.**")

        # File Conversion Options
        st.subheader("🔄 **File Conversion Options**")
        conversion_type = st.radio(f"Convert `{file.name}` to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert `{file.name}`"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_extension, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine='openpyxl')
                file_name = file.name.replace(file_extension, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            # Download button
            st.download_button(
                label=f"⬇️ Download `{file.name}` as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type,
            )

        st.success(f"✅ **{file.name} processed successfully!**")
