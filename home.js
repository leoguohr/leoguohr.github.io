const slider = document.getElementById('scene-slider');
slider.addEventListener('input', () => document.getElementById('scene-comparison').style.setProperty('--split', `${slider.value}%`));
fetch('assets/nexus-preview.json').then(r => { if (!r.ok) throw new Error('Mesh unavailable'); return r.json(); }).then(mesh => {
  const canvas = document.getElementById('mesh-preview');
  const faces = mesh.faces;
  const view = new MeshView(canvas, mesh.vertices);
  let yaw = .61, pitch = .44, point, touched = false, visible = false, previous = 0;
  const draw = () => view.draw(faces, yaw, pitch);
  new ResizeObserver(draw).observe(canvas);
  new IntersectionObserver(entries => { visible = entries[0].isIntersecting; }).observe(canvas);
  canvas.addEventListener('pointerdown', e => { touched = true; point = [e.clientX,e.clientY]; canvas.setPointerCapture(e.pointerId); });
  canvas.addEventListener('pointermove', e => { if (point) { yaw += (e.clientX-point[0])*.008; pitch += (e.clientY-point[1])*.008; point=[e.clientX,e.clientY]; draw(); } });
  for (const event of ['pointerup','pointercancel']) canvas.addEventListener(event, () => { point = null; });
  canvas.addEventListener('keydown', e => { const move={ArrowLeft:[-.12,0],ArrowRight:[.12,0],ArrowUp:[0,-.12],ArrowDown:[0,.12]}[e.key];if(move){e.preventDefault();touched=true;yaw+=move[0];pitch+=move[1];draw();} });
  draw();
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const animate = time => { if (visible && !document.hidden && !touched && time-previous>70) { yaw+=.008;draw();previous=time; } requestAnimationFrame(animate); };
    requestAnimationFrame(animate);
  }
}).catch(() => {
  const canvas = document.getElementById('mesh-preview'), image = document.createElement('img');
  image.src='assets/nexus-result.webp'; image.alt='Target mesh and actual reconstruction'; canvas.replaceWith(image);
});
