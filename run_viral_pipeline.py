#!/usr/bin/env python3
import os
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

def build_all_scenes():
    print("[1/4] Generating high-impact visual scene cards...")
    os.makedirs("assets/scenes", exist_ok=True)
    
    scenes = [
        ("assets/scenes/scene1.jpg", "#0f172a", "#38bdf8", "THE 'GENIUS INTERN' TRAP", "99% Brilliant. 1% Fatal Hallucination.", "WHY YOU NEVER PLUG RAW AI INTO THE GRID"),
        ("assets/scenes/scene2.jpg", "#450a0a", "#ef4444", "GRID FREQUENCY COLLAPSE", "59.72 Hz // 500,000 Homes Dark", "PHYSICAL RELAYS TRIP ON 0.1% DRIFT"),
        ("assets/scenes/scene3.jpg", "#0c4a6e", "#facc15", "THE SOLID OS DIGITAL BOUNCER", "Deterministic Logic Verification Layer", "ZERO UNVERIFIED PACKETS TOUCH HARDWARE"),
        ("assets/scenes/scene4.jpg", "#022c22", "#10b981", "SYSTEMS 100% OPERATIONAL", "solid-integrations.polsia.io", "SOVEREIGN INFRASTRUCTURE & SYSTEMS ARCHITECTURE")
    ]

    for path, bg, accent, title, sub, tag in scenes:
        img = Image.new("RGB", (1080, 1920), color=bg)
        draw = ImageDraw.Draw(img)
        
        # Grid lines
        for y in range(0, 1920, 80):
            draw.line([(0, y), (1080, y)], fill="#1e293b", width=1)
        for x in range(0, 1080, 80):
            draw.line([(x, 0), (x, 1920)], fill="#1e293b", width=1)
            
        # Outer border
        draw.rectangle([(60, 160), (1020, 1760)], outline=accent, width=5)
        
        # Top Badge
        draw.rounded_rectangle([(100, 240), (980, 360)], radius=15, fill="#000000")
        draw.text((140, 280), tag, fill=accent, font=get_font(30))
        
        # Center Hero Box
        draw.rounded_rectangle([(100, 680), (980, 1140)], radius=20, fill="#000000", outline=accent, width=4)
        draw.text((140, 780), title, fill="#ffffff", font=get_font(46))
        draw.text((140, 880), sub, fill=accent, font=get_font(34))
        
        # Bottom Telemetry Badge
        draw.text((140, 1600), "SOLID INTEGRATIONS LLC // DALLAS, TX", fill="#64748b", font=get_font(24))
        draw.text((140, 1640), "CAGE: 20U61  |  UEI: XT2KK6DNSLR5", fill="#64748b", font=get_font(22))
        
        img.save(path)
        print(f"  [✓] Built: {path}")

async def generate_voice(text, path):
    print("[2/4] Recording Brian's urgent voiceover...")
    comm = edge_tts.Communicate(text, VOICE, rate="+14%", pitch="-2Hz")
    await comm.save(path)
    print(f"  [✓] Voiceover complete: {path}")

def render_final_video():
    print("[3/4] Rendering 9:16 vertical short with camera push-ins...")
    audio_path = "assets/audio/viral_voice.mp3"
    out_file = "output/viral_character_short.mp4"
    
    script_text = (
        "Imagine hiring a genius intern who is ninety-nine percent brilliant, but one percent of the time, he pours hot coffee straight into the main server. "
        "In real life, that intern is AI. When companies connect AI directly to city power grids or transit systems, that tiny one percent hallucination trips a breaker and cuts power to five hundred thousand homes. "
        "That is why you never let AI touch physical machines alone. You need a digital bouncer. A deterministic logic firewall that inspects and locks down every single packet before it touches real hardware. "
        "Stop guessing with mission-critical systems. Build infrastructure that cannot fail at solid-integrations.polsia.io. Link in bio."
    )
    
    os.makedirs("assets/audio", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    asyncio.run(generate_voice(script_text, audio_path))

    filter_complex = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "zoompan=z='min(zoom+0.0015,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=175:s=1080x1920:fps=25[v0];"
        
        "[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "zoompan=z='min(zoom+0.002,1.2)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=200:s=1080x1920:fps=25[v1];"
        
        "[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "zoompan=z='min(zoom+0.0015,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=250:s=1080x1920:fps=25[v2];"
        
        "[3:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "zoompan=z='min(zoom+0.001,1.1)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=250:s=1080x1920:fps=25[v3];"
        
        "[v0][v1][v2][v3]concat=n=4:v=1:a=0[raw_v];"
        
        "[raw_v]"
        "drawbox=y=100:color=black@0.7:width=iw:height=140:t=fill,"
        f"drawtext=fontfile='{FONT_PATH}':text='WHY YOU NEVER PLUG RAW AI INTO HARDWARE':fontcolor=0xfacc15:fontsize=40:x=(w-text_w)/2:y=150,"
        "drawbox=y=1660:color=black@0.8:width=iw:height=180:t=fill,"
        f"drawtext=fontfile='{FONT_PATH}':text='SOLID INTEGRATIONS // DETERMINISTIC FIREWALL':fontcolor=0x38bdf8:fontsize=32:x=(w-text_w)/2:y=1710,"
        f"drawtext=fontfile='{FONT_PATH}':text='solid-integrations.polsia.io':fontcolor=white:fontsize=26:x=(w-text_w)/2:y=1760[vout]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", "7", "-i", "assets/scenes/scene1.jpg",
        "-loop", "1", "-t", "8", "-i", "assets/scenes/scene2.jpg",
        "-loop", "1", "-t", "10", "-i", "assets/scenes/scene3.jpg",
        "-loop", "1", "-t", "10", "-i", "assets/scenes/scene4.jpg",
        "-i", audio_path,
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-map", "4:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        out_file
    ]
    subprocess.run(cmd, check=True)
    print(f"\n[4/4] [✓] VIRAL SHORT RENDER COMPLETE: {out_file}")
    print("[i] Opening video player...")
    subprocess.run(["open", out_file])

if __name__ == "__main__":
    build_all_scenes()
    render_final_video()
