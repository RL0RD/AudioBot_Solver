import os
import urllib.request
import pydub
import speech_recognition as sr
import time
from DrissionPage.common import Keys
from DrissionPage import ChromiumPage


class Captcha_Atack:
    # Acceso a la web
    def __init__(self, driver: ChromiumPage):
        self.driver = driver
    
    def solveCaptcha(self):
        # Busqueda de la sección Captcha
        iframe_inner = self.driver("@title=reCAPTCHA")
        time.sleep(0.1)
        
        # Clic en el frame reCAPTCHA
        iframe_inner('.rc-anchor-content', timeout=1).click()
        self.driver.wait.ele_displayed("xpath://iframe[contains(@title, 'recaptcha')]", timeout=3)

        # Si se da el caso que se auto valide
        if self.isSolved():
            return
        
        # Visualizar nuevo iframe
        iframe = self.driver("xpath://iframe[contains(@title, 'recaptcha')]")

        # Clic en botón audio
        self.driver("xpath://button[@id='recaptcha-audio-button']", timeout=1).click()   # Cambiar por xpath del boton de audio 
        
        # Obtención de enlace de audio
        src = self.driver("xpath://audio[@id='audio-source']").attrs['src'] # Cambiar por xpath del boton de reproducir
        print(src)
        
        # Obtener la ruta del directorio actual
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Ruta para el archivo MP3
        path_to_mp3 = os.path.join(current_dir, "song_key.mp3")
        
        # Descargar el audio formato MP3
        urllib.request.urlretrieve(src, path_to_mp3)

        # Conversión mp3 a wav
        path_to_wav = os.path.join(current_dir, "song_key.wav")

        sound = pydub.AudioSegment.from_mp3(path_to_mp3)
        sound.export(path_to_wav, format="wav")

        # Reconocer el audio
        r = sr.Recognizer()
        with sr.AudioFile(path_to_wav) as source:
            audio = r.record(source)

        # Verifica la duración del audio
        print(f"Duración del audio: {len(audio.frame_data) / audio.sample_rate} segundos")

        # Reconocer el audio
        try:
            key = r.recognize_google(audio, language='es-ES')
            print(key)
        except sr.UnknownValueError:
            raise Exception("Google Speech Recognition no comprendio el audio")
        except sr.RequestError as e:
            raise Exception(f"No hay conexion con Google Speech Recognition service; {e}")

        # Escribiendo la validación
        self.driver('xpath://*[@id="audio-response"]').input(key.lower()) # Cambiar por xpath del textbox
        time.sleep(0.1)
        
        # Envío key
        self.driver('#audio-response').input(Keys.ENTER)
        time.sleep(4)

        # Verificación del captcha resuelto
        if self.isSolved():
            return
        else:
            raise Exception("Fallo al resolver captcha")

    def isSolved(self):
        try:
            element = self.driver.ele(".recaptcha-checkbox-checkmark", timeout=1)
            print(f"Elemento encontrado: {element.attrs}")
            return "style" in element.attrs
        except Exception as e:
            print(f"Error en isSolved: {e}")
            return False
