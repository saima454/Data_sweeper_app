import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Configure the Streamlit app's appearance and layout
st.set_page_config(page_title="Data Sweeper", layout="wide")
st.title("Data Sweeper")
st.write("Transform your files between CSV to Excel formate with built_in data cleaning and visualization.!")

# File uploader widget that accepts CSV and Excel files

uploded_file = st.file_uploader("Choose a file (CSV or Excel)", type=['csv', 'xlsx'] , accept_multiple_files=True)

if uploded_file:

    for file in uploded_file:
       # Extract the file extension to determine if it's CSV or Excel
        file_extension = os.path.splitext(file.name)[-1].lower()

          # Read the uploaded file into a pandas DataFrame based on its extension
        if file_extension == ".csv":
            df = pd.read_csv(file)  # Read CSV files
       
        elif file_extension == ".xlsx":
            df = pd.read_excel(file)  # Read Excel files
       
        else:
            # Show an error message if the file type is unsupported
            st.error(f"Unsupported file type: {file_extension}")
            continue

        # Display uploaded file information (name and size)     
        st.write(f"file name: {file.name}")
        st.write("file size:  {file.size/1024}")


        # Preview the first 5 rows of the uploaded file
        st.write("🔍 Preview of the Uploaded File:")
        st.dataframe(df.head())  # Display a scrollable preview of the data

        # Display the data cleaning options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"cleaning Data for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed successfully!")


            with col2:
                if st.button(f"fill missing values for  {file.name}"):
                   numeric_cols =df.select_dtypes(include=['number']).colums
                   df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                   st.write("Missing values filled successfully!")

        #  create some visulization for
        st.subheader("Data Visualization") 
        if st.checkbox(f"show visulization for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])  # Plot the first two numeric columns as a bar chart

        # Section to choose file conversion type (CSV or Excel)
        st.subheader("File Conversion Options")
        conversion_type =st.radio(f"convert file{file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"convert{file.name}"):
          buffer = BytesIO()  # Creates in-memory buffer for file output
          if conversion_type == "CSV":
              df.to_csv(buffer,index=False)  # Save DataFrame as CSV in buffer
              file_name = file.name.replace(file_extension, ".csv")
              mime_type = "text/csv"
          elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine='openpyxl')  # Save as Excel using openpyxl
                file_name = file.name.replace(file_extension, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          buffer.seek(0)


        #   download button
        st.download_button(
            label=f"download {file.name} as {conversion_type}",
            data=buffer,
            filename=file_name,
            mime=mime_type,
            )
                  
                    
                
st.success("all files processed successfully!")



        