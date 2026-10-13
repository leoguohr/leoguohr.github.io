// CPU canvas renderer for the archived mesh arrays. Display transforms only.
class MeshView {
  constructor(canvas, vertices) {
    this.canvas = canvas;
    const low = [Infinity, Infinity, Infinity], high = [-Infinity, -Infinity, -Infinity];
    for (const point of vertices) for (let axis = 0; axis < 3; axis++) {
      low[axis] = Math.min(low[axis], point[axis]); high[axis] = Math.max(high[axis], point[axis]);
    }
    const center = low.map((value, i) => (value + high[i]) / 2);
    const centered = vertices.map(point => point.map((value, i) => value - center[i]));
    const radius = Math.max(...centered.map(point => Math.hypot(...point)), 1e-12);
    this.vertices = centered.map(point => point.map(value => value / radius));
  }
  draw(faces, yaw = .61, pitch = .44, overlays = [], zoom = 1) {
    const canvas = this.canvas, width = canvas.clientWidth, height = canvas.clientHeight;
    if (!width || !height) return;
    const dpr = Math.min(devicePixelRatio || 1, 2);
    canvas.width = width * dpr; canvas.height = height * dpr;
    const ctx = canvas.getContext('2d'); ctx.scale(dpr, dpr);
    const a = Math.cos(yaw), b = Math.sin(yaw), c = Math.cos(pitch), d = Math.sin(pitch);
    const points = this.vertices.map(([x, y, z]) => { const X = a*x-b*y, Y = b*x+a*y; return [X, d*Y+c*z, c*Y-d*z]; });
    const xs = points.map(p => p[0]), ys = points.map(p => p[1]);
    const range = Math.max(Math.max(...xs)-Math.min(...xs), Math.max(...ys)-Math.min(...ys), .1);
    const mx = (Math.max(...xs)+Math.min(...xs))/2, my = (Math.max(...ys)+Math.min(...ys))/2;
    const scale = Math.min(width, height)*.79/range*zoom;
    const xy = points.map(p => [width/2+(p[0]-mx)*scale, height/2-(p[1]-my)*scale]);
    const paint = (triangles, color, alpha) => {
      ctx.globalAlpha = alpha;
      const sorted = triangles.map(face => ({face, depth:face.reduce((sum, i) => sum+points[i][2],0)/3})).sort((x,y) => x.depth-y.depth);
      for (const {face} of sorted) {
        ctx.beginPath(); ctx.moveTo(...xy[face[0]]); ctx.lineTo(...xy[face[1]]); ctx.lineTo(...xy[face[2]]); ctx.closePath();
        if (color) { ctx.fillStyle = color; ctx.strokeStyle = color; ctx.lineWidth = .4; }
        else {
          const q = face.map(i => points[i]), u = q[1].map((v,i) => v-q[0][i]), v = q[2].map((v,i) => v-q[0][i]);
          const n = [u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];
          const shade = .63+.37*Math.abs((n[0]*.25+n[1]*.35+n[2]*.90277)/(Math.hypot(...n)||1));
          ctx.fillStyle = `rgb(${[147,174,160].map(x => Math.round(x*shade)).join(',')})`;
          ctx.strokeStyle = '#719280'; ctx.lineWidth = .14;
        }
        ctx.fill(); ctx.stroke();
      }
    };
    paint(faces, null, overlays.length ? .35 : 1);
    for (const overlay of overlays) paint(overlay.faces, overlay.color, .88);
    ctx.globalAlpha = 1;
  }
}
