import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, executor
from yt_dlp import YoutubeDL
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- ЖӨНДӨӨЛӨР ---
TOKEN = '8672995204:AAEkdFdEDeZdl2AuLKRJklgMAwfxqBsrnUM'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Render үчүн жасалма порт (аны өчүрүп салбашы үчүн)
def run_dummy_server():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running!")
    port = int(os.environ.get("PORT", 8080))
    httpd = HTTPServer(('', port), Handler)
    httpd.serve_forever()

# Музыка жүктөө жөндөөлөрү
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': True,
    'noplaylist': True
}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("🎵 **Салам! Мен музыка издөөчү ботмун.**\n\nМага музыканын атын же ырчынын атын жазсаңыз, мен сизге таап берем.")

@dp.message_handler()
async def search_music(message: types.Message):
    query = message.text
    if query.startswith('/'): return
    
    status_msg = await message.answer("🔎 **Издеп жатам...**")

    try:
        # Издөө жана жүктөө
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
            title = info.get('title', 'music')
            # Файлдын атын табуу
            file_path = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp3"
            
            await status_msg.edit_text("📤 **Жүктөп жатам...**")
            
            # Музыканы жөнөтүү
            with open(file_path, 'rb') as audio:
                await message.answer_audio(audio, caption=f"🎵 {title}\n✅ Даяр болду!")
            
            await status_msg.delete()
            
            # Файлды өчүрүү (память толбошу үчүн)
            if os.path.exists(file_path):
                os.remove(file_path)

    except Exception as e:
        logging.error(e)
        await status_msg.edit_text("❌ Кечириңиз, музыка табылган жок же ката кетти.")

if __name__ == '__main__':
    # Папка түзүү
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    # Жасалма серверди иштетүү
    Thread(target=run_dummy_server, daemon=True).start()
    
    print("Музыка бот ишке кирди!")
    executor.start_polling(dp, skip_updates=True)
          
