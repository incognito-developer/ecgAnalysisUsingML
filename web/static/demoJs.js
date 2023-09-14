// Get model menu elements
const modelMenu = document.querySelector('.model-menu');
const modelSelect = modelMenu.querySelector('.model-select');
const modelOptions = modelMenu.querySelector('.model-options');

// Get selected image element
const selectedImage = document.querySelector('#selected-image');

// Show/hide model options on hover/click
modelSelect.addEventListener('mouseover', function() {
    modelOptions.style.display = 'block';
});

modelSelect.addEventListener('mouseout', function() {
    modelOptions.style.display = 'none';
});

modelSelect.addEventListener('click', function(e) {
    e.preventDefault();
    modelOptions.style.display = modelOptions.style.display === 'block' ? 'none' : 'block';
});

modelOptions.addEventListener('click', function(e) {
    e.preventDefault();
    const imageSrc = e.target.dataset.image;
    selectedImage.src = imageSrc;
});