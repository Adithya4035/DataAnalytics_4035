document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('sarcasm-form');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const comment = document.getElementById('comment-input').value;
        // Mock API call
        const mockResponse = {
            score: Math.random() * 10,
            comment: "Oh, what an absolutely delightful and original comment. I'm sure no one has ever thought of that before."
        };
        localStorage.setItem('sarcasmAnalysis', JSON.stringify(mockResponse));
        window.location.href = '/result.html';
    });
});
