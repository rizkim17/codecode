import streamlit as st
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

st.set_page_config(page_title="Prediksi FoMO", layout="centered")

st.title("🎯 Prediksi Kecenderungan FoMO (Fear of Missing Out)")
st.write("Isi kuesioner berikut untuk melihat prediksi tingkat FoMO Anda.")

# ==== INPUT FORM ====
usia = st.slider("Usia", 15, 30, 20)
gender = st.radio("Jenis Kelamin", ['Laki-laki', 'Perempuan'])
waktu = st.selectbox("Rata-rata waktu menggunakan media sosial per hari", ['<1 jam', '1–3 jam', '4-6 jam', '>6 jam'])

st.subheader("🔄 Intensitas Penggunaan Media Sosial")
intensitas = [st.slider(f"Pertanyaan Intensitas {i+1}", 1, 5, 3) for i in range(5)]

st.subheader("📱 Skala FoMO")
fomo = [st.slider(f"Pertanyaan FoMO {i+1}", 1, 5, 3) for i in range(7)]

# ==== PROSES ====
# Encode gender dan waktu
gender_num = 1 if gender == 'Laki-laki' else 0
waktu_map = {'<1 jam': 0.5, '1–3 jam': 2, '4-6 jam': 5, '>6 jam': 7}
waktu_num = waktu_map[waktu]

# Buat DataFrame fitur
total_intensitas = sum(intensitas)
fitur = np.array([
    usia,
    gender_num,
    waktu_num,
    *intensitas,
    *fomo,
    total_intensitas
]).reshape(1, -1)

# === Load Model dan Scaler ===
scaler = joblib.load("scaler.pkl")
model = joblib.load("model_logreg.pkl")

# ==== PREDIKSI ====
if st.button("Prediksi Sekarang"):
    fitur_scaled = scaler.transform(fitur)
    pred = model.predict(fitur_scaled)[0]
    label_map = {0: 'FoMO Rendah', 1: 'FoMO Sedang', 2: 'FoMO Tinggi'}
    st.success(f"Hasil Prediksi: **{label_map[pred]}** 🎉")
