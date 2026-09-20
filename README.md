# 🛒 TokoKita API & Dashboard Store

Aplikasi Toko Online sederhana yang mengintegrasikan **RESTful API** berbasis **Python Flask**, basis data **SQLite**, dan antarmuka **Frontend Interaktif** (HTML/CSS/JS + Tailwind CSS) untuk mengelola katalog produk, stok, serta simulasi transaksi penjualan.

---

## 📸 Fitur Utama

- **Katalog Produk & Kasir**: Tampilan *card grid* interaktif untuk melihat stok, detail produk, dan melakukan checkout transaksi.
- **Manajemen Inventaris (CRUD Full)**:
  - **Create**: Menambahkan produk baru.
  - **Read**: Menampilkan daftar produk & detail spesifik per ID.
  - **Update**: Mengubah nama, harga, dan stok produk.
  - **Delete**: Menghapus produk dari database.
- **Transaksi Otomatis**: Menghitung total biaya pembelian secara otomatis dan mengurangi stok produk secara *real-time*.
- **Riwayat Transaksi**: Mencatat detail setiap transaksi yang berhasil dilakukan.
- **Dual Data Mode Switcher**:
  - **Mock Data Mode**: Menggunakan `LocalStorage` browser (cocok untuk pengujian tanpa server).
  - **Flask API Mode**: Terhubung langsung ke basis data SQLite melalui server Flask.

---

## 🛠️ Teknologi yang Digunakan

### Backend & Database
- **Python 3.x**
- **Flask**: Framework web mikro untuk membangun REST API.
- **Flask-CORS**: Mengatasi masalah Cross-Origin Resource Sharing (CORS).
- **SQLite3**: Database terembed (*file-based*) bawaan Python.

### Frontend
- **HTML5 & Vanilla JavaScript (ES6+)**
- **Tailwind CSS**: Styling UI modern via CDN.
- **Font Awesome 6**: Ikonografi antarmuka.

---

## 📁 Struktur Direktori

```text
my_project/
├── app.py              # File utama server Flask (Route & Database logic)
├── schema.sql          # Skema basis data SQLite
├── toko_online.db      # Database SQLite (dibuat otomatis saat app.py berjalan)
├── templates/
│   └── index.html      # Single Page Application (SPA) Frontend
└── README.md           # Dokumentasi Proyek

```

---

## 🚀 Cara Menjalankan Aplikasi

### 1. Persyaratan Sistem

Pastikan kamu telah menginstal Python di komputer kamu.

### 2. Instalasi Dependensi

Buka terminal/command prompt pada direktori proyek, lalu jalankan:

```bash
pip install flask flask-cors

```

### 3. Menjalankan Server

Jalankan file `app.py`:

```bash
python app.py

```

Secara otomatis, server akan:

1. Membuat database `toko_online.db` beserta tabel `produk` dan `transaksi` jika belum ada.
2. Menjalankan server lokal pada **`http://127.0.0.1:5000`**.

### 4. Mengakses Aplikasi

Buka browser dan kunjungi:

```text
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

```

> **Tips:** Pastikan sakelar **Mode Data** di pojok kanan atas aplikasi sudah diatur ke **Flask API**.

---

## 📖 Dokumentasi Endpoint API

### 1. Produk (`/api/produk`)

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| **GET** | `/api/produk` | Mengambil seluruh daftar produk. |
| **POST** | `/api/produk` | Menambahkan produk baru. |

**Contoh Body (POST `/api/produk`):**

```json
{
  "nama": "Sepatu Sneaker",
  "harga": 250000,
  "stok": 10
}

```

---

### 2. Detail & Manajemen Produk (`/api/produk/detail`)

| Method | Endpoint | Query Param | Deskripsi |
| --- | --- | --- | --- |
| **GET** | `/api/produk/detail` | `?id={id}` | Mengambil detail spesifik produk. |
| **PUT** | `/api/produk/detail` | `?id={id}` | Memperbarui data produk. |
| **DELETE** | `/api/produk/detail` | `?id={id}` | Menghapus produk dari database. |

**Contoh Body (PUT `/api/produk/detail?id=1`):**

```json
{
  "nama": "Sepatu Sneaker Premium",
  "harga": 275000,
  "stok": 12
}

```

---

### 3. Transaksi (`/api/transaksi`)

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| **GET** | `/api/transaksi` | Mengambil riwayat seluruh transaksi. |
| **POST** | `/api/transaksi` | Membuat transaksi baru dan mengurangi stok produk. |

**Contoh Body (POST `/api/transaksi`):**

```json
{
  "produk_id": 1,
  "jumlah": 2
}

```

---

## 🗄️ Skema Database (`schema.sql`)

```sql
CREATE TABLE IF NOT EXISTS produk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    harga REAL NOT NULL,
    stok INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS transaksi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produk_id INTEGER NOT NULL,
    jumlah INTEGER NOT NULL,
    total_harga REAL NOT NULL,
    tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produk_id) REFERENCES produk (id)
);

```

```
