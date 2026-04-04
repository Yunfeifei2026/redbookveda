"""
Inject pretext demo section into all 10 design HTML files.
Each design gets a styled demo that matches its aesthetic.
"""

import re
import os

DESIGNS_DIR = os.path.join(os.path.dirname(__file__), 'designs')

# Per-design theme config
THEMES = {
    'design-01-editorial.html': {
        'bg': '#EAE0CC', 'border': '#A07840', 'header_bg': '#2C1810',
        'header_color': '#F5EFE0', 'accent': '#7A1A2E',
        'canvas_bg': '#F5EFE0', 'canvas_text': '#2C1810',
        'metric_color': '#8B7D70', 'font_family': 'Noto Serif SC',
        'label': '排版引擎 · PRETEXT',
    },
    'design-02-brutalist.html': {
        'bg': '#F5F5F0', 'border': '#0A0A0A', 'header_bg': '#0A0A0A',
        'header_color': '#FFD600', 'accent': '#FF2222',
        'canvas_bg': '#FFFFFF', 'canvas_text': '#0A0A0A',
        'metric_color': '#555', 'font_family': 'Noto Sans SC',
        'label': '⚡ PRETEXT ENGINE',
    },
    'design-03-minimal.html': {
        'bg': '#F5F5F0', 'border': '#E2E2DC', 'header_bg': '#FAFAF6',
        'header_color': '#1A1A18', 'accent': '#1A1A18',
        'canvas_bg': '#FAFAF6', 'canvas_text': '#1A1A18',
        'metric_color': '#8A8A84', 'font_family': 'Noto Serif SC',
        'label': 'pretext · 文字测量引擎',
    },
    'design-04-retro.html': {
        'bg': '#0C0C0A', 'border': '#006622', 'header_bg': '#001A08',
        'header_color': '#FFAA00', 'accent': '#00CC44',
        'canvas_bg': '#050A05', 'canvas_text': '#00CC44',
        'metric_color': '#448844', 'font_family': 'Share Tech Mono',
        'label': '[ PRETEXT ENGINE v0.0.4 ]',
    },
    'design-05-noir.html': {
        'bg': '#0F0F1E', 'border': '#1E1E38', 'header_bg': '#080810',
        'header_color': '#C8902A', 'accent': '#C8902A',
        'canvas_bg': '#0D0D25', 'canvas_text': '#D0D0E0',
        'metric_color': '#5060A0', 'font_family': 'Noto Serif SC',
        'label': 'pretext · 排版引擎',
    },
    'design-06-genz.html': {
        'bg': '#F0F0F8', 'border': '#111118', 'header_bg': '#111118',
        'header_color': '#FFD600', 'accent': '#FF1493',
        'canvas_bg': '#FFFFFF', 'canvas_text': '#111118',
        'metric_color': '#666', 'font_family': 'Noto Sans SC',
        'label': '⚡ pretext 排版黑科技',
    },
    'design-07-traditional.html': {
        'bg': '#EDE0C4', 'border': 'rgba(139,105,20,0.3)', 'header_bg': '#1C1208',
        'header_color': '#F4ECD8', 'accent': '#C0392B',
        'canvas_bg': '#F4ECD8', 'canvas_text': '#1C1208',
        'metric_color': '#7A6040', 'font_family': 'Noto Serif SC',
        'label': '字迹丈量 · 由 pretext 驱动',
    },
    'design-08-futuristic.html': {
        'bg': '#080820', 'border': 'rgba(0,229,255,0.12)', 'header_bg': '#050510',
        'header_color': '#00E5FF', 'accent': '#00E5FF',
        'canvas_bg': '#0D0D28', 'canvas_text': '#00E5FF',
        'metric_color': '#5060A0', 'font_family': 'Noto Sans SC',
        'label': '▶ PRETEXT ENGINE · ACTIVE',
    },
    'design-09-newspaper.html': {
        'bg': '#EAE4C8', 'border': '#1A1714', 'header_bg': '#1A1714',
        'header_color': '#F2EDD7', 'accent': '#8B0000',
        'canvas_bg': '#F2EDD7', 'canvas_text': '#1A1714',
        'metric_color': '#5A5040', 'font_family': 'Noto Serif SC',
        'label': '排版技术 · pretext 引擎',
    },
    'design-10-wildcard.html': {
        'bg': '#FDEFCE', 'border': '#1A120A', 'header_bg': '#E8472A',
        'header_color': '#FDEFCE', 'accent': '#1EBBCA',
        'canvas_bg': '#FDEFCE', 'canvas_text': '#1A120A',
        'metric_color': '#888', 'font_family': 'Noto Sans SC',
        'label': 'PRETEXT · 叠印排版引擎',
    },
}

# The JavaScript logic is the same for all designs
JS_TEMPLATE = r"""
<script type="module">
import {{ prepareWithSegments, layoutWithLines, prepare, layout }} from 'https://esm.sh/@chenglou/pretext';

const FONT = '16px "{font_family}", serif';
const LINE_HEIGHT = 26;
const MAX_WIDTH = 480;

const canvas = document.getElementById('ptx-canvas');
const ctx = canvas ? canvas.getContext('2d') : null;
const input = document.getElementById('ptx-input');
const metricsEl = document.getElementById('ptx-metrics');
const statusEl = document.getElementById('ptx-status');
const canvasTextColor = '{canvas_text}';

function updateStatus(ok) {{
  if (statusEl) statusEl.textContent = ok ? '运行中 ✓' : '加载中…';
  if (statusEl) statusEl.style.color = ok ? '#00CC44' : '#888';
}}

function renderCanvas(text) {{
  if (!ctx || !canvas) return;
  try {{
    const prepared = prepareWithSegments(text, FONT);
    const {{ lines, height }} = layoutWithLines(prepared, MAX_WIDTH, LINE_HEIGHT);
    const canvasH = Math.max(height + 48, 80);
    canvas.width = MAX_WIDTH + 48;
    canvas.height = canvasH;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.font = FONT;
    ctx.fillStyle = canvasTextColor;
    ctx.textBaseline = 'top';
    lines.forEach((line, i) => {{
      ctx.fillText(line.text, 24, 24 + i * LINE_HEIGHT);
    }});
    // Draw line guides (subtle)
    ctx.strokeStyle = 'rgba(128,128,128,0.1)';
    ctx.lineWidth = 1;
    lines.forEach((_, i) => {{
      ctx.beginPath();
      ctx.moveTo(0, 24 + i * LINE_HEIGHT + LINE_HEIGHT);
      ctx.lineTo(canvas.width, 24 + i * LINE_HEIGHT + LINE_HEIGHT);
      ctx.stroke();
    }});
    updateStatus(true);
    return {{ lines: lines.length, height, chars: text.replace(/\s/g,'').length }};
  }} catch(e) {{
    updateStatus(false);
    return null;
  }}
}}

function updateMetrics(text) {{
  if (!metricsEl) return;
  const result = renderCanvas(text);
  if (!result) return;
  metricsEl.innerHTML =
    '<span>字数: <strong>' + result.chars + '</strong></span>' +
    '<span>行数: <strong>' + result.lines + '</strong></span>' +
    '<span>高度: <strong>' + result.height + 'px</strong></span>' +
    '<span style="opacity:0.7;font-size:0.85em">无 DOM reflow</span>';
}}

const sampleText = '在消失之前：致我们正在失去的城市记忆。城市在加速更新，那些承载我们童年与青春的街道、建筑、气味，正以难以感知的速度消逝。';

if (input) {{
  input.value = sampleText;
  input.addEventListener('input', () => updateMetrics(input.value));
}}

// Initial render (wait for fonts)
document.fonts.ready.then(() => {{
  updateMetrics(input ? input.value : sampleText);
}});

// Measure article excerpts and annotate with pretext measurements
const excerptSelectors = [
  '.card-excerpt', '.article-excerpt', '.hero-excerpt',
  '.featured-excerpt', '.body-text', '.col-body',
  '.preview-body', '.cc-excerpt', '.hc-title .cc-title'
];
document.querySelectorAll(excerptSelectors.join(',')).forEach(el => {{
  const text = el.textContent.trim();
  if (!text || text.length < 10) return;
  try {{
    const w = Math.max(el.offsetWidth || 240, 120);
    const p = prepareWithSegments(text, FONT);
    const {{ lines }} = layoutWithLines(p, w, LINE_HEIGHT);
    const badge = document.createElement('span');
    badge.className = 'ptx-badge';
    badge.title = 'pretext 精确测量，无 DOM reflow';
    badge.textContent = lines.length + '行';
    el.style.position = 'relative';
    el.appendChild(badge);
  }} catch(e) {{}}
}});
</script>
"""

# CSS for the demo section (same structure, different colors via template vars)
CSS_TEMPLATE = """
<style>
.ptx-section {{
  background: {bg};
  border-top: 2px solid {border};
  padding: 48px 60px;
  position: relative;
  z-index: 1;
}}
.ptx-header {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: {header_bg};
  color: {header_color};
  padding: 12px 20px;
  margin-bottom: 24px;
  font-family: monospace;
  font-size: 12px;
  letter-spacing: 0.15em;
}}
.ptx-status {{ font-size: 11px; opacity: 0.8; color: #888; }}
.ptx-body {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}}
.ptx-left label {{
  display: block;
  font-size: 10px;
  letter-spacing: 0.2em;
  color: {metric_color};
  margin-bottom: 8px;
}}
#ptx-input {{
  width: 100%;
  background: {canvas_bg};
  border: 1px solid {border};
  color: {canvas_text};
  padding: 12px 14px;
  font-size: 14px;
  line-height: 1.8;
  min-height: 80px;
  resize: vertical;
  outline: none;
  font-family: inherit;
}}
.ptx-metrics {{
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  margin-top: 12px;
  font-family: monospace;
  font-size: 12px;
  color: {metric_color};
}}
.ptx-metrics strong {{ color: {accent}; }}
.ptx-right label {{
  display: block;
  font-size: 10px;
  letter-spacing: 0.2em;
  color: {metric_color};
  margin-bottom: 8px;
}}
.ptx-canvas-wrap {{
  border: 1px solid {border};
  background: {canvas_bg};
  overflow: hidden;
  min-height: 80px;
}}
#ptx-canvas {{ display: block; max-width: 100%; }}
.ptx-footnote {{
  margin-top: 16px;
  font-size: 10px;
  letter-spacing: 0.15em;
  color: {metric_color};
  opacity: 0.6;
  font-family: monospace;
}}
/* Badge on article excerpts */
.ptx-badge {{
  display: inline-block;
  margin-left: 6px;
  background: {accent};
  color: {header_color};
  font-size: 9px;
  padding: 1px 5px;
  letter-spacing: 0.05em;
  vertical-align: middle;
  opacity: 0.75;
  border-radius: 2px;
  font-family: monospace;
  pointer-events: none;
}}
@media (max-width: 700px) {{
  .ptx-section {{ padding: 32px 20px; }}
  .ptx-body {{ grid-template-columns: 1fr; }}
}}
</style>
"""

HTML_TEMPLATE = """
<!-- ═══════════════════════════════════════════════
     PRETEXT ENGINE DEMO
     github.com/chenglou/pretext
═══════════════════════════════════════════════ -->
<section class="ptx-section">
  <div class="ptx-header">
    <span>{label}</span>
    <span id="ptx-status" class="ptx-status">加载中…</span>
  </div>
  <div class="ptx-body">
    <div class="ptx-left">
      <label>输入文字 — 实时排版测量（不触发 DOM reflow）</label>
      <textarea id="ptx-input"></textarea>
      <div id="ptx-metrics" class="ptx-metrics"></div>
    </div>
    <div class="ptx-right">
      <label>Canvas 渲染 — pretext 精确控制每一行</label>
      <div class="ptx-canvas-wrap">
        <canvas id="ptx-canvas"></canvas>
      </div>
    </div>
  </div>
  <div class="ptx-footnote">
    pretext@0.0.4 · github.com/chenglou/pretext ·
    使用 Canvas measureText 精确测量中文排版，零布局偏移，支持汉字 / emoji / 双向文本
  </div>
</section>
"""

def inject(filename, theme):
    filepath = os.path.join(DESIGNS_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Build CSS, HTML section, and JS
    css = CSS_TEMPLATE.format(**theme)
    section = HTML_TEMPLATE.format(label=theme['label'])
    js = JS_TEMPLATE.format(**theme)

    # Insert CSS before </style> that's in <head>, or before </head>
    # Actually insert before </head>
    if '</head>' in html:
        html = html.replace('</head>', css + '</head>', 1)

    # Insert demo section + JS before </body>
    if '</body>' in html:
        html = html.replace('</body>', section + js + '</body>', 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'✓ {filename}')

for filename, theme in THEMES.items():
    inject(filename, theme)

print('\n全部完成！')
