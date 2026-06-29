# 🚀 AI WhatsApp Funnel & Objection Handler Simulator

Aplikasi simulator interaktif berbasis AI ($0 Stack) yang dirancang untuk melatih tim Customer Service (CS) dan Digital Marketer lokal dalam mengatasi penolakan (*objection*) calon pembeli di WhatsApp guna menekan angka boncos iklan akibat gagal *closing*.

---

## 🎯 Masalah Pasar (The Pain Point)
Banyak bisnis online dan digital marketer lokal berhasil mendatangkan banyak *leads* chat WhatsApp lewat iklan (Facebook/TikTok/Google Ads), namun **boncos di fase akhir** karena tim CS gagal menangani keberatan konsumen seperti:
- "Kok harganya mahal ya?"
- "Ini barangnya ori atau KW?"
- "Bisa COD gak?"
- Tiba-tiba di-*ghosting* setelah tanya-tanya.

## 💡 Solusi yang Dibangun
Aplikasi localhost ini menyelesaikan masalah tersebut melalui 2 fitur utama:
1. **AI Script Generator:** Menghasilkan 3 variasi skrip balasan instan berdasarkan framework sales riil (*Feel-Felt-Found*, *Urgency/Scarcity*, dan *Deep Questioning*) serta skrip edukasi VO video pendek (maksimal 22 kata).
2. **Interactive Roleplay Simulator & Coach Review:** CS bisa melakukan simulasi *chatting* real-time melawan AI yang menyamar jadi buyer rewel (Emak-emak pelit, anak muda skeptis). Di akhir sesi, AI akan mengeluarkan **Rapor Performa** berisi skor closing, analisis blunder kata, dan rekomendasi *Golden Script*.

## 🛠️ Tech Stack & Arsitektur (Modal Rp 0)
Proyek ini dibangun menggunakan metode *Vibe Coding* dengan efisiensi biaya mutlak (Lokal Server):
- **Backend Core:** FastAPI (Python) - Ringan, cepat, dan *async default*.
- **Frontend UI:** HTML5 & Tailwind CSS (via CDN) - Tampilan premium, responsif, dan kontras tinggi.
- **Dynamic Interaction:** HTMX - Mengirim dan menukar komponen HTML secara *real-time* tanpa *load* JavaScript berat atau framework frontend rumit.
- **AI Brain:** Gemini API (`gemini-2.5-flash`) via Google AI Studio Free Tier.

---

## 🚀 Cara Menjalankan di Localhost

1. Clone repositori ini ke laptop lu.
2. Buat file `.env` di root folder dan masukkan API Key lu:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```
