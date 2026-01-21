
![Screenshot_21-1-2026_141542_localhost](https://github.com/user-attachments/assets/925a221b-7b97-403b-bffa-040ee7a4ba11)

Di bawah ini gue bikinin **INSTALLATION & RUN GUIDE LENGKAP** (rapi + teknis).

---

# 📡 Internet Stability Monitor

**Realtime Web-based Ping, Packet Loss & Dual Latency Monitor**

---

## 🎯 Fitur Utama

* Realtime ping monitoring (ICMP RTT & Process Latency)
* Packet loss windowed calculation
* Jitter & RTO detection
* Grafik dual latency realtime
* HUD style (inspired by DOTA 2 network stats)
* Start / Stop monitoring
* Target ping dinamis
* Status pintar (OK / WARN / BAD)

---

# 🛠️ REQUIREMENT

## 1️⃣ Software

Pastikan sudah terinstall:

| Software | Minimal Versi    |
| -------- | ---------------- |
| Python   | 3.8+             |
| pip      | Latest           |
| Browser  | Chrome / Firefox |

---

## 2️⃣ Python Libraries

Aplikasi ini menggunakan:

* Flask
* Flask-SocketIO
* eventlet

---

# 📁 STRUKTUR PROJECT

```
internet-monitor/
│
├── app.py
├── monitor.py
├── requirements.txt
│
├── templates/
│   └── index.html
│
└── static/ (optional kalo mau pisahin style/script)
    ├── style.css
    └── main.js
```

---

# 📦 INSTALLATION

## 1️⃣ Clone / Copy Project

Masuk ke folder project:

```bash
cd internet-monitor
```

---

## 2️⃣ Buat Virtual Environment (SANGAT DISARANKAN)

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

### `requirements.txt`

```txt
flask
flask-socketio
eventlet
```

Install dengan:

```bash
pip install -r requirements.txt
```

---

# ▶️ MENJALANKAN APLIKASI

## 1️⃣ Jalankan Server

```bash
python app.py
```

Jika berhasil, akan muncul:

```
 * Running on http://127.0.0.1:5000
 * Monitoring ready
```

---

## 2️⃣ Buka Web UI

Buka browser dan akses:

```
http://localhost:5000
```

---

# 🎮 CARA MENGGUNAKAN APLIKASI

## 1️⃣ Pilih Target Ping

Di kolom **Target** masukkan alamat:

```
8.8.8.8
```

atau:

```
1.1.1.1
google.com
```

---

## 2️⃣ Klik Tombol START

* Tombol berubah menjadi **STOP (merah)**
* Monitoring dimulai
* HUD & grafik bergerak realtime

---

## 3️⃣ Informasi yang Ditampilkan

### 🔹 HUD

| Elemen          | Penjelasan              |
| --------------- | ----------------------- |
| ICMP RTT        | Ping asli (seperti CMD) |
| Process Latency | Delay OS / aplikasi     |
| Packet Loss     | Kehilangan paket (%)    |
| Jitter          | Fluktuasi latency       |
| RTO             | Jumlah timeout          |
| Status          | OK / WARN / BAD         |
| Jam             | Waktu realtime          |

---

### 🔹 Grafik

* Garis 1: **ICMP RTT**
* Garis 2: **Process Latency**
* Gap = indikasi delay non-jaringan

---

## 4️⃣ Klik STOP

* Monitoring berhenti
* Data grafik tidak bertambah
* CPU kembali idle

---

# 🧠 INTERPRETASI DATA (PENTING)

| Kondisi                   | Arti                       |
| ------------------------- | -------------------------- |
| ICMP kecil, Process besar | OS / CPU delay             |
| Dua-duanya tinggi         | ISP / jaringan bermasalah  |
| Packet loss naik          | Koneksi tidak stabil       |
| Jitter tinggi             | Micro-stutter (gaming lag) |
| Status BAD                | Koneksi bermasalah serius  |

---

# ⚠️ CATATAN PENTING

* **Gunakan ICMP RTT untuk kualitas jaringan**
* **Process latency ≠ kualitas ISP**
* Jangan jalankan tanpa `socketio.sleep()` → CPU 100%
* Windows Firewall bisa memblok ping (allow ICMP)

---

# 🧪 TROUBLESHOOTING

### ❌ Tidak ada data muncul

* Pastikan klik **START**
* Pastikan target valid
* Cek terminal tidak error

### ❌ Ping selalu LOSS

* Firewall block ICMP
* Jalankan CMD:

```bash
ping 8.8.8.8
```

# 🏆 PENUTUP

Project ini:

* ❌ Bukan sekadar ping biasa
* ✅ Sudah **network monitoring tool**
* ✅ Cocok buat gamer, ISP complain, NOC
* ✅ Kuat buat portfolio
