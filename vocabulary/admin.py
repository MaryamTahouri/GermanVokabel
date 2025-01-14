from django.contrib import admin
from django import forms
from .models import Word


# Dynamisches Formular für Word
class WordAdminForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        word_type = self.instance.word_type

        # فیلدهای مرتبط با هر نوع کلمه
        noun_fields = ['plural_form', 'genitive_form', 'gender']
        verb_fields = ['simple_past', 'past_participle', 'auxiliary_verb']
        adjective_fields = ['comparative', 'superlative']

        # مخفی کردن و غیرفعال کردن فیلدها به صورت پیش‌فرض
        for field in noun_fields + verb_fields + adjective_fields:
            self.fields[field].widget.attrs['style'] = 'display:none;'
            self.fields[field].widget.attrs['disabled'] = 'disabled'

        # فعال‌سازی و نمایش فیلدهای مرتبط بر اساس نوع کلمه
        if word_type == 'noun':
            for field in noun_fields:
                self.fields[field].widget.attrs.pop('style', None)
                self.fields[field].widget.attrs.pop('disabled', None)
        elif word_type == 'verb':
            for field in verb_fields:
                self.fields[field].widget.attrs.pop('style', None)
                self.fields[field].widget.attrs.pop('disabled', None)
        elif word_type == 'adjective':
            for field in adjective_fields:
                self.fields[field].widget.attrs.pop('style', None)
                self.fields[field].widget.attrs.pop('disabled', None)


# Admin-Konfiguration
class WordAdmin(admin.ModelAdmin):
    form = WordAdminForm
    list_display = ('german_word', 'word_type', 'gender', 'comparative', 'superlative')
    list_filter = ('word_type', 'gender')
    search_fields = ('german_word', 'farsi_word', 'english_word', 'synonyms', 'antonyms')
    fieldsets = (
        ('Allgemeine Informationen', {
            'fields': ('german_word', 'farsi_word', 'english_word', 'definition', 'word_type')
        }),
        ('Nomen', {
            'fields': ('plural_form', 'genitive_form', 'gender'),
        }),
        ('Verben', {
            'fields': ('simple_past', 'past_participle', 'auxiliary_verb'),
        }),
        ('Adjektive', {
            'fields': ('comparative', 'superlative', 'synonyms', 'antonyms'),
        }),
        ('Usage', {
            'fields': ('usage',),
        }),

        ('Beispielsätze & Audio', {
            'fields': (
                'german_example_sentence', 'farsi_example_sentence', 'english_example_sentence',
                'audio', 'german_example_audio', 'english_audio', 'english_example_audio','video'
            )
        }),
    )

    # Hinzufügen von JavaScript für dynamisches Anzeigen der Felder
    class Media:
        js = ('vocabulary/admin/js/word_type_dynamic.js',)


admin.site.register(Word, WordAdmin)
