from django.shortcuts import render, redirect, get_object_or_404
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from .models import Word, Flashcard
from .utils import generate_audio_file
import os
from django.conf import settings
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # ورود خودکار کاربر
            return redirect('home')  # هدایت به صفحه اصلی
    else:
        form = RegisterForm()
    return render(request, 'vocabulary/register.html', {'form': form})


def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'vocabulary/logout.html')
    return redirect('home')  # در صورت نیاز به تغییر مسیر پیش فرض


def home(request):
    return render(request, 'vocabulary/search.html')  # نمایش فایل search.html به جای home.html

def word_list(request):
    words = Word.objects.all()  # Alle Wörter aus der Datenbank abrufen

    # Audiodateien für jedes Wort generieren
    for word in words:
        audio_path = os.path.join(settings.MEDIA_ROOT, 'audio', f"{word.german_word}.mp3")
        if not os.path.exists(audio_path):  # Nur generieren, wenn die Datei fehlt
            generate_audio_file(word.german_word)

    return render(request, 'vocabulary/word_list.html', {'words': words})


def search_word(request):
    query = request.GET.get('query')  # دریافت کلمه جستجو شده
    words = None
    flashcard_ids = []  # لیست آی‌دی کلمات در فلش‌کارت کاربر
    message = ""

    if query:  # اگر کاربر چیزی جستجو کرده باشد
        words = Word.objects.filter(german_word__iexact=query)  # جستجو بر اساس کلمه آلمانی
        if not words.exists():
            message = f"Es wurden keine Einträge für das Wort '{query}' gefunden."
        else:
            # بررسی کنید که کدام کلمات در فلش‌کارت کاربر هستند
            if request.user.is_authenticated:  # بررسی لاگین بودن کاربر
                flashcard_ids = Flashcard.objects.filter(user=request.user, word__in=words).values_list('word_id', flat=True)
    else:
        message = "Bitte geben Sie ein Wort zum Suchen ein..."

    return render(request, 'vocabulary/search.html', {
        'words': words,
        'flashcard_ids': list(flashcard_ids),  # ارسال لیست آی‌دی‌های فلش‌کارت
        'message': message,
        'query': query
    })


@login_required
def add_to_flashcards(request):
    if request.method == "POST":
        word_id = request.POST.get("word_id")
        if request.user.is_authenticated and word_id:
            word = Word.objects.get(id=word_id)
            # بررسی کنید که آیا کلمه قبلاً در فلش‌کارت وجود دارد
            flashcard, created = Flashcard.objects.get_or_create(user=request.user, word=word)
            print(f"Flashcard created: {created}, Word: {word.german_word}")

            # بازگشت به صفحه قبلی
            return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('home')  # اگر مشکلی پیش آمد، به صفحه اصلی برگردید

@login_required
def flashcards(request):
    user_flashcards = Flashcard.objects.filter(user=request.user)
    flashcards = [
        {
            "id": fc.id,  # اضافه کردن ID فلش‌کارت برای هر کارت
            "word": {
                "german_word": fc.word.german_word or "",
                "english_word": fc.word.english_word or "",
                "farsi_word": fc.word.farsi_word or "",
            }
        }
        for fc in user_flashcards
    ]
    print(f"Flashcards data for user {request.user}: {flashcards}")  # لاگ گرفتن برای بررسی داده‌ها
    return render(request, 'vocabulary/flashcards.html', {'flashcards': json.dumps(flashcards)})




@login_required
def remove_flashcard(request, flashcard_id):
    if request.method == 'POST':
        flashcard = get_object_or_404(Flashcard, id=flashcard_id, user=request.user)
        flashcard.delete()
        return JsonResponse({"status": "success", "message": "Flashcard removed successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


def grammatik_links(request):
    links = [
        "https://learngerman.dw.com/de/grammar",
        "https://www.deutsch-perfekt.com/#feature-1601538296",
        "https://mein-deutschbuch.de/grammatik.html",
        "https://www.grammatikdeutsch.de/",
        "https://deutsch.lingolia.com/de/grammatik"
    ]
    return render(request, 'vocabulary/links.html', {'title': 'Nützliche Links - Grammatik', 'links': links})


def redewendung_links(request):
    links = ["https://learngerman.dw.com/de/das-sagt-man-so/s-60040484"]
    return render(request, 'vocabulary/links.html', {'title': 'Nützliche Links - Redewendung', 'links': links})


def nomen_verbindung_links(request):
    links = ["https://deutschtraining.org/deutsche-grammatik/substantive/nomen-verb-verbindungen/"]
    return render(request, 'vocabulary/links.html', {'title': 'Nützliche Links - Nomen Verbindung', 'links': links})


def woerterbuch_links(request):
    links = ["https://www.dwds.de/verbindungen",
             "https://www.verbformen.de/"
             ]
    return render(request, 'vocabulary/links.html', {'title': 'Nützliche Links - Wörterbuch', 'links': links})


def video_links(request):
    links = ["https://www.youtube.com/watch?v=abFz6JgOMCk&ab_channel=DeutschlernenmitderDW"]
    return render(request, 'vocabulary/links.html', {'title': 'Nützliche Links - Video', 'links': links})


def podcast_links(request):
    links = ["https://www.easygerman.org/podcast"]
    return render(request, 'vocabulary/links.html', {'title': 'Nützliche Links - Podcast', 'links': links})


def sonstige_links(request):
    links = ["https://www.volkshochschule.de/kurswelt/online-lernen/index.php"]
    return render(request, 'vocabulary/links.html', {'title': 'Nützliche Links - Sonstige', 'links': links})
