# SISTEM REKOMENDASI WISATA YOGYAKARTA
Proyek ini bertujuan untuk membangun model sistem rekomendasi Wisata di Yogyakarta menggunakan model content-based-filtering dan collaborative filtering.

## Sumber Dataset
Kagle:[Sistem Rekomendasi Wisata Yogyakarta](https://www.kaggle.com/datasets/aprabowo/indonesia-tourism-destination/data)

## Dataset
  - tourism_rating.csv (Terdapat 3 kolom dengan tipe data berbentuk integer)
  - tourism_with_id (Terdapat 13 kolom dengan tipe data 3 integer,5 objek, dan 5)
  - user.csv (Terdapat 3 kolom dengan tipe data 2 integer dan 1 objek )

### Fitur 
  - tourism_rating.csv:
   | No. | Nama Fitur       | Tipe Data |Deskripsi                                                                 |
   |-----|------------------|-----------|---------------------------------------------------------------------------|
   | 1   | `User_Id`        | Integer   | ID unik untuk setiap pengguna yang memberikan rating pada tempat wisata. |
   | 2   | `Place_Id`       | Integer   | ID unik untuk setiap tempat wisata yang dinilai oleh pengguna.           |
   | 3   | `Place_Ratings`  | Integer   | Nilai rating yang diberikan pengguna terhadap tempat wisata.             |

 - taourism_with_id:
   | No | Nama Kolom     | Tipe Data | Deskripsi                                                                 |
   |----|----------------|-----------|---------------------------------------------------------------------------|
   | 1  | Place_Id       | int64     | ID unik untuk setiap tempat wisata.                                       |
   | 2  | Place_Name     | object    | Nama tempat wisata.                                                      |
   | 3  | Description    | object    | Deskripsi atau informasi umum tentang tempat wisata.                     |
   | 4  | Category       | object    | Kategori dari tempat wisata (misalnya: Budaya, Taman Hiburan, dll).      |
   | 5  | City           | object    | Kota tempat lokasi wisata berada.                                        |
   | 6  | Price          | int64     | Harga tiket masuk dalam satuan Rupiah.                                   |
   | 7  | Rating         | float64   | Rating tempat wisata berdasarkan ulasan pengguna.                        |
   | 8  | Time_Minutes   | float64   | Estimasi waktu yang dihabiskan di tempat tersebut (dalam menit).         |
   | 9  | Coordinate     | object    | Representasi koordinat dalam bentuk string JSON (berisi lat dan lng).    |
   | 10 | Lat            | float64   | Latitude (garis lintang) lokasi wisata.                                  |
   | 11 | Long           | float64   | Longitude (garis bujur) lokasi wisata.                                   |
   | 12 | Unnamed: 11    | float64   | Kolom kosong/tidak terpakai (semua nilai NaN).                           |
   | 13 | Unnamed: 12    | int64     | Duplikasi dari Place_Id, tidak diperlukan.                               |

 - user.csv : 
   | No | Nama Kolom | Tipe Data | Deskripsi                                                                 |
   |----|------------|-----------|---------------------------------------------------------------------------|
   | 1  | User_Id    | int64     | ID unik yang merepresentasikan masing-masing pengguna.                    |
   | 2  | Location   | object    | Lokasi pengguna dalam format "Kota, Provinsi".                            |
   | 3  | Age        | int64     | Umur pengguna dalam satuan tahun.                                         |

## Tahapan Proyek
 - Load Dataset,kemudian melakukan Eksplorasi dan analisis dataset.
 Pemrosesan data dengan mengambil fitur dan labelnya.
 - Splitting data.
 - Membangun model content-based-filtering dan collaborative filtering.

## Library Yang Digunakan
 - `pandas`, `numpy`
 - `matplotlib`, `seaborn`
 - `sklearn` (model, preprocessing, evaluasi)
 - `tensorflow` (model collaborative filtering)

## Hasil Model
1. **Collaborative Filtering (Berbasis User/Item)**:
    - Berikut adalah 5 rekomendasi teratas untuk **User ID: 10** berdasarkan prediksi rating:

        | Rank | Place ID | Predicted Rating |
        |------|----------|------------------|
        | 1    | 134      | 5.00             |
        | 2    | 168      | 4.96             |
        | 3    | 145      | 3.03             |
        | 4    | 165      | 2.97             |
        | 5    | 122      | 2.75             |


2. **Content-Based Filtering**:
    - Berikut adalah hasil rekomendasi berdasarkan input `Situs Warungboto`:

      | No  | Place_Name                                | Category       |
      |-----|--------------------------------------------|----------------|
      | 0   | Jogja Exotarium                            | Taman Hiburan  |
      | 1   | Studio Alam Gamplong                       | Taman Hiburan  |
      | 2   | Bukit Lintang Sewu                         | Taman Hiburan  |
      | 3   | Puncak Kebun Buah Mangunan                 | Taman Hiburan  |
      | 4   | Desa Wisata Rumah Domes/Teletubbies        | Taman Hiburan  |
 