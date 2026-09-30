import base64
import os

def build_svg_girl():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="240" height="240">
  <defs>
    <linearGradient id="g_bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e003a"/>
      <stop offset="50%" stop-color="#3b0764"/>
      <stop offset="100%" stop-color="#0284c7"/>
    </linearGradient>
    <linearGradient id="g_hair" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ec4899"/>
      <stop offset="50%" stop-color="#a855f7"/>
      <stop offset="100%" stop-color="#6366f1"/>
    </linearGradient>
    <linearGradient id="g_eye" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#0369a1"/>
    </linearGradient>
    <linearGradient id="g_jacket" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="50%" stop-color="#1e1b4b"/>
      <stop offset="100%" stop-color="#312e81"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- Background Base -->
  <rect width="240" height="240" rx="48" fill="url(#g_bg)"/>
  <circle cx="120" cy="110" r="85" fill="#38bdf8" opacity="0.1" filter="url(#glow)"/>

  <!-- Neck & Base -->
  <path d="M96 150 L144 150 L150 240 L90 240 Z" fill="#ffe4e6"/>
  <!-- Neck Shadow -->
  <path d="M96 150 Q120 162 144 150 Q130 168 110 168 Z" fill="#fda4af" opacity="0.4"/>

  <!-- Outfit / Cyber Jacket -->
  <path d="M45 190 Q120 160 195 190 L210 240 L30 240 Z" fill="url(#g_jacket)"/>
  <!-- Neon Collar Trims -->
  <path d="M75 190 L105 240 L88 240 L62 192 Z" fill="#ec4899" filter="url(#glow)"/>
  <path d="M165 190 L135 240 L152 240 L178 192 Z" fill="#38bdf8" filter="url(#glow)"/>
  <path d="M120 195 L120 240" stroke="#f43f5e" stroke-width="3" stroke-dasharray="4 2"/>

  <!-- Head Base -->
  <path d="M75 80 Q120 165 165 80 Q165 50 120 50 Q75 50 75 80 Z" fill="#fff1f2"/>

  <!-- Ears -->
  <ellipse cx="72" cy="108" rx="9" ry="14" fill="#fff1f2"/>
  <ellipse cx="168" cy="108" rx="9" ry="14" fill="#fff1f2"/>
  <ellipse cx="72" cy="108" rx="5" ry="8" fill="#fda4af" opacity="0.5"/>
  <ellipse cx="168" cy="108" rx="5" ry="8" fill="#fda4af" opacity="0.5"/>

  <!-- Eyes - Left -->
  <ellipse cx="98" cy="102" rx="12" ry="17" fill="#ffffff"/>
  <ellipse cx="98" cy="103" rx="9" ry="14" fill="url(#g_eye)"/>
  <circle cx="95" cy="96" r="4" fill="#ffffff"/>
  <circle cx="102" cy="109" r="2" fill="#ffffff"/>
  <path d="M83 87 Q98 81 113 88" fill="none" stroke="#0f172a" stroke-width="4.5" stroke-linecap="round"/>
  <path d="M110 85 L116 80" stroke="#0f172a" stroke-width="3" stroke-linecap="round"/>

  <!-- Eyes - Right -->
  <ellipse cx="142" cy="102" rx="12" ry="17" fill="#ffffff"/>
  <ellipse cx="142" cy="103" rx="9" ry="14" fill="url(#g_eye)"/>
  <circle cx="139" cy="96" r="4" fill="#ffffff"/>
  <circle cx="146" cy="109" r="2" fill="#ffffff"/>
  <path d="M127 88 Q142 81 157 87" fill="none" stroke="#0f172a" stroke-width="4.5" stroke-linecap="round"/>
  <path d="M127 85 L121 80" stroke="#0f172a" stroke-width="3" stroke-linecap="round"/>

  <!-- Eyebrows -->
  <path d="M85 76 Q98 70 110 76" fill="none" stroke="#ec4899" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M130 76 Q142 70 155 76" fill="none" stroke="#ec4899" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Blush -->
  <ellipse cx="88" cy="118" rx="10" ry="5" fill="#fb7185" opacity="0.45"/>
  <ellipse cx="152" cy="118" rx="10" ry="5" fill="#fb7185" opacity="0.45"/>

  <!-- Nose & Smile -->
  <circle cx="120" cy="116" r="1.5" fill="#e11d48"/>
  <path d="M110 128 Q120 138 130 128" fill="none" stroke="#881337" stroke-width="3" stroke-linecap="round"/>

  <!-- Hair Base (Back & Front Bangs) -->
  <path d="M60 90 Q30 30 120 20 Q210 30 180 90 Q170 140 185 180 Q160 170 165 120 Q120 30 75 120 Q80 170 55 180 Q70 140 60 90 Z" fill="url(#g_hair)"/>
  <!-- Front Bangs Detail -->
  <path d="M80 65 Q95 95 105 75 Q120 105 135 75 Q145 95 160 65 Q135 35 80 65 Z" fill="url(#g_hair)"/>

  <!-- Hair Shine Strand -->
  <path d="M90 42 Q120 32 150 42" fill="none" stroke="#ffffff" stroke-width="3.5" opacity="0.5" stroke-linecap="round"/>

  <!-- Sleek Headset Accessory -->
  <path d="M60 100 A 65 65 0 0 1 180 100" fill="none" stroke="#0284c7" stroke-width="6" filter="url(#glow)"/>
  <rect x="52" y="92" width="16" height="30" rx="7" fill="#38bdf8" stroke="#0f172a" stroke-width="2.5"/>
  <rect x="172" y="92" width="16" height="30" rx="7" fill="#ec4899" stroke="#0f172a" stroke-width="2.5"/>
  <circle cx="60" cy="107" r="4" fill="#ffffff"/>
  <circle cx="180" cy="107" r="4" fill="#ffffff"/>
</svg>'''
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode('utf-8')).decode('utf-8')

def build_svg_boy():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="240" height="240">
  <defs>
    <linearGradient id="b_bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090d16"/>
      <stop offset="50%" stop-color="#1e1b4b"/>
      <stop offset="100%" stop-color="#0284c7"/>
    </linearGradient>
    <linearGradient id="b_hair" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0284c7"/>
      <stop offset="50%" stop-color="#06b6d4"/>
      <stop offset="100%" stop-color="#3b82f6"/>
    </linearGradient>
    <linearGradient id="b_eye" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#c084fc"/>
      <stop offset="100%" stop-color="#7e22ce"/>
    </linearGradient>
    <linearGradient id="b_hoodie" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#311042"/>
      <stop offset="50%" stop-color="#581c87"/>
      <stop offset="100%" stop-color="#1e1b4b"/>
    </linearGradient>
    <filter id="b_glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- Background Base -->
  <rect width="240" height="240" rx="48" fill="url(#b_bg)"/>
  <circle cx="120" cy="110" r="85" fill="#a855f7" opacity="0.12" filter="url(#b_glow)"/>

  <!-- Neck & Base -->
  <path d="M96 148 L144 148 L150 240 L90 240 Z" fill="#ffedd5"/>
  <path d="M96 148 Q120 160 144 148 Q130 165 110 165 Z" fill="#fed7aa" opacity="0.5"/>

  <!-- Hoodie / Techwear -->
  <path d="M40 185 Q120 155 200 185 L215 240 L25 240 Z" fill="url(#b_hoodie)"/>
  <!-- High Collar / Inner Lining -->
  <path d="M70 185 Q120 168 170 185 L180 240 L60 240 Z" fill="#0f172a"/>
  <!-- Glowing Neon Stripes -->
  <path d="M80 185 L95 240" stroke="#06b6d4" stroke-width="4" stroke-linecap="round" filter="url(#b_glow)"/>
  <path d="M160 185 L145 240" stroke="#a855f7" stroke-width="4" stroke-linecap="round" filter="url(#b_glow)"/>
  <!-- Hoodie Drawstrings -->
  <circle cx="108" cy="205" r="3" fill="#38bdf8"/>
  <circle cx="132" cy="205" r="3" fill="#38bdf8"/>
  <line x1="108" y1="185" x2="108" y2="205" stroke="#38bdf8" stroke-width="2"/>
  <line x1="132" y1="185" x2="132" y2="205" stroke="#38bdf8" stroke-width="2"/>

  <!-- Head Base -->
  <path d="M76 80 Q120 162 164 80 Q164 48 120 48 Q76 48 76 80 Z" fill="#fff7ed"/>

  <!-- Ears -->
  <ellipse cx="73" cy="106" rx="9" ry="14" fill="#fff7ed"/>
  <ellipse cx="167" cy="106" rx="9" ry="14" fill="#fff7ed"/>

  <!-- Eyes - Left -->
  <ellipse cx="98" cy="100" rx="11" ry="16" fill="#ffffff"/>
  <ellipse cx="98" cy="101" rx="8" ry="13" fill="url(#b_eye)"/>
  <circle cx="95" cy="94" r="3.5" fill="#ffffff"/>
  <circle cx="101" cy="107" r="1.8" fill="#ffffff"/>
  <path d="M84 86 Q98 80 112 87" fill="none" stroke="#0f172a" stroke-width="4.5" stroke-linecap="round"/>

  <!-- Eyes - Right -->
  <ellipse cx="142" cy="100" rx="11" ry="16" fill="#ffffff"/>
  <ellipse cx="142" cy="101" rx="8" ry="13" fill="url(#b_eye)"/>
  <circle cx="139" cy="94" r="3.5" fill="#ffffff"/>
  <circle cx="145" cy="107" r="1.8" fill="#ffffff"/>
  <path d="M128 87 Q142 80 156 86" fill="none" stroke="#0f172a" stroke-width="4.5" stroke-linecap="round"/>

  <!-- Eyebrows -->
  <path d="M84 74 Q98 67 112 75" fill="none" stroke="#0284c7" stroke-width="3" stroke-linecap="round"/>
  <path d="M128 75 Q142 67 156 74" fill="none" stroke="#0284c7" stroke-width="3" stroke-linecap="round"/>

  <!-- Nose & Confident Smile -->
  <circle cx="120" cy="114" r="1.5" fill="#ea580c"/>
  <path d="M108 125 Q120 134 132 125" fill="none" stroke="#7c2d12" stroke-width="3" stroke-linecap="round"/>

  <!-- Spiky Anime Hair -->
  <!-- Layer 1 Back Spikes -->
  <path d="M55 75 L38 45 L70 55 L65 25 L95 40 L120 15 L145 40 L175 25 L170 55 L202 45 L185 75 Z" fill="#1e1b4b"/>
  <!-- Layer 2 Main Spikes -->
  <path d="M60 75 Q40 25 120 18 Q200 25 180 75 Q165 40 120 35 Q75 40 60 75 Z" fill="url(#b_hair)"/>
  <!-- Layer 3 Bangs -->
  <path d="M75 55 L90 88 L105 60 L120 95 L135 60 L150 88 L165 55 Q120 35 75 55 Z" fill="url(#b_hair)"/>

  <!-- Hair Highlight Strand -->
  <path d="M85 38 Q120 26 155 38" fill="none" stroke="#ffffff" stroke-width="3" opacity="0.5" stroke-linecap="round"/>
</svg>'''
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode('utf-8')).decode('utf-8')

def build_svg_kid():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="240" height="240">
  <defs>
    <linearGradient id="k_bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4c0519"/>
      <stop offset="50%" stop-color="#881337"/>
      <stop offset="100%" stop-color="#f43f5e"/>
    </linearGradient>
    <linearGradient id="k_hair" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fbbf24"/>
      <stop offset="50%" stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#ea580c"/>
    </linearGradient>
    <linearGradient id="k_eye" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#10b981"/>
      <stop offset="100%" stop-color="#047857"/>
    </linearGradient>
    <linearGradient id="k_outfit" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0284c7"/>
      <stop offset="50%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#facc15"/>
    </linearGradient>
    <filter id="k_glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- Background Base -->
  <rect width="240" height="240" rx="48" fill="url(#k_bg)"/>
  <circle cx="120" cy="110" r="85" fill="#facc15" opacity="0.15" filter="url(#k_glow)"/>

  <!-- Cat-Ear Headband (Behind Hair) -->
  <path d="M68 62 L48 20 L92 48 Z" fill="#f43f5e" stroke="#0f172a" stroke-width="2.5"/>
  <path d="M72 58 L56 26 L90 48 Z" fill="#fda4af"/>
  <path d="M172 62 L192 20 L148 48 Z" fill="#f43f5e" stroke="#0f172a" stroke-width="2.5"/>
  <path d="M168 58 L184 26 L150 48 Z" fill="#fda4af"/>

  <!-- Neck & Base -->
  <path d="M100 152 L140 152 L145 240 L95 240 Z" fill="#fff1f2"/>

  <!-- Cute Kid Outfit -->
  <path d="M48 190 Q120 162 192 190 L205 240 L35 240 Z" fill="url(#k_outfit)"/>
  <!-- Star Emblem on Hoodie -->
  <path d="M120 192 L123 200 L131 200 L125 205 L127 213 L120 208 L113 213 L115 205 L109 200 L117 200 Z" fill="#ffffff" filter="url(#k_glow)"/>

  <!-- Chibi Rounded Head Base -->
  <path d="M70 82 Q120 170 170 82 Q170 48 120 48 Q70 48 70 82 Z" fill="#fff1f2"/>

  <!-- Ears -->
  <ellipse cx="68" cy="108" rx="8" ry="12" fill="#fff1f2"/>
  <ellipse cx="172" cy="108" rx="8" ry="12" fill="#fff1f2"/>

  <!-- Big Chibi Eyes - Left -->
  <ellipse cx="98" cy="102" rx="13" ry="18" fill="#ffffff"/>
  <ellipse cx="98" cy="103" rx="10" ry="15" fill="url(#k_eye)"/>
  <circle cx="94" cy="95" r="4.5" fill="#ffffff"/>
  <circle cx="102" cy="110" r="2.2" fill="#ffffff"/>
  <path d="M82 86 Q98 78 114 87" fill="none" stroke="#0f172a" stroke-width="5" stroke-linecap="round"/>

  <!-- Big Chibi Eyes - Right -->
  <ellipse cx="142" cy="102" rx="13" ry="18" fill="#ffffff"/>
  <ellipse cx="142" cy="103" rx="10" ry="15" fill="url(#k_eye)"/>
  <circle cx="138" cy="95" r="4.5" fill="#ffffff"/>
  <circle cx="146" cy="110" r="2.2" fill="#ffffff"/>
  <path d="M126 87 Q142 78 158 86" fill="none" stroke="#0f172a" stroke-width="5" stroke-linecap="round"/>

  <!-- Cute Rosy Cheeks -->
  <ellipse cx="85" cy="118" rx="11" ry="6" fill="#f43f5e" opacity="0.5"/>
  <ellipse cx="155" cy="118" rx="11" ry="6" fill="#f43f5e" opacity="0.5"/>

  <!-- Tiny Nose & Joyful Open Smile -->
  <circle cx="120" cy="114" r="1.5" fill="#be123c"/>
  <path d="M108 126 Q120 142 132 126 Z" fill="#9f1239"/>
  <path d="M112 133 Q120 140 128 133" fill="#fb7185"/>

  <!-- Fluffy Kid Hair Bangs -->
  <path d="M65 75 Q40 25 120 20 Q200 25 175 75 Q160 45 120 40 Q80 45 65 75 Z" fill="url(#k_hair)"/>
  <path d="M78 60 Q92 90 102 70 Q120 100 138 70 Q148 90 162 60 Q135 35 78 60 Z" fill="url(#k_hair)"/>

  <!-- Hair Shine Strand -->
  <path d="M90 40 Q120 28 150 40" fill="none" stroke="#ffffff" stroke-width="3.5" opacity="0.6" stroke-linecap="round"/>
</svg>'''
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode('utf-8')).decode('utf-8')

def main():
    girl_avatar = build_svg_girl()
    boy_avatar = build_svg_boy()
    kid_avatar = build_svg_kid()

    # Others profile avatar for returning WhoIsWatching screen
    others_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="240" height="240">
  <rect width="240" height="240" rx="48" fill="url(#othBg)" />
  <defs>
    <linearGradient id="othBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4158D0" />
      <stop offset="50%" stop-color="#C850C0" />
      <stop offset="100%" stop-color="#FFCC70" />
    </linearGradient>
  </defs>
  <circle cx="120" cy="95" r="42" fill="#ffffff" opacity="0.9" />
  <path d="M50 205 Q120 145 190 205 Z" fill="#ffffff" opacity="0.9" />
</svg>'''
    others_avatar = "data:image/svg+xml;base64," + base64.b64encode(others_svg.encode('utf-8')).decode('utf-8')

    content = f'''// EXACTLY 3 Premium Original Anime-Style Vector Avatars for CineNest OTT
export const ANIME_AVATARS = [
  "{girl_avatar}", // 1. ANIME GIRL
  "{boy_avatar}",  // 2. ANIME BOY
  "{kid_avatar}"   // 3. ANIME KID
];

export const KIDS_AVATAR = "{kid_avatar}";
export const OTHERS_AVATAR = "{others_avatar}";
'''

    os.makedirs('frontend/src/constants', exist_ok=True)
    with open('frontend/src/constants/avatars.js', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Successfully generated EXACTLY 3 premium anime avatars in frontend/src/constants/avatars.js!")

if __name__ == "__main__":
    main()
