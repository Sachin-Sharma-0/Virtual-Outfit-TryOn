document.addEventListener('DOMContentLoaded', function() {
    const tryOnButtons = document.querySelectorAll('.try-on-button');
    const resultImage = document.getElementById('result-image');

    tryOnButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const outfitImage = this.dataset.outfit;
            resultImage.innerHTML = `<img src="${outfitImage}" alt="Result">`;
        });
    });
});
