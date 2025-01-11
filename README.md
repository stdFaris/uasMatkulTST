# SantaiRumah

Sebuah platform yang menghubungkan pengguna dengan penyedia jasa rumah tangga seperti pijat, pembantu rumah tangga, dan tukang kebun. Platform ini dirancang untuk mempermudah proses pencarian dan pemesanan jasa dengan sistem booking yang terorganisir.

## Fitur Utama

- Pemesanan jasa dengan durasi fleksibel (1 jam hingga bulanan)
- Sistem booking yang terorganisir untuk menghindari konflik jadwal
- Cooldown period 1 jam setelah layanan selesai sebelum slot berikutnya tersedia
- Antarmuka yang responsif untuk penggunaan di berbagai perangkat
- Manajemen jadwal otomatis untuk mencegah double booking

## Teknologi yang Digunakan

- **Frontend**:

  - React TypeScript (Vite)
  - Tailwind CSS untuk styling
  - Dihosting di Netlify

- **Backend**:

  - FastAPI (Python)
  - Dihosting di Railway menggunakan Docker

- **Database**:
  - PostgreSQL

## Tautan Proyek

Website dapat diakses di: [https://santairumah.netlify.app](https://santairumah.netlify.app)

## Kontributor

- Habib Akhmad Al Farisi (18222029)

## Cara Penggunaan

1. Kunjungi website SantaiRumah
2. Pilih jenis layanan yang dibutuhkan (pijat/pembantu rumah tangga/tukang kebun)
3. Pilih durasi layanan yang diinginkan
4. Pilih jadwal yang tersedia
5. Lakukan pemesanan

## Instalasi untuk Development

### Frontend

```bash
# Clone repository
git clone [URL_REPO]

# Masuk ke direktori frontend
cd frontend

# Install dependencies
npm install

# Jalankan development server
npm run dev
```

### Backend

```bash
# Masuk ke direktori backend
cd backend

# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Jalankan server
uvicorn main:app --reload
```

## Catatan Penting

- Sistem booking memiliki cooldown period 1 jam setelah setiap layanan selesai
- Pastikan untuk memperhatikan durasi layanan saat melakukan pemesanan
- Website bersifat responsif dan dapat diakses dari berbagai perangkat
