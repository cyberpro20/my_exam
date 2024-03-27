function onInputFocus(inputId, labelId, defaultText) {
    var input = document.getElementById(inputId);
    var label = document.getElementById(labelId);
    if (input.value === '') {
        label.style.display = 'none';
    }
    input.addEventListener('input', function() {
        label.style.display = this.value === '' ? 'block' : 'none';
    });
}