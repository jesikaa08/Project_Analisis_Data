import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import matplotlib 

day_df = pd.read_csv("day.csv", delimiter=",")
day_df.to_csv("all_data.csv", index=False)
all_data = pd.read_csv("all_data.csv", delimiter=",")
# Grouping data per bulan dan tahun
monthly_rentals = all_data.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()

# Mengubah kolom 'yr' menjadi tahun sebenarnya (2011, 2012)
monthly_rentals['yr'] = monthly_rentals['yr'].map({0: 2011, 1: 2012})

# Menggabungkan kolom tahun dan bulan menjadi format tanggal
monthly_rentals['date'] = pd.to_datetime(monthly_rentals['yr'].astype(str) + '-' + monthly_rentals['mnth'].astype(str) + '-01')

# Judul aplikasi di Streamlit
st.title('Trend Penyewaan Sepeda')

# Membuat plot dengan Matplotlib
fig, axs = plt.subplots(2, 1, figsize=(12, 12))

# Plot tahun 2011
axs[0].plot(monthly_rentals[monthly_rentals['yr'] == 2011]['date'],
             monthly_rentals[monthly_rentals['yr'] == 2011]['cnt'],
             marker='o', color='skyblue')
axs[0].set_title('Trend Penyewaan Sepeda 2011')
axs[0].set_xlabel('Bulan')
axs[0].set_ylabel('Total Penyewaan')
axs[0].grid()

# Format sumbu x
axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%B'))
axs[0].set_xticks(monthly_rentals[monthly_rentals['yr'] == 2011]['date'])
axs[0].tick_params(axis='x', rotation=45)  # Memutar label sumbu x

# Plot tahun 2012
axs[1].plot(monthly_rentals[monthly_rentals['yr'] == 2012]['date'],
             monthly_rentals[monthly_rentals['yr'] == 2012]['cnt'],
             marker='o', color='orange')
axs[1].set_title('Trend Penyewaan Sepeda 2012')
axs[1].set_xlabel('Bulan')
axs[1].set_ylabel('Total Penyewaan')
axs[1].grid()

# Format sumbu x
axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%B'))
axs[1].set_xticks(monthly_rentals[monthly_rentals['yr'] == 2012]['date'])
axs[1].tick_params(axis='x', rotation=45)

# Layout agar plot tidak saling tumpang tindih
plt.tight_layout()

# Tampilkan plot di Streamlit
st.pyplot(fig)


# Menghitung total penyewaan untuk hari kerja dan akhir pekan/holiday
weekday_data = day_df[day_df['workingday'] == 1]['cnt']
weekend_holiday_data = day_df[(day_df['workingday'] == 0) | (day_df['holiday'] == 1)]['cnt']

# Total penyewaan
total_weekday_rentals = weekday_data.sum()
total_weekend_holiday_rentals = weekend_holiday_data.sum()

# Data untuk visualisasi
labels = ['Hari Kerja', 'Akhir Pekan/Holiday']
totals = [total_weekday_rentals, total_weekend_holiday_rentals]

# Judul aplikasi di Streamlit
st.title('Total Penyewaan Sepeda pada Hari Kerja vs Akhir Pekan/Holiday')

# Diagram batang
plt.figure(figsize=(5, 6))
plt.bar(labels, totals, color=['skyblue', 'orange'])
plt.title('Total Penyewaan Sepeda')
plt.xlabel('Jenis Hari')
plt.ylabel('Total Penyewaan')
plt.grid(axis='y')

# Menampilkan nilai total di atas batang
for index, value in enumerate(totals):
    plt.text(index, value, str(value), ha='center', va='bottom')

plt.tight_layout()

# Tampilkan plot di Streamlit
st.pyplot(plt)

# Data penyewaan per kondisi cuaca
clear = day_df[day_df['weathersit'] == 1]['cnt']
mist = day_df[day_df['weathersit'] == 2]['cnt']
light = day_df[day_df['weathersit'] == 3]['cnt']
heavy = day_df[day_df['weathersit'] == 4]['cnt']

# Total peminjaman untuk setiap kondisi cuaca
weather_data = pd.DataFrame({
    'Kondisi Cuaca': ['Clear', 'Mist', 'Light Rain/Snow', 'Heavy Rain/Snow'],
    'Total Peminjaman': [clear.sum(), mist.sum(), light.sum(), heavy.sum()]
})

# Judul aplikasi di Streamlit
st.title('Total Peminjaman Sepeda Berdasarkan Kondisi Cuaca')

# Diagram batang
plt.figure(figsize=(10, 6))
plt.bar(weather_data['Kondisi Cuaca'], weather_data['Total Peminjaman'], color=['skyblue', 'lightgreen', 'orange', 'red'])
plt.title('Total Peminjaman Sepeda Berdasarkan Kondisi Cuaca')
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Total Peminjaman')
plt.grid(axis='y')

# Menampilkan nilai total di atas batang
for index, value in enumerate(weather_data['Total Peminjaman']):
    plt.text(index, value, str(value), ha='center', va='bottom')

plt.tight_layout()

# Tampilkan plot di Streamlit
st.pyplot(plt)

# Menghitung korelasi
correlation = day_df['temp'].corr(day_df['cnt'])
st.title('Keterkaitan antara temperatur dan jumlah penyewaan sepeda')
st.write(f'Korelasi: {correlation:.2f}')

# Plot hubungan antara temperatur dan jumlah penyewaan
plt.figure(figsize=(10, 6))
sns.regplot(x=day_df['temp'] * 41, y=day_df['cnt'], scatter_kws={'alpha': 0.7}, line_kws={'color': 'red'})

# Menetapkan judul dan label sumbu
plt.title('Hubungan antara Temperatur dan Jumlah Penyewaan Sepeda dengan Garis Tren')
plt.xlabel('Temperatur (Celsius)')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.grid(True)

# Tampilkan plot di Streamlit
st.pyplot(plt)

st.title('Perbandingan penyewa kasual dan terdaftar')

# Total penyewa kasual dan terdaftar
total_casual = day_df['casual'].sum()
total_registered = day_df['registered'].sum()

# DataFrame untuk perbandingan
comparison_df = pd.DataFrame({
    'Tipe Penyewa': ['Kasual', 'Terdaftar'],
    'Total': [total_casual, total_registered]
})

# Visualisasi
plt.figure(figsize=(5, 5))
plt.bar(comparison_df['Tipe Penyewa'], comparison_df['Total'], color=['skyblue', 'lightgreen'])
plt.title('Total Penyewa Sepeda: Kasual vs Terdaftar')
plt.xlabel('Tipe Penyewa')
plt.ylabel('Total Penyewa')
plt.grid(axis='y')

# Menambahkan nilai total di atas batang
for index, value in enumerate(comparison_df['Total']):
    plt.text(index, value, str(value), ha='center', va='bottom')

# Tampilkan plot di Streamlit
st.pyplot(plt)

# Untuk membersihkan figure setelah ditampilkan
plt.clf() 


