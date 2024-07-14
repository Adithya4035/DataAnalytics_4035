document.addEventListener('DOMContentLoaded', () => {
    const resultData = JSON.parse(localStorage.getItem('sarcasmAnalysis'));
    const scoreCircle = document.getElementById('sarcasm-score-circle');
    const scoreText = document.getElementById('sarcasm-score');
    const sarcasmComment = document.getElementById('sarcastic-comment');

    if (resultData) {
        try {
            const score = resultData.score.toFixed(2);
            const scorePercentage = score * 100; // Calculate percentage if needed
            scoreCircle.style.setProperty('--value', scorePercentage); // Set as percentage
            scoreText.textContent = `Sarcasm Score: ${score} / 10`;
            sarcasmComment.textContent = resultData.comment;
        } catch (error) {
            console.error('Error parsing result data:', error);
        }
    } else {
        console.error('No result data found in localStorage.');
    }
});
