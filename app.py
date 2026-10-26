import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# KONFIGURASI HALAMAN
# =========================

st.set_page_config(
    page_title="Dashboard Data Fiskal",
    page_icon="📊",
    layout="wide"
)

# =========================
# MEMBACA DATA
# =========================

df = pd.read_csv("dataset_fiskal_97_hipoFull.csv")

# =========================
# JUDUL
# =========================

st.title("📊 Dashboard Data Fiskal")
st.markdown(
    "Dashboard ini menampilkan data fiskal dan indikator sosial ekonomi berdasarkan kota dan tahun."
)

# =========================
# SIDEBAR
# =========================

st.sidebar.header("🔎 Filter Data")

# Filter kota
kota_pilihan = st.sidebar.selectbox(
    "Pilih Kota",
    ["Semua Kota"] + sorted(df["Kota"].unique().tolist())
)

# Filter tahun
tahun_pilihan = st.sidebar.selectbox(
    "Pilih Tahun",
    ["Semua Tahun"] + sorted(df["Tahun"].unique().tolist())
)

# =========================
# FILTER DATA
# =========================

data = df.copy()

if kota_pilihan != "Semua Kota":
    data = data[data["Kota"] == kota_pilihan]

if tahun_pilihan != "Semua Tahun":
    data = data[data["Tahun"] == tahun_pilihan]

# =========================
# METRIK
# =========================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Kemiskinan",
    f"{data['KEMISKINAN'].mean():.2f}"
)

col2.metric(
    "Pengangguran",
    f"{data['PENGANGGURAN'].mean():.2f}"
)

col3.metric(
    "IPM",
    f"{data['IPM'].mean():.2f}"
)

col4.metric(
    "PAD",
    f"{data['PAD'].mean():.2f}"
)

st.divider()

# =========================
# GRAFIK KEMISKINAN
# =========================

st.subheader("📈 Perkembangan Kemiskinan")

if kota_pilihan == "Semua Kota":
    data_tahun = data.groupby("Tahun", as_index=False)["KEMISKINAN"].mean()

    fig1 = px.line(
        data_tahun,
        x="Tahun",
        y="KEMISKINAN",
        markers=True,
        title="Rata-rata Kemiskinan Berdasarkan Tahun"
    )

else:
    data_tahun = data.groupby("Tahun", as_index=False)["KEMISKINAN"].mean()

    fig1 = px.line(
        data_tahun,
        x="Tahun",
        y="KEMISKINAN",
        markers=True,
        title=f"Perkembangan Kemiskinan - {kota_pilihan}"
    )

st.plotly_chart(fig1, use_container_width=True)

# =========================
# GRAFIK PAD
# =========================

st.subheader("💰 Perkembangan PAD")

data_pad = data.groupby("Tahun", as_index=False)["PAD"].mean()

fig2 = px.bar(
    data_pad,
    x="Tahun",
    y="PAD",
    title="Rata-rata PAD Berdasarkan Tahun"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# HUBUNGAN PAJAK DAN KEMISKINAN
# =========================

st.subheader("🔎 Hubungan Pajak dengan Kemiskinan")

fig3 = px.scatter(
    data,
    x="DBH_PAJAK",
    y="KEMISKINAN",
    hover_data=["Kota", "Tahun"],
    title="DBH Pajak vs Kemiskinan"
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# TABEL DATA
# =========================

st.subheader("📋 Data")

st.dataframe(
    data,
    use_container_width=True
)
