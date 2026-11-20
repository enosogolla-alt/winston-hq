"""Generate Winston HQ dark luxury-tech covers, tiles and icons (PNG)."""
import math, os
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets')
os.makedirs(OUT, exist_ok=True)
GOLD, GREEN = '#D9A441', '#3DDC97'

def hexgrid(cx, cy, r, rows, cols, stroke):
    s = []
    for row in range(rows):
        for col in range(cols):
            x = cx + col * r * 1.75 + (row % 2) * r * 0.875
            y = cy + row * r * 1.52
            pts = ' '.join(f"{x + r*math.cos(math.radians(60*k+30)):.1f},{y + r*math.sin(math.radians(60*k+30)):.1f}" for k in range(6))
            op = max(0.08, 1 - (abs(col - cols/2) + abs(row - rows/2)) / (cols*0.7))
            s.append(f'<polygon points="{pts}" fill="none" stroke="{stroke}" stroke-width="1.4" opacity="{op:.2f}"/>')
    return ''.join(s)

def motif(kind, w, h, cx):
    cy = h / 2
    if kind == 'hq':
        rings = ''.join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GOLD}" stroke-width="{1.6 if i%2==0 else 0.8}" opacity="{0.9-i*0.13:.2f}" {"stroke-dasharray=\"4 10\"" if i%2 else ""}/>' for i, r in enumerate([60, 105, 150, 200, 255, 315]))
        ticks = ''.join(f'<line x1="{cx+215*math.cos(math.radians(a))}" y1="{cy+215*math.sin(math.radians(a))}" x2="{cx+235*math.cos(math.radians(a))}" y2="{cy+235*math.sin(math.radians(a))}" stroke="{GOLD}" stroke-width="2" opacity=".6"/>' for a in range(0, 360, 10))
        return rings + ticks + f'<line x1="{cx-360}" y1="{cy}" x2="{cx+360}" y2="{cy}" stroke="{GOLD}" opacity=".25"/><line x1="{cx}" y1="{cy-360}" x2="{cx}" y2="{cy+360}" stroke="{GOLD}" opacity=".25"/><circle cx="{cx+150*math.cos(math.radians(-40))}" cy="{cy+150*math.sin(math.radians(-40))}" r="7" fill="{GREEN}" filter="url(#glow)"/>'
    if kind == 'goal':
        pts, x0 = [], cx - 330
        vals = [0.1, 0.18, 0.15, 0.3, 0.27, 0.42, 0.5, 0.47, 0.66, 0.78, 0.95]
        for i, v in enumerate(vals):
            pts.append((x0 + i * 66, cy + 150 - v * 300))
        path = 'M' + ' L'.join(f'{x:.0f},{y:.0f}' for x, y in pts)
        area = path + f' L{pts[-1][0]:.0f},{cy+170} L{pts[0][0]:.0f},{cy+170} Z'
        grid = ''.join(f'<line x1="{x0}" y1="{cy-150+i*75}" x2="{x0+660}" y2="{cy-150+i*75}" stroke="{GOLD}" opacity=".12"/>' for i in range(5))
        dots = ''.join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3.5" fill="{GOLD}"/>' for x, y in pts)
        tx, ty = pts[-1]
        return grid + f'<path d="{area}" fill="url(#fade)"/><path d="{path}" fill="none" stroke="{GOLD}" stroke-width="3" filter="url(#glow)"/>' + dots + f'<circle cx="{tx}" cy="{ty}" r="22" fill="none" stroke="{GREEN}" stroke-width="2"/><circle cx="{tx}" cy="{ty}" r="40" fill="none" stroke="{GREEN}" stroke-width="1" opacity=".5"/><circle cx="{tx}" cy="{ty}" r="7" fill="{GREEN}" filter="url(#glow)"/>'
    if kind == 'freelance':
        wins = ''
        for i, (dx, dy, ww, hh, op) in enumerate([(-300, -150, 420, 280, .35), (-180, -80, 460, 300, .9), (60, -20, 300, 200, .5)]):
            x, y = cx + dx, cy + dy
            wins += f'<rect x="{x}" y="{y}" width="{ww}" height="{hh}" rx="14" fill="#0E1411" stroke="{GOLD}" stroke-width="1.5" opacity="{op}"/><line x1="{x}" y1="{y+34}" x2="{x+ww}" y2="{y+34}" stroke="{GOLD}" opacity="{op*.6:.2f}"/>'
            wins += ''.join(f'<circle cx="{x+20+k*18}" cy="{y+17}" r="5" fill="{GOLD}" opacity="{op*.7:.2f}"/>' for k in range(3))
        code = ''.join(f'<rect x="{cx-150+(k%3)*24}" y="{cy-25+k*26}" width="{[180,240,120,200,150,90][k]}" height="8" rx="4" fill="{[GOLD,GREEN][k%2]}" opacity=".55"/>' for k in range(6))
        return wins + code + f'<text x="{cx+120}" y="{cy+60}" font-family="DejaVu Sans Mono" font-size="90" fill="{GOLD}" opacity=".9">&lt;/&gt;</text>'
    if kind == 'hive':
        return hexgrid(cx - 330, cy - 230, 48, 7, 9, GOLD) + f'<polyline points="{cx-80},{cy+60} {cx-20},{cy} {cx+20},{cy+30} {cx+90},{cy-50}" fill="none" stroke="{GREEN}" stroke-width="5" stroke-linejoin="round" filter="url(#glow)"/><polygon points="{cx+90},{cy-50} {cx+60},{cy-48} {cx+88},{cy-20}" fill="{GREEN}"/>'
    if kind == 'zoo':
        bars = ''
        for i in range(48):
            a = abs(math.sin(i * 0.37) * math.cos(i * 0.11)) * 200 + 14
            x = cx - 380 + i * 16
            bars += f'<rect x="{x}" y="{cy-a/2}" width="7" height="{a}" rx="3.5" fill="{GOLD if 16<i<32 else GREEN}" opacity="{0.95 if 16<i<32 else 0.35}"/>'
        return bars + f'<circle cx="{cx}" cy="{cy}" r="250" fill="none" stroke="{GOLD}" stroke-width="1" opacity=".18"/>'
    if kind == 'school':
        lines = ''.join(f'<path d="M{cx-320},{cy-200+i*36} Q{cx},{cy-240+i*36} {cx+320},{cy-200+i*36}" fill="none" stroke="{GOLD}" stroke-width="1.2" opacity="{0.08+0.06*i:.2f}"/>' for i in range(12))
        cap = f'<polygon points="{cx},{cy-90} {cx+170},{cy-20} {cx},{cy+50} {cx-170},{cy-20}" fill="#0E1411" stroke="{GOLD}" stroke-width="2.5" filter="url(#glow)"/><path d="M{cx-100},{cy+10} L{cx-100},{cy+85} Q{cx},{cy+135} {cx+100},{cy+85} L{cx+100},{cy+10}" fill="none" stroke="{GOLD}" stroke-width="2.5"/><line x1="{cx+170}" y1="{cy-20}" x2="{cx+170}" y2="{cy+90}" stroke="{GREEN}" stroke-width="3"/><circle cx="{cx+170}" cy="{cy+96}" r="8" fill="{GREEN}" filter="url(#glow)"/>'
        return lines + cap
    if kind == 'personal':
        circ = ''.join(f'<circle cx="{cx+60*math.cos(i)}" cy="{cy+60*math.sin(i)}" r="{170}" fill="none" stroke="{GOLD if i<3 else GREEN}" stroke-width="1.4" opacity=".45"/>' for i in [0, 1.05, 2.1, 3.15, 4.2, 5.25])
        return circ + f'<circle cx="{cx}" cy="{cy}" r="10" fill="{GOLD}" filter="url(#glow)"/>'
    if kind == 'system':
        out = ''
        nodes = [(cx-260, cy-120), (cx-60, cy-170), (cx+170, cy-100), (cx-180, cy+90), (cx+40, cy+40), (cx+250, cy+120)]
        for a in range(len(nodes)):
            for b in range(a+1, len(nodes)):
                if (a+b) % 2:
                    out += f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="{GOLD}" opacity=".25"/>'
        for x, y in nodes:
            out += f'<ellipse cx="{x}" cy="{y-18}" rx="34" ry="11" fill="#0E1411" stroke="{GOLD}" stroke-width="1.6"/><path d="M{x-34},{y-18} L{x-34},{y+18} A34,11 0 0 0 {x+34},{y+18} L{x+34},{y-18}" fill="#0E1411" stroke="{GOLD}" stroke-width="1.6"/>'
        return out
    return ''

def page(w, h, kind, label, title, sub, tile=False):
    cx = w * (0.72 if not tile else 0.62)
    title_size = 92 if not tile else 64
    return f'''<html><body style="margin:0;background:#070A08">
<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
<defs>
<radialGradient id="glowbg" cx="{cx/w:.2f}" cy="0.5" r="0.6"><stop offset="0" stop-color="#2A2210"/><stop offset=".55" stop-color="#0B0F0C"/><stop offset="1" stop-color="#060807"/></radialGradient>
<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GOLD}" stop-opacity=".28"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></linearGradient>
<linearGradient id="vign" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#060807" stop-opacity=".95"/><stop offset=".45" stop-color="#060807" stop-opacity=".25"/><stop offset="1" stop-color="#060807" stop-opacity="0"/></linearGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{GOLD}" stroke-opacity=".05"/></pattern>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .05 0"/></filter>
</defs>
<rect width="{w}" height="{h}" fill="url(#glowbg)"/>
<rect width="{w}" height="{h}" fill="url(#grid)"/>
{motif(kind, w, h, cx)}
<rect width="{w}" height="{h}" fill="url(#vign)"/>
<rect width="{w}" height="{h}" filter="url(#grain)"/>
<g font-family="Inter Display, Inter, sans-serif">
<text x="{64 if not tile else 48}" y="{h/2 - (title_size*0.55 if sub else title_size*0.1)}" font-family="DejaVu Sans Mono" font-size="{20 if not tile else 18}" letter-spacing="6" fill="{GOLD}">{label}</text>
<text x="{60 if not tile else 44}" y="{h/2 + title_size*0.42}" font-size="{title_size}" font-weight="200" letter-spacing="-2" fill="#EFEBDF">{title}</text>
<text x="{64 if not tile else 48}" y="{h/2 + title_size*0.42 + (46 if not tile else 40)}" font-size="{22 if not tile else 20}" font-weight="400" fill="#8E9C92">{sub}</text>
</g>
<rect x="1" y="1" width="{w-2}" height="{h-2}" fill="none" stroke="{GOLD}" stroke-opacity=".12"/>
</svg></body></html>'''

ICON_PATHS = {
    'hq': '<circle cx="32" cy="32" r="20"/><circle cx="32" cy="32" r="9"/><path d="M32 4v10M32 50v10M4 32h10M50 32h10"/>',
    'goal': '<path d="M8 50 L22 36 L32 42 L54 18"/><path d="M42 18h12v12"/>',
    'freelance': '<rect x="6" y="12" width="52" height="38" rx="5"/><path d="M6 22h52M24 32l-6 6 6 6M40 32l6 6-6 6"/>',
    'hive': '<path d="M32 6l20 11.5v23L32 52 12 40.5v-23z"/><path d="M24 36l6-6 4 4 8-8"/>',
    'zoo': '<rect x="24" y="6" width="16" height="30" rx="8"/><path d="M16 30a16 16 0 0 0 32 0M32 46v12M24 58h16"/>',
    'school': '<path d="M32 12l26 12-26 12L6 24z"/><path d="M16 29v13c8 7 24 7 32 0V29M58 24v16"/>',
    'personal': '<path d="M32 56C14 44 8 32 8 22a12 12 0 0 1 24-4 12 12 0 0 1 24 4c0 10-6 22-24 34z"/>',
    'system': '<ellipse cx="32" cy="14" rx="20" ry="7"/><path d="M12 14v36c0 4 9 7 20 7s20-3 20-7V14M12 32c0 4 9 7 20 7s20-3 20-7"/>',
    'idea': '<path d="M22 40a16 16 0 1 1 20 0v8H22z"/><path d="M24 56h16"/>',
    'income': '<rect x="6" y="16" width="52" height="34" rx="5"/><circle cx="32" cy="33" r="8"/><path d="M6 26h6M52 26h6M6 40h6M52 40h6"/>',
}

AREAS = [
    # key, kind, label, title, sub
    ('hq', 'hq', 'COMMAND CENTER', 'Winston HQ', 'Build the million.'),
    ('goal', 'goal', 'KES 1,000,000 · DEC 2027', 'Million Goal', 'Every task moves the number.'),
    ('freelance', 'freelance', 'CLIENT WORK', 'Freelance', 'Ship it. Get paid.'),
    ('hive', 'hive', 'DIGITAL AGENCY', 'HollowComb', 'Systems that grow businesses.'),
    ('zoo', 'zoo', 'PRODUCTION CO.', 'Zoo Unfiltered', 'Kago · Otis · Nia · Ras'),
    ('school', 'school', 'BBIT · STRATHMORE', 'School Hub', 'Exams 2 – 15 Dec'),
    ('personal', 'personal', 'LIFE', 'Personal', 'The engine behind everything.'),
    ('system', 'system', 'ENGINE ROOM', 'Systems', 'Databases behind the dashboards.'),
]

with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome')
    pg = b.new_page()
    for key, kind, label, title, sub in AREAS:
        for name, (w, h, tile) in {'cover': (1800, 600, False), 'tile': (960, 540, True)}.items():
            pg.set_viewport_size({'width': w, 'height': h})
            pg.set_content(page(w, h, kind, label, title, sub, tile))
            pg.wait_for_timeout(150)
            pg.screenshot(path=f'{OUT}/{name}-{key}.png', clip={'x': 0, 'y': 0, 'width': w, 'height': h})
    for key, d in ICON_PATHS.items():
        pg.set_viewport_size({'width': 256, 'height': 256})
        pg.set_content(f'<html><body style="margin:0;background:transparent"><svg width="256" height="256" viewBox="0 0 64 64"><g fill="none" stroke="{GOLD}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">{d}</g></svg></body></html>')
        pg.screenshot(path=f'{OUT}/icon-{key}.png', omit_background=True, clip={'x': 0, 'y': 0, 'width': 256, 'height': 256})
    b.close()
print('done', sorted(os.listdir(OUT)))
