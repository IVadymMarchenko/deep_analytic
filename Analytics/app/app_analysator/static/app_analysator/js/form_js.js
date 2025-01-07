document.getElementById("uploadBtn").addEventListener("change", function() {
    // Автоматически отправляем форму при выборе файла
    document.getElementById("uploadForm").submit();
});