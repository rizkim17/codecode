import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, roc_curve

st.set_page_config(page_title="Prediksi FoMO", layout="wide")
st.title("Sistem Prediksi FoMO (Fear of Missing Out)")

# Upload CSV
uploaded_file = st.file_uploader("Unggah file CSV data kuesioner:", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Praproses
    df = df.dropna(subset=['Nama'])
    median_fomo = df['Total_Skor_FoMO'].median()
    df['FOMO_kategori'] = np.where(df['Total_Skor_FoMO'] >= median_fomo, 1, 0)

    # Encoding
    df['Gender'] = df['Jenis Kelamin'].map({'Laki-laki': 0, 'Perempuan': 1})
    usage_map = {'<1 jam': 0, '1–3 jam': 1, '4–6 jam': 2, '>6 jam': 3}
    df['Usage'] = df['Rata-rata waktu menggunakan media sosial per hari  '].map(usage_map)
    platform_dummies = pd.get_dummies(df['Platform media sosial yang paling sering digunakan  '], prefix='Plat')
    df = pd.concat([df, platform_dummies], axis=1)

    features = ['Usia', 'Gender', 'Usage', 'Total_Skor_Intensitas_Medsos',
                'Total_Skor_Kontrol_Regulasi_Diri'] + list(platform_dummies.columns)
    X = df[features]
    y = df['FOMO_kategori']

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Prediksi
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_proba)

    st.subheader("Evaluasi Model")
    st.write(f"**Akurasi:** {acc:.2f}")
    st.write(f"**Precision:** {prec:.2f} | **Recall:** {rec:.2f} | **F1-score:** {f1:.2f}")
    st.write(f"**AUC-ROC:** {roc_auc:.2f}")

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    fig_cm, ax_cm = plt.subplots()
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Rendah", "Tinggi"], yticklabels=["Rendah", "Tinggi"])
    ax_cm.set_xlabel("Prediksi")
    ax_cm.set_ylabel("Aktual")
    ax_cm.set_title("Confusion Matrix")
    st.pyplot(fig_cm)

    # ROC Curve
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    fig_roc, ax_roc = plt.subplots()
    ax_roc.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}")
    ax_roc.plot([0, 1], [0, 1], linestyle='--')
    ax_roc.set_xlabel("False Positive Rate")
    ax_roc.set_ylabel("True Positive Rate")
    ax_roc.set_title("ROC Curve")
    ax_roc.legend()
    st.pyplot(fig_roc)

    # Tampilkan tabel prediksi
    st.subheader("Data dengan Prediksi FoMO")
    df_test = X_test.copy()
    df_test['Prediksi_FoMO'] = y_pred
    df_test['Aktual_FoMO'] = y_test.values
    df_test['Prediksi_FoMO'] = df_test['Prediksi_FoMO'].map({0: 'Rendah', 1: 'Tinggi'})
    df_test['Aktual_FoMO'] = df_test['Aktual_FoMO'].map({0: 'Rendah', 1: 'Tinggi'})
    st.dataframe(df_test.reset_index(drop=True))
else:
    st.info("Silakan unggah file CSV untuk mulai analisis.")
