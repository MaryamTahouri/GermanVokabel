from django.db import models
from django.conf import settings
from .utils import generate_audio_file  # Importiere die Funktion aus utils.py
import os
from django.contrib.auth.models import User


class Word(models.Model):
    # Allgemeine Felder
    german_word = models.CharField(max_length=50)
    farsi_word = models.CharField(max_length=50)
    english_word = models.CharField(max_length=50, blank=True, null=True)
    definition = models.TextField()

    # Wortart-Feld
    WORD_TYPE_CHOICES = [
        ('noun', 'Nomen'),
        ('verb', 'Verb'),
        ('adjective', 'Adjektiv'),
        ('article', 'Artikel'),
        ('pronoun', 'Pronomen'),
        ('numeral', 'Numerale'),
        ('adverb', 'Adverb'),
        ('preposition', 'Präposition'),
        ('conjunction', 'Konjunktion'),
        ('interjection', 'Interjektion'),
        ('particle', 'Partikel'),
    ]
    word_type = models.CharField(max_length=20, choices=WORD_TYPE_CHOICES, blank=True, null=True)

    # Felder für Adjektive
    comparative = models.CharField(max_length=50, blank=True, null=True)
    superlative = models.CharField(max_length=50, blank=True, null=True)


    # فیلدهای مربوط به افعال
    is_verb = models.BooleanField(default=False)
    simple_past = models.CharField(max_length=50, blank=True, null=True)
    past_participle = models.CharField(max_length=50, blank=True, null=True)
    auxiliary_verb = models.CharField(max_length=50, blank=True, null=True)

    # فیلدهای مربوط به اسم‌ها
    is_noun = models.BooleanField(default=False)
    plural_form = models.CharField(max_length=50, blank=True, null=True)
    genitive_form = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('m', 'Masculine'), ('f', 'Feminine'), ('n', 'Neutral')],
                              blank=True, null=True)


    usage = models.TextField(blank=True, null=True)  # فیلد توضیحاتی


    # سایر فیلدها
    german_example_sentence = models.TextField()
    farsi_example_sentence = models.TextField(blank=True, null=True)
    english_example_sentence = models.TextField(blank=True, null=True)
    synonyms = models.TextField(blank=True, null=True)
    antonyms = models.TextField(blank=True, null=True)

    #Audio
    audio = models.FileField(upload_to='audio/', blank=True, null=True)
    german_example_audio = models.FileField(upload_to='german_example_audio/', blank=True, null=True)
    english_audio = models.FileField(upload_to='english_audio/', blank=True, null=True)
    english_example_audio = models.FileField(upload_to='english_example_audio/', blank=True, null=True)

    #Video
    video = models.FileField(upload_to='videos/', blank=True, null=True)

    def __str__(self):
        return self.german_word

    def save(self, *args, **kwargs):
        print(f"Speichere Word-Instanz: {self.german_word}")

        # Verzeichnisse definieren
        audio_directory = os.path.join(settings.MEDIA_ROOT, 'audio')
        german_example_audio_directory = os.path.join(settings.MEDIA_ROOT, 'german_example_audio')
        english_example_audio_directory = os.path.join(settings.MEDIA_ROOT, 'english_example_audio')
        english_audio_directory = os.path.join(settings.MEDIA_ROOT, 'english_audio')

        # Generiere Audio für das deutsche Wort
        if not self.audio:
            print(f"Generiere deutsches Audio für: {self.german_word}")
            print(f"Verzeichnis: {audio_directory}")
            file_path = generate_audio_file(
                text=self.german_word,
                lang='de',
                directory=audio_directory,
                filename=f"{self.german_word}.mp3"
            )
            if file_path:
                print(f"Audio-Datei erfolgreich erstellt: {file_path}")
                self.audio.name = f"audio/{self.german_word}.mp3"
                print(f"Setze Audio-Pfad im Modell: {self.audio.name}")
            else:
                print(f"Fehler bei der Erstellung der Audio-Datei für: {self.german_word}")

        # Generiere Audio für den deutschen Beispielsatz
        if self.german_example_sentence and not self.german_example_audio:
            print(f"Generiere deutsches Beispielsatz-Audio für: {self.german_example_sentence}")
            filename = f"{self.german_word}_example.mp3".replace(" ", "_")
            file_path = generate_audio_file(
                text=self.german_example_sentence,
                lang='de',
                directory=german_example_audio_directory,
                filename=filename
            )
            if file_path:
                print(f"Beispielsatz-Audio-Datei erfolgreich erstellt: {file_path}")
                self.german_example_audio.name = f"german_example_audio/{filename}"
            else:
                print(f"Fehler bei der Erstellung der Beispielsatz-Audio-Datei für: {self.german_example_sentence}")

        # Generiere Audio für das englische Wort
        if self.english_word and not self.english_audio:
            print(f"Generiere englisches Audio für: {self.english_word}")
            file_path = generate_audio_file(
                text=self.english_word,
                lang='en',
                directory=english_audio_directory,
                filename=f"{self.english_word}.mp3"
            )
            if file_path:
                print(f"Englisches Audio-Datei erfolgreich erstellt: {file_path}")
                self.english_audio.name = f"english_audio/{self.english_word}.mp3"
            else:
                print(f"Fehler bei der Erstellung der englischen Audio-Datei für: {self.english_word}")

        # Generiere Audio für den englischen Beispielsatz
        if self.english_example_sentence and not self.english_example_audio:
            print(f"Generiere englisches Beispielsatz-Audio für: {self.english_example_sentence}")
            file_path = generate_audio_file(
                text=self.english_example_sentence,
                lang='en',
                directory=english_example_audio_directory,
                filename=f"{self.german_word}_english_example.mp3"
            )
            if file_path:
                print(f"Englisches Beispielsatz-Audio-Datei erfolgreich erstellt: {file_path}")
                self.english_example_audio.name = f"english_example_audio/{self.german_word}_english_example.mp3"
            else:
                print(f"Fehler bei der Erstellung der Beispielsatz-Audio-Datei für: {self.english_example_sentence}")

        # Speichere das Modell
        super().save(*args, **kwargs)
        print(f"Modell {self.german_word} wurde erfolgreich gespeichert.")


class Flashcard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # اتصال به کاربر
    word = models.ForeignKey(Word, on_delete=models.CASCADE)  # اتصال به کلمه
    created_at = models.DateTimeField(auto_now_add=True)  # زمان افزودن فلش‌کارت

    def __str__(self):
        return f"{self.user.username} - {self.word.german_word}"