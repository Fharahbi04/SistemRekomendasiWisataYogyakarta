# -*- coding: utf-8 -*-
"""MLTerapanSistemRekomendasi.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1FNLmJCjkn2TSK5xa1UUG4WjhkRoDNYsf

# **Sistem Rekomendasi Wisata Yogyakarta**

Indonesia adalah negara yang kaya akan keindahan alam dan juga budaya. Banyak turis atau wisatawan lokal yang sering berpergian pada tempat-tempat tertentu seperti contohnya pada Daerah Istimewa Yogyakarta,oleh karena itu untuk mempermudah wisatawan untuk mendapatkan rekomendasi wisata yang ingin dituju,sistem rekomendasi kali ini dapat membantu para wisatawan tersebut terkhusus di Yogyakarta.

**Sumber Dataset:** [Sistem Rekomendasi Wisata Yogyakarta](https://www.kaggle.com/datasets/aprabowo/indonesia-tourism-destination/data)

## **Import Library**
"""

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras import layers,regularizers,Input,Model
# from tensorflow.keras.layers import Embedding, Dot, Flatten, Input
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, precision_score

"""## **Load Data**"""

wisata= pd.read_csv('tourism_with_id.csv') # fungsi untuk membaca data dengan tipe .csv
wisata.head() # Menampilkan 5 baris teratas pada tabel

"""**Insight:** Tabel dari tempat wisata"""

user= pd.read_csv('user.csv') # fungsi untuk membaca data dengan tipe .csv
user.head() # Menampilkan 5 baris teratas pada tabel

"""**Insight:** Tampilan tabel user"""

rating_wisata = pd.read_csv('tourism_rating.csv') # fungsii untuk membaca data dengan tipe .csv
rating_wisata.head() # Menampilkan 5 baris teratas pada tabel

"""**Insight:** Tabel dari raing wisata

## **Exploratory Analysis Data (EDA)**

### Data Understanding
"""

print ("Jumlah Wisata: ",len(wisata.Place_Id.unique())) # Menampilkan jumlah wisata
print ("Jumlah User: ",len(user.User_Id.unique())) # Menampilkan jumlah user
print ("Jumlah Rating: ",len(rating_wisata.Place_Id.unique())) # Menampilkan jumlah rating

"""**Insight:**
- Terdapat 437 Jumlah Wisata yang ada.
- Jumlah user sebanyak 300.
- Rating berdasarkan place_id berjumlah 437.
"""

print ("Jumlah Semua Data Wisata: ", len(wisata)) # Menampilkan jumlah semua wisata
print ("Jumlah Semua Data User: ", len(user)) # Menampilkan jumlah semua user
print ("Jumlah Semua Data Rating: ", len(rating_wisata)) # Menampilkan jumlah semua rating

"""**Insight:**
- Jumlah semua data wisata adalah 437.
- Jumlah semua user adalah 300.
- Jumlah semua rating adalah 10000.
"""

wisata.info() #Menampilkan info dari tabel wisata

"""**Insight:** Terdapat 13 kolom dengan tipe data 5 objek,3 integer,dan 5 float kemudian data yang kosong pada kolom unnamed 11 dan Time_Minutes,kemudian pada preprocessing,data kosong serta kolom unnamed 11 dan 12 akan di drop."""

wisata.isna().sum() # Melihat jumlah data yang kosong dari tiap kolom

"""**Insight:** 232 data kosong pada kolom time_minutes dan 437 data kosong pada kolom unnamed: 11."""

wisata.duplicated().sum() # Melihat jumlah data yang duplikat

wisata.shape # Melihat jumlah baris dan kolom

"""**Insight:**Tidak terdapat data yang terduplikat"""

user.info() #Menampilkan info dari tabel user

"""**Insight:** Terdapat 3 kolom dengan tipe data  yaitu 2 integer dan 1 object,dan tidak terdapat data kosong."""

user.duplicated().sum() # Melihat jumlah data yang duplikat

user.shape # Melihat jumlah baris dan kolom

"""**Insight:**Tidak terdapat data yang duplikat"""

rating_wisata.info() #Menampilan info dari tabel rating_wisata

"""**Insight:** Terdiri dari 3 kolom bertipe numerik dengan 3 integer dan tidak terdapat data yang kosong."""

rating_wisata.duplicated().sum() # Melihat jumlah data yang duplikat

rating_wisata.shape # Melihat jumlah baris dan kolom

"""**Insight:** Terdapat data yang terdupliat sebanyak 79, akan tetapi kita ingin mempertahankan data tersebut,karena satu user bisa saja memberikan rating dan tempat untuk diberikan rating secara berulang.

### Data Preprocessing & Preparation
"""

print('Data :', len(wisata.Place_Id.unique())) #Menampilkan jumlah data
print('Kota:', wisata.City.unique()) #Menampilkan nama-nama kota

"""**Insight:** Terdapat 5 kota yaitu Jakarta Yogyakarta Bandung Semarang dan Surabaya"""

wisata = wisata.drop(columns=['Unnamed: 11'], axis=1) #Menghapus kolom unnamed: 11
wisata = wisata.drop(columns=['Unnamed: 12'], axis=1) #Menghapus kolom unnamed: 12
wisata = wisata.dropna() #Menghapus data kosong
wisata.head() #Menampilkan 5 baris teratas pada tabel wisata

"""**Insight:**Berhasil menghapus data kosong dan kolom yang tidak diperlukan yaitu unnamed: 11 dan 12"""

# Melihat sebaran distribusi data wisata dan kota
Fitur = 'City'
count = wisata[Fitur].value_counts()
percent = 100*wisata[Fitur].value_counts(normalize=True)
city = pd.DataFrame({'jumlah Sebaran Data Wisata dan kota':count, 'persentase':percent.round(1)})
print(city)
count.plot(kind='bar', title=Fitur);

"""**Insight:**Dari data sebaran diatas Yogyakarta memiliki jumlah wisata yang tinggi dengan nilai 60 atau 29% dari total semua wisata di tiap kota. Oleh karena itu sistem rekomendasi kali ini mengambil data Yogyakarta.

"""

# Mengambil kota yogyakarta
wisataYogyakata= wisata[wisata['City']=='Yogyakarta']
wisataYogyakata

"""**Insight:**Tampilan wisata di Yogyakarta"""

# Mengambil rating pada Yogyarkarta
rating_jogja = pd.merge(rating_wisata, wisataYogyakata[['Place_Id']], how='right', on='Place_Id')
rating_jogja

"""**Insight**:Mengambil Data Rating Wisata Jogja untuk mengambil rating yang hanya di jogja dan untuk membuat model"""

#Mengambil data user dan digabungkan pada rating yogyakarta
user_jogja = pd.merge(user, rating_jogja[['User_Id']], how='right', on='User_Id').drop_duplicates().sort_values('User_Id')
user_jogja

"""**Insight:** Menggabungkan data user dengan rating pada yogyakarta untuk membuat model."""

#Menggabungkan semua data wisata pada Yogyakarta
Yogyakarta = rating_jogja
Yogyakarta

"""**Insight:**Sebelum membuat model,kita harus menggabungkan semua data rating dan tempat."""

#Menghaous data yang terduplikat
Yogyakarta = Yogyakarta.drop_duplicates('Place_Id')

#Menggabungkan semua data
allYogyakarta = pd.merge(Yogyakarta, wisataYogyakata[['Place_Id','Place_Name','Category']], on='Place_Id', how='left')
allYogyakarta.head()

"""**Insight:**Menggabungkan semua data dan siap membuat model dengan conten based filtering."""

# Melihat banyaknya wisata di Yogyakarta
print('Banyak Data Wisata Yogyakarta :', len(allYogyakarta.Place_Name.unique()))

"""**Insight:** Banyak data pada Yogyakarta adalah 60"""

# Melihat distribusi jenis wisata yang ada di Yogyakarta
feature = 'Category' # Mengambil fitur/kolom kategori
count = allYogyakarta[feature].value_counts() #menghitung jumlah ketegori
percent = 100*allYogyakarta[feature].value_counts(normalize=True) #membuat persentase wisata
kategori = pd.DataFrame({'jumlah Sebaran Jenis/Tipe Wisata Yogyakarta':count, 'persentase':percent.round(1)}) #menampilkan tipe,jumlah dan persentase data
print(kategori)
count.plot(kind='bar', title=feature); #menampilkan grafik perbandingan

"""**Insight:**Membuat distribusi tipe wista guna untuk mengetahui jenis wisata apa yang paling banyak dan disi didapatkan bahwa taman hiburan yang paling banyak disusul dengan cagar alam."""

new_jogja= allYogyakarta[['Place_Id','Place_Name','Category']] #Mengambil kolom yang diperlukan
new_jogja.head()

"""**Insight:**Menampilkan fitur-fitur yang diperlukan untuk conten based filtering

## **Build Model**

### Model Conten Based Filtering
"""

# Inisialisasi TfidfVectorizer
cv = CountVectorizer()

cv.fit(allYogyakarta['Category'])
# Mengganti get_feature_names() dengan get_feature_names_out() karena get_feature_names() sudah deprecated
cv.get_feature_names_out()

"""**Insight:** Menginisialisasi tfidf vektorizer untuk mengubah teks menjadi representasi numerik (fitur)

"""

tfidf_matrix = cv.fit_transform(allYogyakarta['Category'])# Mengambil kolom categori
tfidf_matrix.shape #melihat hasil

"""**Insight:**mengubah setiap entri teks dalam kolom 'Category' menjadi vektor angka berdasarkan jumlah kemunculan kata CountVectorizer atau bobot TF-IDF TfidfVectorizer."""

# Menghitung Similarty
cos = cosine_similarity(tfidf_matrix)
cos

"""**insight:**Menghitung similarity dari transform category sebelumnya"""

# Convert the cosine similarity matrix to a DataFrame with Place_Name as index and columns
cos_df = pd.DataFrame(cos, index=allYogyakarta['Place_Name'], columns=allYogyakarta['Place_Name'])

"""**Insight:**Berfungsi untuk mengonversi matriks similarity (dalam hal ini cosine similarity) menjadi sebuah DataFrame pandas yang lebih mudah dibaca dan diakses.


"""

# Fungsi untuk memberikan rekomendasi tempat wisata di Yogyakarta
# berdasarkan kemiripan cosine similarity terhadap tempat wisata yang diberikan.

def rekomenjogja(wisataJogja, similarity_data=cos_df, items=allYogyakarta[['Place_Name', 'Category']], k=5):
    # wisataJogja       : string nama tempat wisata sebagai acuan rekomendasi
    # similarity_data   : DataFrame cosine similarity antar tempat wisata (default: cos_df)
    # items             : DataFrame berisi informasi nama dan kategori tempat wisata
    # k                 : jumlah rekomendasi tempat wisata yang ingin ditampilkan (default: 5)

    # Ambil indeks tempat wisata yang paling mirip berdasarkan similarity
    index = similarity_data.loc[:, wisataJogja].to_numpy().argpartition(
        range(-1, -k, -1))

    # Ambil nama tempat wisata terdekat berdasarkan skor similarity
    closest = similarity_data.columns[index[-1:-(k+2):-1]]

    # Hapus nama tempat wisata acuan agar tidak direkomendasikan ke dirinya sendiri
    closest = closest.drop(wisataJogja, errors='ignore')

    # Gabungkan hasil rekomendasi dengan data kategori tempat wisata
    return pd.DataFrame(closest).merge(items).head(k)

"""**Insight:**Fungsi wisata berhasil dibuat dan siap untuk di implementasi"""

#Implementasi
rekomenjogja('Situs Warungboto')

"""**Insight:**5 rekomendasi ketika user mengunjungi situs warung boto"""

#Mengevaluasi model conten based dengan precission@k
def precision_at_k(wisataJogja, k=5):
    # Ambil kategori tempat acuan
    kategori_target = allYogyakarta.loc[allYogyakarta['Place_Name'] == wisataJogja, 'Category'].values[0]

    # Ambil rekomendasi
    hasil_rekomendasi = rekomenjogja(wisataJogja, k=k)

    # Hitung berapa yang kategori-nya sama → dianggap relevan
    hasil_rekomendasi['Relevan'] = hasil_rekomendasi['Category'].apply(lambda x: x == kategori_target)

    # Precision@K = jumlah yang relevan dibagi total yang direkomendasikan (k)
    precision = hasil_rekomendasi['Relevan'].sum() / k

    return precision

# Contoh evaluasi
p_at_5 = precision_at_k('Situs Warungboto', k=5)
print(f'Precision@k untuk "Situs Warungboto": {p_at_5:.2f}')

"""**Insgiht:**Berdasarkan hasil pengujian dengan precission@k pada "situs warung boto" mendapatkan hasil 1.00 dimana ke 5 konten rekomendasi yang ditampilkan sesuai,dan memiliki kesamaan yang sangat mirip.

### Colaborative filtering
"""

# Mengambil daftar unik User_Id dari dataset rating_jogja
user = rating_jogja['User_Id'].unique().tolist()
print('list userID: ', user)

# Membuat dictionary pemetaan dari User_Id asli ke indeks numerik (encoding user)
user_encoded = {x: i for i, x in enumerate(user)}
print('encoded userID : ', user_encoded)

# Membuat dictionary kebalikan: dari indeks numerik ke User_Id asli
user_encoded_user = {i: x for i, x in enumerate(user)}
print('encoded angka ke userID: ', user_encoded_user)

"""**Insight:**Berhasil memasukkan ke dalam list."""

# Mengambil daftar unik Place_Id (tempat wisata) dari dataset
wisata = rating_jogja['Place_Id'].unique().tolist()

# Membuat dictionary pemetaan dari Place_Id asli ke indeks numerik (encoding wisata)
wisata_encoded = {x: i for i, x in enumerate(wisata)}

# Membuat dictionary kebalikan: dari indeks numerik ke Place_Id asli
wisata_encoded_wisata = {i: x for i, x in enumerate(wisata)}

"""**Insight:**Berhasil mengambil place_id dan memasukkannya kedalam list"""

# Menambahkan kolom baru 'user' di dataframe rating_jogja dengan hasil encoding user
rating_jogja['user'] = rating_jogja['User_Id'].map(user_encoded)

# Menambahkan kolom baru 'wisata' di dataframe rating_jogja dengan hasil encoding wisata
rating_jogja['wisata'] = rating_jogja['Place_Id'].map(wisata_encoded)

"""**Insight:**Menggabungkan kolom baru yaitu user dan wisata"""

# Normalisasi rating
min_rating = rating_jogja['Place_Ratings'].min()
max_rating = rating_jogja['Place_Ratings'].max()

rating_jogja['Place_Ratings'] = rating_jogja['Place_Ratings'].astype(np.float32)

# Use the encoded 'user' and 'wisata' columns for training data
x = rating_jogja[['user', 'wisata']].values
y = rating_jogja['Place_Ratings'].apply(lambda r: (r - min_rating) / (max_rating - min_rating)).values

# Split train dan validation
x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, random_state=42)

"""**Insight:**Normalisasi rating dan spil data"""

#Membuat fungsi dari kolaboratif filtering
class CollaborativeFilteringModel(tf.keras.Model):
    def __init__(self, num_users, num_items, embedding_size=50):
        super(CollaborativeFilteringModel, self).__init__()
        self.user_embedding = tf.keras.layers.Embedding(num_users, embedding_size)
        self.item_embedding = tf.keras.layers.Embedding(num_items, embedding_size)

    def call(self, inputs):
        user_vec = self.user_embedding(inputs[:, 0])
        item_vec = self.item_embedding(inputs[:, 1])
        return tf.reduce_sum(user_vec * item_vec, axis=1)

"""**Insight:**Model Berhasil dibuat"""

# Inisialisasi model
num_users = len(user_encoded)
num_items = len(wisata_encoded)

model = CollaborativeFilteringModel(num_users, num_items)
model.compile(optimizer='adam', loss='mse')

# Callback untuk mencatat RMSE per epoch
class RMSELogger(tf.keras.callbacks.Callback):
    def __init__(self):
        super().__init__()
        self.val_rmse = []  # Menyimpan RMSE tiap epoch

    def on_epoch_end(self, epoch, logs=None):
        y_pred = self.model.predict(x_val)
        rmse = np.sqrt(mean_squared_error(y_val, y_pred))
        print(f"Epoch {epoch+1}, RMSE: {rmse:.4f}")
        self.val_rmse.append(rmse)

rmse_logger = RMSELogger()

# Training model dengan callback RMSELogger
history = model.fit(
    x_train, y_train,
    epochs=50,
    batch_size=64,
    verbose=1,
    callbacks=[rmse_logger]
)

"""**Insight:**Secara hasil RMSE berhasil turun"""

# Mengambil data loss dan RMSE
loss_values = history.history['loss']
rmse_values = rmse_logger.val_rmse
epochs = range(1, len(loss_values) + 1)

# Membuat visualisasi
fig, ax1 = plt.subplots(figsize=(8, 5))

# Plot Loss di sumbu Y kiri
color_loss = 'tab:blue'
ax1.set_xlabel('Epoch')
ax1.set_ylabel('MSE Loss', color=color_loss)
ax1.plot(epochs, loss_values, '-', color=color_loss, label='Loss')
ax1.tick_params(axis='y', labelcolor=color_loss)
ax1.grid(True)

# Plot RMSE di sumbu Y kanan (shared X-axis)
ax2 = ax1.twinx()
color_rmse = 'tab:green'
ax2.set_ylabel('Validation RMSE', color=color_rmse)
ax2.plot(epochs, rmse_values, '-', color=color_rmse, label='Validation RMSE')
ax2.tick_params(axis='y', labelcolor=color_rmse)

# Judul dan layout rapih
fig.suptitle('Training Loss and Validation RMSE per Epoch')
fig.tight_layout()

# Tampilkan plot
plt.show()

"""**Insight:**Berdasarkan visualisasi ke dua garisnya saling mengikuti"""

# Tentukan user ID yang ingin direkomendasikan
user_id = 10  # contoh user
user_idx = user_encoded[user_id]

# Buat pasangan (user, semua wisata)
all_wisata_idx = np.array(list(wisata_encoded.values()))
user_input = np.array([[user_idx, w] for w in all_wisata_idx])

# Prediksi rating
pred_ratings = model.predict(user_input)

# Denormalisasi (jika sebelumnya dilakukan normalisasi)
pred_ratings = pred_ratings * (max_rating - min_rating) + min_rating

# Urutkan berdasarkan rating tertinggi
top_indices = pred_ratings.argsort()[::-1]
top_wisata_ids = [list(wisata_encoded.keys())[i] for i in top_indices[:5]]
top_ratings = pred_ratings[top_indices[:5]]

# Tampilkan hasil rekomendasi lengkap dengan nama wisata
print("Top 5 Rekomendasi untuk User ID:", user_id)
for place, score in zip(top_wisata_ids, top_ratings):
    # Menggunakan DataFrame allYogyakarta untuk mendapatkan Place_Name
    place_name = allYogyakarta[allYogyakarta['Place_Id'] == place]['Place_Name'].values[0]
    print(f"{place_name} (ID: {place}): Predicted Rating = {score:.2f}")

"""**Insight:**Top 5 rekomendasi berdasarkan model colaboorative filtering."""