import streamlit as st
import numpy as np
import joblib

st.set_page_config(page_title="Prediksi FoMO", layout="centered")
st.title("🎯 Prediksi Kecenderungan FoMO (Fear of Missing Out)")
st.markdown("Silakan isi kuesioner di bawah ini berdasarkan kondisi Anda saat ini.")

# ==== INPUT DASAR ====
usia = st.slider("Usia Anda", 15, 30, 20)
gender = st.radio("Jenis Kelamin", ['Laki-laki', 'Perempuan'])
waktu = st.selectbox("Berapa lama Anda rata-rata menggunakan media sosial per hari?", 
                     ['<1 jam', '1–3 jam', '4-6 jam', '>6 jam'])

# ==== PERTANYAAN INTENSITAS ====
st.subheader("🔄 Pertanyaan Intensitas Penggunaan Media Sosial (1–5)")
intensitas_questions = [
    "Saya membuka media sosial setiap kali memiliki waktu luang",
    "Saya menggunakan media sosial hampir setiap saat dalam sehari",
    "Saya merasa sulit untuk tidak membuka media sosial selama beberapa jam",
    "Saya selalu memulai dan mengakhiri hari dengan membuka media sosial",
    "Saya menghabiskan lebih dari 3 jam sehari di media sosial"
]
intensitas = [st.slider(q, 1, 5, 3, key=f"intensitas_{i}") for i, q in enumerate(intensitas_questions)]

# ==== PERTANYAAN FOMO ====
st.subheader("📱 Pertanyaan Skala FoMO (1–5)")
fomo_questions = [
    "Saya merasa cemas jika tidak membuka media sosial dalam beberapa jam",
    "Saya takut tertinggal informasi atau kegiatan teman-teman saya",
    "Saya merasa terganggu jika tidak bisa mengikuti update terbaru di media sosial",
    "Saya sering membandingkan hidup saya dengan apa yang saya lihat di media sosial",
    "Saya merasa perlu mengetahui semua yang terjadi dalam kehidupan orang lain",
    "Saya merasa harus langsung melihat notifikasi media sosial saat muncul",
    "Saya kesulitan fokus jika belum membuka media sosial dalam sehari"
]
fomo = [st.slider(q, 1, 5, 3, key=f"fomo_{i}") for i, q in enumerate(fomo_questions)]

# ==== ENCODING ====
gender_num = 1 if gender == 'Laki-laki' else 0
waktu_map = {'<1 jam': 0.5, '1–3 jam': 2, '4-6 jam': 5, '>6 jam': 7}
waktu_num = waktu_map[waktu]

# ==== FITUR FINAL ====
total_intensitas = sum(intensitas)
fitur = np.array([
    usia,
    gender_num,
    waktu_num,
    *intensitas,
    *fomo,
    total_intensitas
]).reshape(1, -1)

# ==== LOAD MODEL ====
scaler = joblib.load("scaler.pkl")
model = joblib.load("model_logreg.pkl")

# ==== PREDIKSI ====
if st.button("🔎 Prediksi FoMO Saya"):
    fitur_scaled = scaler.transform(fitur)
    pred = model.predict(fitur_scaled)[0]
    label_map = {0: 'FoMO Rendah 😌', 1: 'FoMO Sedang 😐', 2: 'FoMO Tinggi 😰'}
    st.success(f"Hasil Prediksi: **{label_map[pred]}**")
