function copyUserInfo(button) {
    const userId = button.dataset.userId;
    const secretCode = button.dataset.secretCode;
    const textToCopy = `ID пользователя: ${userId}\nКодовое слово: ${secretCode}`;

    navigator.clipboard.writeText(textToCopy).then(() => {
        const originalText = button.innerText;
        button.innerText = "✅ Скопировано!";
        setTimeout(() => {
            button.innerText = originalText;
        }, 2000);
    }).catch(err => {
        alert("Не удалось скопировать. Попробуйте вручную.");
        console.error('Ошибка копирования:', err);
    });
}