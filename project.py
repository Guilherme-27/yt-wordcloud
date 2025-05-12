from wordcloud import WordCloud, STOPWORDS
import yt_dlp
import matplotlib.pyplot as plt
import re
import whisper
import torch


def sanitize_filename(title):
    # Removes invalid characters from the title to safely use as a filename

    return re.sub(r'[\\/*?:"<>|]', "_", title)

def download_audio(url):
    # Downloads the audio from the YouTube video and converts it to .mp3

    info_temp = yt_dlp.YoutubeDL().extract_info(url, download=False)
    safe_title = sanitize_filename(info_temp["title"])

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'audios/{safe_title}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return f'audios/{safe_title}.mp3'

def transcribe_audio(audio_path):
    # Loads the Whisper model and transcribes the audio file

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    if device == "cuda":
        print("✅ NVIDIA GPU detected. Using CUDA for faster transcription.")
    else:
        print("⚠️ No CUDA-compatible GPU found. Using CPU — transcription may take longer.")

    model = whisper.load_model('tiny', device=device)
    result = model.transcribe(audio_path)
    return result['text']

def generate_wordcloud(text):
    # Generates and displays a word cloud from the given text

    stopwords = set(STOPWORDS)
    stopwords_pt = { # Update stopwords for Portuguese (my language)
    "a", "o", "os", "as", "um", "uma", "uns", "umas",
    "de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas",
    "por", "com", "para", "pra", "sem", "sob", "sobre", "até", "entre",
    "e", "ou", "mas", "porque", "porém", "então", "que", "quando", "se", "como",
    "eu", "tu", "ele", "ela", "nós", "vós", "eles", "elas", "me", "te", "se", "nos", "vos",
    "isso", "isto", "aquilo", "esse", "essa", "aquele", "aquela", "aqui", "ali", "lá", "onde",
    "já", "vai", "tá", "né", "tipo", "daí", "aí", "bom", "só", "tudo", "nada",
    "mesmo", "também", "então", "assim", "agora", "pois", "bem", "cada", "mais", "menos",
    "ser", "estar", "ter", "fazer", "ir", "haver", "poder", "precisar", "querer"
    }
    stopwords.update(stopwords_pt)
    
    wordcloud = WordCloud(width=1280,
    height=1024,
    background_color='white',
    max_words=200,
    stopwords=stopwords,
    colormap='viridis',
    contour_color='black',
    contour_width=1,
    ).generate(text)

    plt.figure(figsize=(14, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig("nuvem.png", dpi=300)
    plt.show()

def main():
    url = input("Enter the YouTube video URL: ")
    audio_path = download_audio(url)
    print(f'Audio saved at: {audio_path}')
    
    transcription = transcribe_audio(audio_path)
    print('\n📝 Full transcription:\n')
    
    generate_wordcloud(transcription)
    
    with open("transcription.txt", "w", encoding="utf-8") as f:
        f.write(transcription)


if __name__ == "__main__":
    main()