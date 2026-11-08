#!/usr/bin/env python3
import argparse
import asyncio
import json
import os
import subprocess
import edge_tts

VOICE = "en-US-BrianNeural"

# Guaranteed built-in macOS system font
MACOS_FONT = "/System/Library/Fonts/Helvetica.ttc"

async def synthesize_audio(text, audio_path):
    communicate = edge_tts.Communicate(text, VOICE, rate="+14%", pitch="-2Hz")
    await communicate.save(audio_path)
    print(f"[✓] Voiceover generated: {audio_path}")

def clean_text(text):
    return text.upper().replace(":", " - ").replace(",", " ").replace("'", "").strip()

def assemble_short(script_json_path, output_mp4):
    with open(script_json_path, "r") as f:
        data = json.load(f)

    os.makedirs("assets/audio", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    voice_path = "assets/audio/voiceover.mp3"
    asyncio.run(synthesize_audio(data["full_text"], voice_path))

    title_clean = clean_text(data["title"])
    topic_clean = clean_text(data.get("topic", "CRITICAL INFRASTRUCTURE"))

    print("[i] Rendering Cyber Telemetry HUD...")

    font_arg = f":fontfile={MACOS_FONT}" if os.path.exists(MACOS_FONT) else ""

    filter_complex = (
        # 1. Dark canvas with animated radar scanline
        "color=c=0x070b14:s=1080x1920:r=25[bg];"
        "[bg]drawgrid=width=72:height=72:thickness=1:color=0x1e293b@0.6[grid];"
        "[grid]drawbox=y='mod(t*400,1920)':color=0x38bdf8@0.2:width=iw:height=80:t=fill[scanned];"
        
        # 2. Live Neon Audio Waveform reacting to the voice
        "[0:a]showwaves=s=920x360:mode=cline:colors=0x38bdf8|0x0284c7:rate=25[wave];"
        "[scanned][wave]overlay=x=(W-w)/2:y=1300[with_wave];"
        
        # 3. Warning Badges and Center Cards
        "[with_wave]"
        "drawbox=y=120:color=black@0.75:width=iw:height=200:t=fill,"
        "drawbox=x=80:y=120:width=920:height=4:color=0xef4444:t=fill,"
        f"drawtext=text='LIVE SCADA TELEMETRY // SECTOR - DFW-01'{font_arg}:fontcolor=0xef4444:fontsize=32:x=(w-text_w)/2:y=150,"
        f"drawtext=text='SYSTEM DESYNCHRONIZATION RISK - CRITICAL'{font_arg}:fontcolor=white:fontsize=28:x=(w-text_w)/2:y=195,"
        f"drawtext=text='REACTIVE PROTOCOL - DETERMINISTIC LOGIC'{font_arg}:fontcolor=0x38bdf8:fontsize=24:x=(w-text_w)/2:y=245,"
        
        "drawbox=y=620:color=black@0.85:width=iw:height=460:t=fill,"
        "drawbox=x=80:y=620:width=920:height=4:color=0xfacc15:t=fill,"
        f"drawtext=text='{title_clean}'{font_arg}:fontcolor=0xfacc15:fontsize=48:x=(w-text_w)/2:y=720,"
        f"drawtext=text='TARGET - {topic_clean}'{font_arg}:fontcolor=white:fontsize=32:x=(w-text_w)/2:y=830,"
        f"drawtext=text='FAILSAFE - SOLID-INTEGRATIONS.POLSIA.IO'{font_arg}:fontcolor=0x38bdf8:fontsize=34:x=(w-text_w)/2:y=940,"
        "drawbox=x=80:y=1080:width=920:height=4:color=0xfacc15:t=fill[vout]"
    )

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", voice_path,
        "-filter_complex", filter_complex,
        "-map", "[vout]",
        "-map", "0:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "19",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        output_mp4
    ]

    res = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("[!] FFmpeg Error Output:\n", res.stderr)
        res.check_returncode()
    
    print(f"\n[✓] VIDEO RENDER COMPLETE: {output_mp4}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--script", required=True)
    args = parser.parse_args()

    date_tag = os.path.basename(args.script).replace(".json", "")
    output_file = f"output/{date_tag}_hud.mp4"
    assemble_short(args.script, output_file)

if __name__ == "__main__":
    main()
