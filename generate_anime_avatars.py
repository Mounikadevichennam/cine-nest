import base64

# Create 6 high-quality vector SVG anime avatar designs

def make_avatar_svg(name, bg_grad, hair_color, skin_color, eyes_color, clothes_color, accessories_type=1):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg_grad[0]}" />
      <stop offset="100%" stop-color="{bg_grad[1]}" />
    </linearGradient>
    <linearGradient id="hairGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{hair_color[0]}" />
      <stop offset="100%" stop-color="{hair_color[1]}" />
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Background Circle -->
  <rect width="200" height="200" rx="40" fill="url(#bgGrad)" />

  <!-- Background Aura Glow -->
  <circle cx="100" cy="100" r="70" fill="#ffffff" opacity="0.08" filter="url(#glow)"/>

  <!-- Neck & Shoulders -->
  <path d="M75 140 L125 140 L130 200 L70 200 Z" fill="{skin_color}" />
  <!-- Clothes / Collar -->
  <path d="M50 160 Q100 135 150 160 L165 200 L35 200 Z" fill="{clothes_color}" />
  <path d="M85 160 L100 185 L115 160" fill="none" stroke="#ffffff" stroke-width="3" opacity="0.6" />

  <!-- Face Base -->
  <path d="M60 70 Q100 145 140 70 Q140 45 100 45 Q60 45 60 70 Z" fill="{skin_color}" />

  <!-- Ears -->
  <ellipse cx="58" cy="95" rx="8" ry="12" fill="{skin_color}" />
  <ellipse cx="142" cy="95" rx="8" ry="12" fill="{skin_color}" />

  <!-- Anime Eyes -->
  <!-- Left Eye -->
  <ellipse cx="80" cy="90" rx="10" ry="14" fill="#ffffff" />
  <ellipse cx="80" cy="90" rx="7" ry="11" fill="{eyes_color}" />
  <circle cx="78" cy="85" r="3" fill="#ffffff" />
  <circle cx="82" cy="94" r="1.5" fill="#ffffff" />
  <path d="M68 76 Q80 72 92 78" fill="none" stroke="#222222" stroke-width="3.5" stroke-linecap="round" />

  <!-- Right Eye -->
  <ellipse cx="120" cy="90" rx="10" ry="14" fill="#ffffff" />
  <ellipse cx="120" cy="90" rx="7" ry="11" fill="{eyes_color}" />
  <circle cx="118" cy="85" r="3" fill="#ffffff" />
  <circle cx="122" cy="94" r="1.5" fill="#ffffff" />
  <path d="M108 78 Q120 72 132 76" fill="none" stroke="#222222" stroke-width="3.5" stroke-linecap="round" />

  <!-- Cute Nose -->
  <circle cx="100" cy="104" r="1.5" fill="#c47d76" />

  <!-- Anime Mouth (Friendly Smile) -->
  <path d="M92 116 Q100 125 108 116" fill="none" stroke="#4a2222" stroke-width="2.5" stroke-linecap="round" />

  <!-- Blush -->
  <ellipse cx="72" cy="104" rx="7" ry="3.5" fill="#ff7b88" opacity="0.4" />
  <ellipse cx="128" cy="104" rx="7" ry="3.5" fill="#ff7b88" opacity="0.4" />

  <!-- Hair Style (Spiky Front / Anime Bangs) -->
  <path d="M55 75 Q40 30 100 20 Q160 30 145 75 Q135 45 100 40 Q65 45 55 75 Z" fill="url(#hairGrad)" />
  <path d="M70 50 Q85 75 90 60 Q100 80 110 58 Q120 75 130 50 Q110 30 70 50 Z" fill="url(#hairGrad)" />

  <!-- Hair Highlights -->
  <path d="M75 35 Q100 25 125 35" fill="none" stroke="#ffffff" stroke-width="2.5" opacity="0.35" stroke-linecap="round" />

  '''

    if accessories_type == 1:
        # Tech Headphones
        svg += '''
  <!-- Headphones -->
  <path d="M48 90 A 55 55 0 0 1 152 90" fill="none" stroke="#333344" stroke-width="7" />
  <rect x="42" y="80" width="14" height="28" rx="6" fill="#00d2ff" stroke="#111" stroke-width="2" />
  <rect x="144" y="80" width="14" height="28" rx="6" fill="#00d2ff" stroke="#111" stroke-width="2" />
  '''
    elif accessories_type == 2:
        # Stylish Glasses
        svg += '''
  <!-- Glasses -->
  <rect x="68" y="80" width="24" height="18" rx="4" fill="none" stroke="#ffd700" stroke-width="2.5" />
  <rect x="108" y="80" width="24" height="18" rx="4" fill="none" stroke="#ffd700" stroke-width="2.5" />
  <line x1="92" y1="88" x2="108" y2="88" stroke="#ffd700" stroke-width="2.5" />
  '''
    elif accessories_type == 3:
        # Star Hair Pin
        svg += '''
  <!-- Hair Clip -->
  <path d="M135 45 L138 52 L145 52 L140 57 L142 64 L135 60 L128 64 L130 57 L125 52 L132 52 Z" fill="#ffd700" />
  '''

    svg += '</svg>'
    b64 = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    return f"data:image/svg+xml;base64,{b64}"

avatars = [
    # Avatar 1: Ren (Cyan Cyberpunk)
    make_avatar_svg("Ren", ["#0f2027", "#2c5364"], ["#00f2fe", "#4facfe"], "#fde2d4", "#00c6ff", "#1f1c2c", accessories_type=1),
    # Avatar 2: Aoi (Indigo Galaxy)
    make_avatar_svg("Aoi", ["#3a1c71", "#d76d77"], ["#7f00ff", "#e100ff"], "#ffe5d9", "#9b51e0", "#2b1055", accessories_type=3),
    # Avatar 3: Kai (Flame Crimson)
    make_avatar_svg("Kai", ["#451254", "#e5405e"], ["#ff416c", "#ff4b2b"], "#fceade", "#ff2a5f", "#3a0007", accessories_type=1),
    # Avatar 4: Hana (Gold Sunshine)
    make_avatar_svg("Hana", ["#283c86", "#45a247"], ["#f7971e", "#ffd200"], "#fff0e6", "#f2994a", "#1e3c72", accessories_type=3),
    # Avatar 5: Yuki (Emerald Sage)
    make_avatar_svg("Yuki", ["#11998e", "#38ef7d"], ["#11998e", "#00b4db"], "#ffe8dc", "#00b4db", "#134e5e", accessories_type=2),
    # Avatar 6: Sora (Violet Night)
    make_avatar_svg("Sora", ["#141e30", "#243b55"], ["#8a2be2", "#4a00e0"], "#fdede2", "#8a2be2", "#0f172a", accessories_type=2),
]

# Kids Avatar
kids_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <rect width="200" height="200" rx="40" fill="url(#kidsBg)" />
  <defs>
    <linearGradient id="kidsBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ff9900" />
      <stop offset="100%" stop-color="#ff5500" />
    </linearGradient>
  </defs>
  <!-- Cat Ears -->
  <path d="M55 60 L40 20 L80 45 Z" fill="#ffffff" />
  <path d="M60 55 L48 28 L75 45 Z" fill="#ffaaaa" />
  <path d="M145 60 L160 20 L120 45 Z" fill="#ffffff" />
  <path d="M140 55 L152 28 L125 45 Z" fill="#ffaaaa" />
  <!-- Cute Chibi Face -->
  <circle cx="100" cy="105" r="55" fill="#ffffff" />
  <!-- Big Chibi Eyes -->
  <circle cx="80" cy="100" r="12" fill="#222" />
  <circle cx="76" cy="95" r="4" fill="#fff" />
  <circle cx="120" cy="100" r="12" fill="#222" />
  <circle cx="116" cy="95" r="4" fill="#fff" />
  <!-- Rosy Cheeks -->
  <circle cx="68" cy="112" r="8" fill="#ff77aa" opacity="0.6" />
  <circle cx="132" cy="112" r="8" fill="#ff77aa" opacity="0.6" />
  <!-- W Mouth -->
  <path d="M92 112 Q96 118 100 112 Q104 118 108 112" fill="none" stroke="#222" stroke-width="3" stroke-linecap="round" />
</svg>'''
kids_avatar = "data:image/svg+xml;base64," + base64.b64encode(kids_svg.encode('utf-8')).decode('utf-8')

# Others Avatar
others_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <rect width="200" height="200" rx="40" fill="url(#othBg)" />
  <defs>
    <linearGradient id="othBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4158D0" />
      <stop offset="50%" stop-color="#C850C0" />
      <stop offset="100%" stop-color="#FFCC70" />
    </linearGradient>
  </defs>
  <circle cx="100" cy="80" r="35" fill="#ffffff" opacity="0.9" />
  <path d="M40 170 Q100 120 160 170 Z" fill="#ffffff" opacity="0.9" />
</svg>'''
others_avatar = "data:image/svg+xml;base64," + base64.b64encode(others_svg.encode('utf-8')).decode('utf-8')

content = f'''// Original Anime-Style Vector Avatars for CineNest OTT
export const ANIME_AVATARS = [
  "{avatars[0]}",
  "{avatars[1]}",
  "{avatars[2]}",
  "{avatars[3]}",
  "{avatars[4]}",
  "{avatars[5]}"
];

export const KIDS_AVATAR = "{kids_avatar}";
export const OTHERS_AVATAR = "{others_avatar}";
'''

import os
os.makedirs('frontend/src/constants', exist_ok=True)
with open('frontend/src/constants/avatars.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Generated frontend/src/constants/avatars.js with 6 unique anime avatars!")
