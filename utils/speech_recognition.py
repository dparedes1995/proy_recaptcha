import speech_recognition as sr
from pydub import AudioSegment
import httpx
from io import BytesIO
import logging


async def recognize_speech_from_url(audio_url):
    logging.info(f"Reconociendo habla desde URL: {audio_url}")
    recognizer = sr.Recognizer()

    async with httpx.AsyncClient() as client:
        response = await client.get(audio_url)

    audio_bytes = BytesIO(response.content)
    audio = AudioSegment.from_file(audio_bytes)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio_wav = BytesIO()
    audio.export(audio_wav, format="wav")
    audio_wav.seek(0)

    with sr.AudioFile(audio_wav) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            logging.info(f"Texto reconocido: {text}")
            return text
        except sr.UnknownValueError:
            logging.error("Google Speech Recognition no pudo entender el audio")
            return None
        except sr.RequestError as e:
            logging.error(f"No se pudo solicitar resultados de Google Speech Recognition; {e}")
            return None
