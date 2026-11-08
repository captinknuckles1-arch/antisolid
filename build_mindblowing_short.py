#!/usr/bin/env python3
import os
import math
import random
import asyncio
import subprocess
from PIL import Image, ImageDraw, ImageFont
import edge_tts

VOICE = "en-US-BrianNeural"
FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"

def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()

# The Viral Script: Plain English + Real 2026 Factual Stats
SCRIPT_SEGMENTS = [
    (0.0, 5.5, "Right now in Texas, AI data centers are demanding 474 GIGAWATTS of power—enough to run New York City forty times over."),
    (5.5, 12.0, "Here is the terrifying secret: companies are plugging reckless AI brains straight into 1980s power grids and city trains."),
    (12.0, 19.0, "AI is a guesser. Hardware needs exact math. When AI guesses wrong by 0.1 percent, breakers trip, costing $15,000 EVERY MINUTE."),
    (19.0, 25.0, "Worse? Under the new 2026 Texas TRAIGA law, one unverified AI failure can hit a company with a $200,000 state fine."),
    (25.0, 33.0, "Enter SOLID INTEGRATIONS. We build the Digital Bouncer—Solid OS—that intercepts every AI command in 1.2 milliseconds."),
    (33.0, 41.0, "Bad AI guesses get vaporized. Grid power locks at 60 Hertz with Solid Zero. See the future at solid-integrations.polsia.io.")
]

FULL_SCRIPT = " ".join([seg[2] for seg in SCRIPT_SEGMENTS])

async def make_audio(path):
    print("[1/4] Synthesizing high-energy documentary narration...")
    comm = edge_tts.Communicate(FULL_SCRIPT, VOICE, rate="+13%", pitch="-2Hz")
    await comm.save(path)

def draw_character_glitch(draw, cx, cy, t, panic=False):
    """Draws 'GLITCH' - the chaotic AI character with animated expressions"""
    bounce = math.sin(t * 14) * (18 if panic else 8)
    y = cy + bounce
    color = "#ef4444" if panic else "#a855f7"
    
    # Hover thrusters flame
    flame_h = 30 + int(abs(math.sin(t * 25)) * 35)
    draw.polygon([(cx-30, y+110), (cx+30, y+110), (cx, y+110+flame_h)], fill="#f97316")
    
    # Body & Head
    draw.rounded_rectangle([(cx-75, y+20), (cx+75, y+115)], radius=20, fill="#1e1b4b", outline=color, width=5)
    draw.rounded_rectangle([(cx-95, y-110), (cx+95, y+10)], radius=30, fill="#0f172a", outline=color, width=6)
    
    # Antenna
    ant_x = cx + math.sin(t * 20) * 20
    draw.line([(cx, y-110), (ant_x, y-155)], fill=color, width=6)
    draw.ellipse([(ant_x-12, y-167), (ant_x+12, y-143)], fill="#facc15")
    
    # Expressive Eyes
    if panic:
        # Wide panicked mismatched eyes
        r1 = 28 + int(math.sin(t*30)*5)
        r2 = 20 - int(math.sin(t*30)*5)
        draw.ellipse([(cx-65, y-80), (cx-65+r1*2, y-80+r1*2)], fill="#ef4444", outline="#ffffff", width=3)
        draw.ellipse([(cx+15, y-75), (cx+15+r2*2, y-75+r2*2)], fill="#facc15", outline="#ffffff", width=3)
        # Screaming mouth
        draw.rounded_rectangle([(cx-40, y-25), (cx+40, y-5)], radius=8, fill="#ef4444")
    else:
        # Cocky glowing cyan/purple eyes
        draw.ellipse([(cx-60, y-75), (cx-15, y-30)], fill="#38bdf8")
        draw.ellipse([(cx+15, y-75), (cx+60, y-30)], fill="#38bdf8")
        draw.arc([(cx-40, y-35), (cx+40, y-5)], start=0, end=180, fill="#38bdf8", width=5)

    draw.text((cx-65, y+135), "AI AGENT ('GLITCH')", fill="#ffffff", font=get_font(22))

def draw_character_guardian(draw, cx, cy, t):
    """Draws 'SOLID OS GUARDIAN' - the armored deterministic bouncer with glowing shield"""
    hover = math.sin(t * 4) * 6
    y = cy + hover
    
    # Armored Shoulders & Torso
    draw.polygon([(cx-130, y-20), (cx+130, y-20), (cx+90, y+140), (cx-90, y+140)], fill="#0f172a", outline="#38bdf8", width=6)
    # Glowing Core Reactor
    core_r = 28 + int(math.sin(t * 10) * 4)
    draw.ellipse([(cx-core_r, y+35-core_r), (cx+core_r, y+35+core_r)], fill="#38bdf8", outline="#ffffff", width=4)
    
    # Helmet & Visor
    draw.rounded_rectangle([(cx-70, y-135), (cx+70, y-25)], radius=22, fill="#1e293b", outline="#38bdf8", width=6)
    draw.polygon([(cx-50, y-95), (cx+50, y-95), (cx+35, y-65), (cx-35, y-65)], fill="#facc15")
    
    # Giant Holographic Hex Shield on Left Side
    sx = cx - 175
    pulse = int(abs(math.sin(t * 12)) * 12)
    draw.rounded_rectangle([(sx-25-pulse, y-170), (sx+25+pulse, y+170)], radius=25, fill="#0284c7", outline="#38bdf8", width=6)
    draw.line([(sx, y-150), (sx, y+150)], fill="#ffffff", width=4)
    draw.text((cx-105, y+155), "SOLID OS BOUNCER", fill="#38bdf8", font=get_font(24))

def draw_captions(draw, t):
    """Draws big viral TikTok-style word chunk captions in the lower third"""
    active_text = ""
    for start, end, txt in SCRIPT_SEGMENTS:
        if start <= t <= end:
            words = txt.split()
            progress = (t - start) / (end - start)
            idx = min(len(words) - 1, int(progress * len(words)))
            # Show 4-word chunks
            chunk_start = (idx // 4) * 4
            active_text = " ".join(words[chunk_start:chunk_start+4]).upper()
            break

    if active_text:
        draw.rounded_rectangle([(60, 1460), (1020, 1610)], radius=24, fill="#000000", outline="#facc15", width=5)
        f = get_font(44)
        bbox = draw.textbbox((0, 0), active_text, font=f)
        tw = bbox[2] - bbox[0]
        draw.text(((1080 - tw) / 2, 1510), active_text, fill="#facc15", font=f)

def render_scene_frame(t, duration):
    img = Image.new("RGB", (1080, 1920), color="#050811")
    draw = ImageDraw.Draw(img)

    # Animated Perspective Cyber Grid
    offset = int((t * 120) % 80)
    for y in range(160 + offset, 1440, 80):
        draw.line([(0, y), (1080, y)], fill="#0f172a", width=2)
    for x in range(0, 1080, 90):
        draw.line([(x, 160), (x, 1440)], fill="#0f172a", width=2)

    # Top Live News / Telemetry Ticker
    draw.rectangle([(0, 0), (1080, 150)], fill="#090d16")
    draw.line([(0, 150), (1080, 150)], fill="#38bdf8", width=4)
    draw.text((60, 45), "2026 INFRASTRUCTURE REPORT // SOLID INTEGRATIONS", fill="#38bdf8", font=get_font(30))
    draw.text((60, 90), "SOURCES: ERCOT (474 GW) | TEXAS TRAIGA HB 149 | GARTNER", fill="#94a3b8", font=get_font(22))

    # --- SCENE 1 (0 - 5.5s): 474 GW ERCOT DATA CENTER SURGE ---
    if t < 5.5:
        p = min(1.0, t / 4.5)
        gw = int(p * 474)
        draw.text((80, 210), "TEXAS AI POWER DEMAND SURGE", fill="#facc15", font=get_font(46))
        draw.text((80, 270), "ERCOT 2026 Interconnection Queue (87% AI Data Centers)", fill="#cbd5e1", font=get_font(26))

        # Animated Rising Bar Chart
        bars = [("2022", 65, "#334155"), ("2024", 150, "#0284c7"), ("2026 AI SURGE", gw, "#ef4444")]
        for i, (label, val, col) in enumerate(bars):
            bx = 140 + i * 290
            bh = int((val / 500.0) * 650)
            by = 1150 - bh
            draw.rounded_rectangle([(bx, by), (bx+200, 1150)], radius=16, fill=col, outline="#ffffff", width=3)
            draw.text((bx+25, by-60), f"{val} GW", fill="#ffffff", font=get_font(42))
            draw.text((bx+10, 1175), label, fill="#94a3b8", font=get_font(26))

        draw.rounded_rectangle([(80, 1260), (1000, 1410)], radius=18, fill="#1e1b4b", outline="#38bdf8", width=3)
        draw.text((120, 1315), "FACT: 474 GW = 40x the entire peak load of New York City", fill="#38bdf8", font=get_font(30))

    # --- SCENE 2 (5.5 - 12.0s): MEET 'GLITCH' PLUGGING INTO 1980s GRID ---
    elif t < 12.0:
        draw.text((80, 210), "THE RECKLESS SHORTCUT", fill="#a855f7", font=get_font(48))
        draw.text((80, 270), "Plugging a 'Guessing' AI Brain into 1980s Grid Hardware", fill="#cbd5e1", font=get_font(26))

        draw_character_glitch(draw, 260, 750, t, panic=False)

        # 1980s Substation Box on Right
        draw.rounded_rectangle([(680, 620), (980, 920)], radius=20, fill="#1e293b", outline="#94a3b8", width=5)
        draw.text((715, 720), "1983 SCADA", fill="#ffffff", font=get_font(38))
        draw.text((715, 775), "POWER RELAY", fill="#facc15", font=get_font(32))

        # Animated erratic packets flying from Glitch to Relay
        for i in range(4):
            prog = ((t * 1.8) + i * 0.25) % 1.0
            px = 360 + int(prog * 320)
            py = 760 + int(math.sin(t * 15 + i * 2) * 55)
            draw.ellipse([(px-16, py-16), (px+16, py+16)], fill="#a855f7", outline="#ffffff", width=3)

        draw.rounded_rectangle([(80, 1180), (1000, 1380)], radius=18, fill="#0f172a", outline="#a855f7", width=3)
        draw.text((120, 1230), "AI = Probabilistic (Makes educated guesses)", fill="#e9d5ff", font=get_font(32))
        draw.text((120, 1295), "POWER GRID = Deterministic (Needs 100% exact math)", fill="#38bdf8", font=get_font(32))

    # --- SCENE 3 (12.0 - 19.0s): THE 0.1% CRASH & $15,000/MIN LOSS ---
    elif t < 19.0:
        # Flashing Red Siren Strobe
        if int(t * 8) % 2 == 0:
            draw.rectangle([(0, 150), (1080, 1440)], fill="#2a0606")

        draw.text((80, 210), "WHEN AI HALLUCINATES BY 0.1%", fill="#ef4444", font=get_font(48))
        draw.text((80, 270), "Physical breakers trip & entire systems lock down", fill="#fca5a5", font=get_font(28))

        draw_character_glitch(draw, 540, 680, t, panic=True)

        # Exploding Red Sparks
        random.seed(int(t * 30))
        for _ in range(18):
            sx = random.randint(120, 960)
            sy = random.randint(420, 950)
            draw.ellipse([(sx-8, sy-8), (sx+8, sy+8)], fill="#facc15")

        # Live Ticking Money Burn Counter
        loss = int(((t - 12.0) / 7.0) * 105000)
        draw.rounded_rectangle([(80, 1020), (1000, 1380)], radius=24, fill="#450a0a", outline="#ef4444", width=6)
        draw.text((140, 1065), "ENTERPRISE DOWNTIME COST ($15,000/MIN):", fill="#fca5a5", font=get_font(30))
        draw.text((220, 1140), f"-${loss:,}", fill="#ef4444", font=get_font(90))
        draw.text((180, 1280), "GRID FREQUENCY: 59.71 Hz [CRITICAL BLACKOUT]", fill="#ffffff", font=get_font(30))

    # --- SCENE 4 (19.0 - 25.0s): 2026 TEXAS TRAIGA LAW ($200K FINE) ---
    elif t < 25.0:
        draw.text((80, 210), "2026 REGULATORY HAMMER", fill="#facc15", font=get_font(48))
        draw.text((80, 270), "Texas Responsible AI Governance Act (HB 149 / TRAIGA)", fill="#cbd5e1", font=get_font(26))

        # Giant Legal Penalty Stamp Card
        draw.rounded_rectangle([(100, 420), (980, 940)], radius=25, fill="#18181b", outline="#facc15", width=5)
        draw.text((160, 480), "STATE OF TEXAS // HB 149 ENFORCEMENT", fill="#facc15", font=get_font(32))
        draw.text((160, 560), "UP TO $200,000", fill="#ef4444", font=get_font(78))
        draw.text((160, 670), "FINE PER UNVERIFIED AI VIOLATION", fill="#ffffff", font=get_font(38))
        draw.text((160, 760), "• Effective January 1, 2026 across Texas", fill="#94a3b8", font=get_font(28))
        draw.text((160, 815), "• Requires NIST Safe-Harbor Audit Proof", fill="#38bdf8", font=get_font(28))

        draw_character_glitch(draw, 540, 1180, t, panic=True)

    # --- SCENE 5 (25.0 - 33.0s): SOLID OS 'THE DIGITAL BOUNCER' ARRIVES ---
    elif t < 33.0:
        draw.text((80, 210), "THE FIX: SOLID INTEGRATIONS", fill="#38bdf8", font=get_font(48))
        draw.text((80, 270), "Solid OS: The 1.2ms Deterministic Logic Bouncer", fill="#cbd5e1", font=get_font(28))

        # Glitch on Left shooting red chaos bolts
        draw_character_glitch(draw, 210, 740, t, panic=False)
        
        # Solid OS Guardian in Center-Right with Shield blocking bolts
        draw_character_guardian(draw, 740, 740, t)

        # Red bolt hitting shield at x=565 and turning into clean green wave
        bx = 310 + int(((t * 3.0) % 1.0) * 240)
        draw.ellipse([(bx-18, 720), (bx+18, 756)], fill="#ef4444", outline="#ffffff", width=3)
        draw.text((340, 660), "HALLUCINATION BLOCKED!", fill="#facc15", font=get_font(26))

        # Feature Breakdown Box
        draw.rounded_rectangle([(80, 1080), (1000, 1400)], radius=20, fill="#0f172a", outline="#38bdf8", width=4)
        draw.text((130, 1130), "HOW SOLID INTEGRATIONS PROTECTS YOU:", fill="#38bdf8", font=get_font(32))
        draw.text((130, 1195), "1. SOLID OS: Inspects & locks every AI command in 1.2ms", fill="#ffffff", font=get_font(28))
        draw.text((130, 1255), "2. v2_LEDGER: Tamper-proof audit vault (TRAIGA Safe Harbor)", fill="#10b981", font=get_font(28))
        draw.text((130, 1315), "3. SOLID ZERO: Battery grid shock-absorber for ERCOT RTC+B", fill="#facc15", font=get_font(28))

    # --- SCENE 6 (33.0 - End): 100% OPTIMAL & CALL TO ACTION ---
    else:
        draw.text((80, 210), "100% DETERMINISTIC RELIABILITY", fill="#10b981", font=get_font(48))
        draw.text((80, 270), "Zero Blackouts. Zero Fines. Zero Hallucinations.", fill="#cbd5e1", font=get_font(28))

        draw_character_guardian(draw, 540, 620, t)

        # Big High-Converting CTA Card
        draw.rounded_rectangle([(70, 940), (1010, 1410)], radius=28, fill="#022c22", outline="#10b981", width=6)
        draw.text((180, 1000), "SOLID INTEGRATIONS LLC", fill="#facc15", font=get_font(48))
        draw.text((140, 1075), "Enterprise AI Firewalls • Grid BESS • Transit Logic", fill="#ffffff", font=get_font(30))
        
        # Glowing Button
        draw.rounded_rectangle([(120, 1160), (960, 1280)], radius=20, fill="#2563eb", outline="#ffffff", width=4)
        draw.text((195, 1198), "solid-integrations.polsia.io", fill="#ffffff", font=get_font(44))
        draw.text((230, 1320), "CAGE: 20U61  |  UEI: XT2KK6DNSLR5  |  DALLAS, TX", fill="#34d399", font=get_font(24))

    # Render Word-by-Word TikTok Captions on every frame
    draw_captions(draw, t)

    # Bottom Persistent Branding Bar
    draw.rectangle([(0, 1830), (1080, 1920)], fill="#090d16")
    draw.text((220, 1860), "LINK IN BIO -> solid-integrations.polsia.io", fill="#38bdf8", font=get_font(28))

    return img

def main():
    os.makedirs("assets/audio", exist_ok=True)
    os.makedirs("output/viral_frames", exist_ok=True)

    audio_path = "assets/audio/mindblowing_voice.mp3"
    asyncio.run(make_audio(audio_path))

    # Measure audio duration via ffmpeg stderr
    res = subprocess.run(["ffmpeg", "-i", audio_path], stderr=subprocess.PIPE, text=True)
    duration = 41.0
    for line in res.stderr.split("\n"):
        if "Duration:" in line:
            t_str = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = t_str.split(":")
            duration = float(h)*3600 + float(m)*60 + float(s)
            break

    fps = 24
    total_frames = int(duration * fps)
    print(f"[2/4] Animating {total_frames} frames with characters, live charts & captions...")

    for idx in range(total_frames):
        t = idx / fps
        img = render_scene_frame(t, duration)
        img.save(f"output/viral_frames/f_{idx:05d}.jpg", quality=92)
        if idx % 96 == 0:
            print(f"  -> Animated {int((idx/total_frames)*100)}% ({idx}/{total_frames} frames)")

    print("[3/4] Synthesizing dark sub-bass tension pulse & mixing audio...")
    out_video = "output/solid_integrations_viral_master.mp4"
    
    # Mix voice with a generated dark cyber sub-bass pulse (55Hz + 110Hz) so there's zero dead air
    cmd = [
        "ffmpeg", "-y",
        "-r", str(fps),
        "-i", "output/viral_frames/f_%05d.jpg",
        "-i", audio_path,
        "-f", "lavfi", "-i", f"aevalsrc='0.08*sin(2*PI*55*t)+0.04*sin(2*PI*110*t)*exp(-mod(t,0.5)*6)':d={duration}",
        "-filter_complex", "[1:a]volume=1.2[v];[2:a]volume=0.6[bg];[v][bg]amix=inputs=2:duration=first[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        out_video
    ]
    subprocess.run(cmd, check=True)
    print(f"\n[4/4] [✓] MIND-BLOWING VIRAL MASTER READY: {out_video}")
    subprocess.run(["open", out_video])

if __name__ == "__main__":
    main()
