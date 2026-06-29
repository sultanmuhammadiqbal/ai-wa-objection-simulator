import os
import json
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from google import genai
from google.genai import types

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = FastAPI(title="WA Objection Simulator Core")
client = genai.Client()

# Trik Rp 0: Pakai list lokal di memori server buat simpen chat session sementara
chat_history = []

@app.get("/", response_class=HTMLResponse)
async def index():
    try:
        with open("index.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>File index.html tidak ditemukan!</h1>")

# ==================== FASE 1: GENERATOR SKRIP CLOSING ====================
@app.post("/generate-handler", response_class=HTMLResponse)
async def generate_handler(product_description: str = Form(...), objection_type: str = Form(...)):
    prompt = f"""
    Kamu adalah seorang pakar Copywriting Sales WhatsApp nomor satu di Indonesia.
    Tangani keberatan pembeli berdasarkan:
    - Deskripsi Produk: {product_description}
    - Tipe Keberatan: {objection_type}

    Berikan output WAJIB format JSON murni dengan key:
    1. "variasi_1": Balasan WA persuasif (Feel-Felt-Found).
    2. "variasi_2": Balasan WA taktis (Urgency/Scarcity).
    3. "variasi_3": Balasan WA halus (Gali kebutuhan).
    4. "follow_up": Chat follow-up esok harinya.
    5. "vo_edukasi": Skrip Voice Over pendek untuk edukasi produk ini.
    
    ATURAN KETAT VO: Maksimal 22 kata, fokus 100% pada keunggulan produk itu sendiri, dilarang keras membandingkan/menghubungkan dengan produk kompetitor lain!
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        res_data = json.loads(response.text)
        
        return f"""
        <div class="space-y-4">
            <div class="bg-gray-900/50 p-4 rounded-xl border border-gray-700 relative group">
                <div class="flex justify-between items-center mb-2">
                    <span class="text-xs font-bold text-blue-400 block">Variasi 1: Feel-Felt-Found</span>
                    <button onclick="copyToClipboard('copy-v1', this)" class="text-gray-500 hover:text-blue-400 transition text-[10px] flex items-center gap-1 bg-gray-800 hover:bg-gray-700 px-2 py-0.5 rounded border border-gray-700 cursor-pointer">
                        Copy
                    </button>
                </div>
                <p id="copy-v1" class="text-sm text-gray-200 whitespace-pre-wrap select-all">{res_data.get('variasi_1', '')}</p>
            </div>
            
            <div class="bg-gray-900/50 p-4 rounded-xl border border-gray-700 relative group">
                <div class="flex justify-between items-center mb-2">
                    <span class="text-xs font-bold text-amber-400 block">Variasi 2: Urgency & Scarcity</span>
                    <button onclick="copyToClipboard('copy-v2', this)" class="text-gray-500 hover:text-amber-400 transition text-[10px] flex items-center gap-1 bg-gray-800 hover:bg-gray-700 px-2 py-0.5 rounded border border-gray-700 cursor-pointer">
                        Copy
                    </button>
                </div>
                <p id="copy-v2" class="text-sm text-gray-200 whitespace-pre-wrap select-all">{res_data.get('variasi_2', '')}</p>
            </div>
            
            <div class="bg-gray-900/50 p-4 rounded-xl border border-gray-700 relative group">
                <div class="flex justify-between items-center mb-2">
                    <span class="text-xs font-bold text-purple-400 block">Variasi 3: Gali Kebutuhan</span>
                    <button onclick="copyToClipboard('copy-v3', this)" class="text-gray-500 hover:text-purple-400 transition text-[10px] flex items-center gap-1 bg-gray-800 hover:bg-gray-700 px-2 py-0.5 rounded border border-gray-700 cursor-pointer">
                        Copy
                    </button>
                </div>
                <p id="copy-v3" class="text-sm text-gray-200 whitespace-pre-wrap select-all">{res_data.get('variasi_3', '')}</p>
            </div>
            
            <div class="bg-gray-900/50 p-4 rounded-xl border border-gray-700 relative group">
                <div class="flex justify-between items-center mb-2">
                    <span class="text-xs font-bold text-rose-400 block">Follow-up Besok Hari</span>
                    <button onclick="copyToClipboard('copy-fu', this)" class="text-gray-500 hover:text-rose-400 transition text-[10px] flex items-center gap-1 bg-gray-800 hover:bg-gray-700 px-2 py-0.5 rounded border border-gray-700 cursor-pointer">
                        Copy
                    </button>
                </div>
                <p id="copy-fu" class="text-sm text-gray-200 whitespace-pre-wrap select-all">{res_data.get('follow_up', '')}</p>
            </div>

            <div class="bg-green-500/10 p-4 rounded-xl border border-green-500/30 relative group">
                <div class="flex justify-between items-center mb-2">
                    <span class="text-xs font-bold text-green-400 block font-semibold">🎙️ Edukasi VO Video Pendek (Max 22 Kata)</span>
                    <button onclick="copyToClipboard('copy-vo', this)" class="text-gray-500 hover:text-green-400 transition text-[10px] flex items-center gap-1 bg-gray-800 hover:bg-gray-700 px-2 py-0.5 rounded border border-gray-700 cursor-pointer">
                        Copy
                    </button>
                </div>
                <p id="copy-vo" class="text-sm font-medium text-green-300 italic">"{res_data.get('vo_edukasi', '')}"</p>
                <span class="text-[10px] text-gray-500 mt-1 block">Panjang: {len(res_data.get('vo_edukasi', '').split())} kata</span>
            </div>
        </div>
        """
    except Exception as e:
        return f"<div class='p-4 bg-red-500/10 text-red-400 text-sm rounded-xl'>Error: {str(e)}</div>"

# ==================== FASE 2: SIMULATOR CHAT ====================
@app.post("/chat-init", response_class=HTMLResponse)
async def chat_init(product_desc: str = Form(...), persona: str = Form(...)):
    global chat_history
    chat_history = [] # Reset memory setiap mulai simulasi baru
    
    prompt = f"""
    Kamu berperan sebagai calon pembeli WhatsApp dari Indonesia dengan tipe persona: '{persona}'.
    Kamu tertarik tapi punya hambatan berat untuk beli produk ini: '{product_desc}'.
    
    TUGAS: Kirimkan 1 kalimat chat pertama di WA yang ketus, skeptis, atau menolak halus yang menunjukkan keberatanmu. 
    Gunakan gaya bahasa chat WA santai Indonesia asli. Jangan bertele-tele.
    """
    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        buyer_msg = response.text.strip()
        
        # Catat ke log memori
        chat_history.append({"speaker": f"Pembeli ({persona})", "message": buyer_msg})
        
        return f"""
        <div class="flex items-start mb-2 animate-fade-in">
            <div class="bg-gray-800 border border-gray-700 text-gray-200 p-3 rounded-2xl rounded-tl-none max-w-xs text-sm shadow-md">
                <span class="text-[10px] text-green-400 font-bold block mb-1">📱 Calon Pembeli ({persona})</span>
                {buyer_msg}
            </div>
        </div>
        """
    except Exception as e:
        return f"<p class='text-red-400 text-xs'>Gagal memicu pembeli: {str(e)}</p>"

@app.post("/chat-simulation", response_class=HTMLResponse)
async def chat_simulation(product_desc: str = Form(...), persona: str = Form(...), user_message: str = Form(...)):
    global chat_history
    chat_history.append({"speaker": "Anda (CS)", "message": user_message})
    
    prompt = f"""
    Kamu adalah calon pembeli WhatsApp Indonesia dengan persona: '{persona}'.
    Kamu sedang di-chat oleh CS yang mencoba menjual produk: '{product_desc}'.
    
    Riwayat obrolan sejauh ini:
    {json.dumps(chat_history, ensure_ascii=False)}
    
    Pesan terbaru dari CS adalah: "{user_message}"
    
    TUGAS KAMU:
    Balas chat CS tersebut tetap sesuai karakter personamu. Jika argumen CS sangat bagus dan meruntuhkan penolakanmu, kamu boleh melunak dan bilang mau order. Jika biasa saja, tetap ketus atau tolak.
    Gunakan gaya tulisan chat WA kasual Indonesia asli.
    """
    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        buyer_msg = response.text.strip()
        
        chat_history.append({"speaker": f"Pembeli ({persona})", "message": buyer_msg})
        
        user_bubble = f"""
        <div class="flex items-end justify-end mb-2">
            <div class="bg-green-600/30 border border-green-500/40 text-green-100 p-3 rounded-2xl rounded-tr-none max-w-xs text-sm shadow-md text-right">
                <span class="text-[10px] text-green-400 font-bold block mb-1">You (CS)</span>
                {user_message}
            </div>
        </div>
        """
        ai_bubble = f"""
        <div class="flex items-start mb-2">
            <div class="bg-gray-800 border border-gray-700 text-gray-200 p-3 rounded-2xl rounded-tl-none max-w-xs text-sm shadow-md">
                <span class="text-[10px] text-green-400 font-bold block mb-1">📱 Calon Pembeli ({persona})</span>
                {buyer_msg}
            </div>
        </div>
        """
        return user_bubble + ai_bubble
    except Exception as e:
        return f"<p class='text-red-400 text-xs'>Error: {str(e)}</p>"

# ==================== FASE 3: EVALUASI COACHING RAPOR ====================
@app.post("/evaluate-chat", response_class=HTMLResponse)
async def evaluate_chat():
    global chat_history
    if not chat_history:
        return "<p class='text-amber-400 text-sm text-center py-4'>Belum ada riwayat chat yang bisa dievaluasi, bro. Chat-chatan dulu sana!</p>"
    
    prompt = f"""
    Kamu adalah seorang Direktur Sales dan Ahli Psikologi Konsumen nomor satu di Asia Tenggara.
    Tugasmu adalah menganalisis riwayat percakapan WhatsApp antara CS (Anda) dan Calon Pembeli berikut ini:
    
    {json.dumps(chat_history, ensure_ascii=False)}
    
    Berikan penilaian kritis dan objektif dalam format JSON murni dengan key berikut (tanpa markdown bumbu tulisan lain):
    1. "skor": Angka dari 0 sampai 100 (seberapa besar peluang closing berdasarkan chat CS).
    2. "blunder": Analisis kesalahan fatal atau kata-kata kurang tepat yang dipakai CS (jelaskan dengan gaya santai tapi tajam).
    3. "kelebihan": Apa yang sudah bagus dari cara jawab CS.
    4. "rekomendasi": Contoh skrip balasan alternatif yang HARUSNYA diucapkan CS biar pembeli langsung transfer seketika.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        res_data = json.loads(response.text)
        
        skor = int(res_data.get('skor', 0))
        warna_skor = "text-red-400" if skor < 50 else "text-amber-400" if skor < 75 else "text-green-400"
        
        return f"""
        <div class="bg-gray-900 border border-gray-700 rounded-xl p-6 space-y-4 animate-fade-in mb-4">
            <div class="text-center border-b border-gray-800 pb-4">
                <h3 class="text-lg font-bold text-white mb-1">📊 RAPOR PERFORMA CLOSING CS</h3>
                <span class="text-5xl font-black {warna_skor}">{skor}/100</span>
            </div>
            <div>
                <strong class="text-sm text-red-400 block mb-1">❌ Analisis Blunder / Kelemahan:</strong>
                <p class="text-xs text-gray-300 bg-gray-950 p-3 rounded-lg border border-gray-800 leading-relaxed">{res_data.get('blunder', '')}</p>
            </div>
            <div>
                <strong class="text-sm text-green-400 block mb-1">✅ Poin Plus:</strong>
                <p class="text-xs text-gray-300 bg-gray-950 p-3 rounded-lg border border-gray-800 leading-relaxed">{res_data.get('kelebihan', '')}</p>
            </div>
            <div class="bg-green-500/10 p-4 rounded-lg border border-green-500/20">
                <strong class="text-sm text-green-400 block mb-1">💡 Saran Perbaikan Skrip (Golden Script):</strong>
                <p class="text-xs font-medium text-green-200 italic">"{res_data.get('rekomendasi', '')}"</p>
            </div>
        </div>
        """
    except Exception as e:
        return f"<div class='p-4 bg-red-500/10 text-red-400 text-sm rounded-xl'>Gagal Evaluasi: {str(e)}</div>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
