(function($) {  // استفاده از django.jQuery به جای $
    $(document).ready(function() {
        console.log("جاوااسکریپت بارگذاری و اجرا شد!");

        function toggleFields() {
            var wordType = $('#id_word_type').val(); // گرفتن مقدار انتخاب‌شده از Dropdown
            console.log("نوع کلمه انتخاب‌شده:", wordType);

            // نمایش یا مخفی کردن فیلدها
            $('#id_plural_form, #id_genitive_form, #id_gender, #id_simple_past, #id_past_participle, #id_auxiliary_verb, #id_comparative, #id_superlative')
                .closest('.form-row').hide(); // مخفی کردن همه


            // نمایش فیلدهای مرتبط
            if (wordType === 'noun') {
                console.log("اسم انتخاب شد");
                $('#id_plural_form, #id_genitive_form, #id_gender').closest('.form-row').show();
            } else if (wordType === 'verb') {
                console.log("فعل انتخاب شد");
                $('#id_simple_past, #id_past_participle, #id_auxiliary_verb').closest('.form-row').show();
            } else if (wordType === 'adjective') {
                console.log("صفت انتخاب شد");
                $('#id_comparative, #id_superlative').closest('.form-row').show();
            }
        }

        // Event برای تغییر در Dropdown
        $('#id_word_type').change(toggleFields);
        console.log("alan bayad baz besche****", wordType);
        toggleFields(); // اجرا هنگام بارگذاری صفحه
    });
})(typeof django !== 'undefined' && django.jQuery ? django.jQuery : jQuery);

