import streamlit as st
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# --- GANTI DENGAN KUNCI SPOTIFY KAMU ---
CLIENT_ID = "ISI_CLIENT_ID_KAMU"
CLIENT_SECRET = "ISI_CLIENT_SECRET_KAMU"

# Autentikasi Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

@st.cache_data
def ambil_data_lagu(playlist_id):
    hasil = sp.playlist_tracks(playlist_id)
    semua_lagu = hasil['items']
    while hasil['next']:
        hasil = sp.next(hasil)
        semua_lagu.extend(hasil['items'])

    data = []
    for item in semua_lagu:
        track = item['track']
        fitur = sp.audio_features(track['id'])[0]
        if fitur:
            data.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'popularity': track['popularity'],
                'danceability': fitur['danceability'],
                'energy': fitur['energy'],
                'tempo': fitur['tempo'],
                'acousticness': fitur['acousticness'],
                'valence': fitur['valence']
            })
    return pd.DataFrame(data)

# Streamlit UI
st.title("🎵 Prediksi Popularitas Lagu Spotify")
st.markdown("Menggunakan regresi linear dari fitur audio.")

# Playlist Spotify Top 50 Global
playlist_id = "37i9dQZEVXbMDoHDwVN2tF"

with st.spinner("Mengambil data dari Spotify..."):
    df = ambil_data_lagu(playlist_id)

st.success("Data berhasil diambil!")

if not df.empty:
    st.dataframe(df.head())

    # Model
    fitur = ['danceability', 'energy', 'tempo', 'acousticness', 'valence']
    X = df[fitur]
    y = df['popularity']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = LinearRegression()
    model.fit(X_train, y_train)
    prediksi = model.predict(X_test)

    st.subheader("📊 Hasil Prediksi")
    hasil = pd.DataFrame({
        'Aktual': y_test,
        'Prediksi': prediksi
    }).reset_index(drop=True)
    st.dataframe(hasil)

    mse = mean_squared_error(y_test, prediksi)
    r2 = r2_score(y_test, prediksi)

    st.metric("MSE", f"{mse:.2f}")
    st.metric("R²", f"{r2:.2f}")
else:
    st.warning("Data tidak tersedia.")
