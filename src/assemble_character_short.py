#!/usr/bin/env python3
import os
import math
import asyncio
import subprocess
import edge_tts

VOICE = "en-US-BrianNeural"
FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"

SCRIPT = (
    "Imagine hiring a genius intern who is ninety-nine percent brilliant, but one percent of the time, he pours hot coffee straight into the main server. "
    "In real life, that intern is AI. When companies connect AI directly to city power grids or transit systems, that tiny one percent hallucination trips a breaker and cuts power to five hundred thousand homes. "
    "That is why you never let AI touch physical machines alone. You need a digital bouncer. A deterministic logic firewall that inspects and locks down every single packet before it touches real hardware. "
    "Stop guessing with mission-critical systems. Build infrastructure that cannot fail at solid-integrations.polsia.io. Link in bio."
)

async def generate_voice(text, path):
    print("[1/3] Generating Brian's urgent documentary voiceover...")
    comm = edge_tts.Communicate(text, VOICE, rate="+14%", pitch="-2Hz")
    await comm.save(path)

def main():
    os.makedirs("assets/scenes", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    audio_path = "assets/audio/viral_voice.mp3"
    asyncio.run(generate_voice(SCRIPT, audio_path))

    # Note: Save the 4 images above as scene1.jpg, scene2.jpg, scene3.jpg, scene4.jpg in assets/scenes/
    print("[2/3] Sequencing 4 character scenes with cinematic Ken Burns camera push-in...")

    # Filter: 4 scenes evenly timed, each with continuous slow push-in zoom and center typography
    filter_complex = (
        # Scene 1 (AI Intern: 0-7s)
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "zoompan=z='min(zoom+0.0015,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=175:s=1080x1920:fps=25[v0];"
        
        # Scene 2 (Server Fire Panic: 7-15s)
        "[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "zoompan=z='min(zoom+0.002,1.2)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=200:s=1080x1920:fps=25[v1];"
        
        # Scene 3 (The Solid Bouncer Shield: 15-25s)
        "[2:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "zoompan=z='min(zoom+0.0015,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=250:s=1080x1920:fps=25[v2];"
        
        # Scene 4 (City Optimal & Thumbs Up: 25s-End)
        "[3:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "zoompan=z='min(zoom+0.001,1.1)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=250:s=1080x1920:fps=25[v3];"
        
        # Concat the 4 animated camera scenes
        "[v0][v1][v2][v3]concat=n=4:v=1:a=0[raw_v];"
        
        # Dynamic HUD Overlays
        "[raw_v]"
        "drawbox=y=120:color=black@0.65:width=iw:height=140:t=fill,"
        f"drawtext=fontfile='{FONT_PATH}':text='WHY YOU NEVER PLUG AI INTO THE GRID':fontcolor=0xfacc15:fontsize=46:x=(w-text_w)/2:y=170,"
        "drawbox=y=1640:color=black@0.75:width=iw:height=180:t=fill,"
        f"drawtext=fontfile='{FONT_PATH}':text='SOLID INTEGRATIONS // DETERMINISTIC FIREWALL':fontcolor=0x38bdf8:fontsize=34:x=(w-text_w)/2:y=1690,"
        f"drawtext=fontfile='{FONT_PATH}':text='solid-integrations.polsia.io':fontcolor=white:fontsize=28:x=(w-text_w)/2:y=1740[vout]"
    )

    out_file = "output/viral_character_short.mp4"

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

    print("[3/3] Encoding master short...")
    subprocess.run(cmd, check=True)
    print(f"\n[✓] VIRAL SHORT READY: {out_file}")
    subprocess.run(["open", out_file])

if __name__ == "__main__":
    main()
