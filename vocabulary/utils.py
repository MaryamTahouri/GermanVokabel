from gtts import gTTS
import os


def generate_audio_file(text, lang, directory, filename):
    """
    Generiert eine Audio-Datei mit gTTS und speichert sie in einem angegebenen Verzeichnis.

    :param text: Der Text, der in Audio umgewandelt werden soll
    :param lang: Die Sprache des Textes (z. B. 'de' für Deutsch, 'en' für Englisch)
    :param directory: Das Verzeichnis, in dem die Datei gespeichert werden soll
    :param filename: Der Name der Datei, die generiert werden soll
    :return: Der vollständige Pfad der generierten Datei
    """
    print(f"Generiere Audio für: {text} in Sprache: {lang}")
    print(f"Verzeichnis: {directory}")

    # Verzeichnis erstellen, falls es noch nicht existiert
    os.makedirs(directory, exist_ok=True)

    # Pfad zur Datei
    file_path = os.path.join(directory, filename)

    # Nur generieren, wenn die Datei noch nicht existiert
    if not os.path.exists(file_path):
        try:
            print(f"Erstelle gTTS-Datei: {file_path}")
            tts = gTTS(text=text, lang=lang)
            tts.save(file_path)
            print(f"Audio-Datei erfolgreich erstellt: {file_path}")
        except Exception as e:
            print(f"Fehler bei der Erstellung der Audio-Datei: {e}")
            return None

    return file_path
