<script type="text/javascript">
    function saveTranslation(itemId, languageCode, newTranslationValue) {
        $.ajax({
            type: 'POST',
            url: '{% url "save_translation" %}',  // Update this to your view's URL name
            data: {
                'item_id': itemId,
                'language_code': languageCode,
                'new_translation_value': newTranslationValue,
                'csrfmiddlewaretoken': '{{ csrf_token }}',  // Required for Django CSRF protection
            },
            success: function(response) {
                if (response.success) {
                    alert("Translation saved successfully!");
                    // Update the page with new data as needed
                    $("#translation_" + itemId).text(newTranslationValue);  // Example: update the element
                } else {
                    alert("Failed to save translation.");
                }
            },
            error: function(xhr, status, error) {
                console.error("AJAX error:", status, error);
            }
        });
    }

    // Event handler to trigger the AJAX request
    $(document).on('click', '#save-translation-btn', function () {
        const itemId = $(this).data('item-id');
        const languageCode = $(this).data('language-code');
        const newTranslationValue = $('#translation-input').val();  // Fetch the input value
        saveTranslation(itemId, languageCode, newTranslationValue);
    });
</script>
