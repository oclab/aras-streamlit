import streamlit as st
import pandas as pd
import os
import pickle
from io import BytesIO
from openpyxl import load_workbook
from openpyxl.styles import PatternFill


# Load model
with open("svmmodel.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Fungsi untuk prediksi nilai
def predict_value(input_data):
    
    data = pd.read_excel(input_data)

    
    data.drop(columns=["no"], inplace=True)

    
    nama_nilai = data[['nama', 'nim']].copy()

    
    X = data.drop(columns=['nama','nim'])

    
    predictions = model.predict(X)

    
    data['Prediksi Nilai Akhir'] = predictions
    data['Prediksi Nilai Akhir'] = data['Prediksi Nilai Akhir'].replace({0: "tidak bermasalah", 1: "bermasalah"})

    return data, nama_nilai

# Judul aplikasi
st.title("Aplikasi Prediksi Mahasiswa Bermasalah")
st.caption("Menggunakan Machine Learning Support Vector Machine")

# Upload file Excel
uploaded_file = st.file_uploader("Upload file Excel untuk prediksi", type=["xlsx"])


# Buat list nama kolom
columns = ["no", "nama", "nim"] + [f"nilai - {i}" for i in range(1, 15)]

# Buat data contoh
data = [
    [1, "John", "NIM001"] + [-i for i in range(1, 15)],
    [2, "Alice", "NIM002"] + [-i for i in range(1, 15)],
    [3, "Bob", "NIM003"] + [-i for i in range(1, 15)]
]



# Membuat DataFrame dari data contoh
df_template = pd.DataFrame(data, columns = columns)

# Judul aplikasi
st.title("Unduh Template Excel")


# Membuat file Excel dalam bentuk BytesIO
output = BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df_template.to_excel(writer, sheet_name='Sheet1', index=False)

st.download_button("Download Template Excel", data=output, file_name="template_excel.xlsx", key="template_excel")

st.write("Contoh Data:")
st.write(df_template)


if uploaded_file is not None:
    
    result, nama_nilai = predict_value(uploaded_file)

    st.write("Hasil Prediksi:")
    st.write(result)

    
    final_result = pd.concat([nama_nilai, result['Prediksi Nilai Akhir']], axis=1)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        final_result.to_excel(writer, sheet_name='Sheet 1', index=False)
        input_data = pd.read_excel(uploaded_file)
        input_data.to_excel(writer,sheet_name='sheet 2',index = False)


    output.seek(0)
    st.download_button("Download Hasil Prediksi sebagai Excel", file_name="hasil_prediksi.xlsx", key="hasil_prediksi", data=output)

    
