const slider = document.getElementById('scene-slider');
slider.addEventListener('input', () => document.getElementById('scene-comparison').style.setProperty('--split', `${slider.value}%`));
