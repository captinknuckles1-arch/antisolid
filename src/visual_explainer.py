#!/usr/bin/env python3
import os
import math
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

async def generate_voice(text, path):
    print("[1/3] Generating voiceover...")
    comm = edge_tts.Communicate(text, VOICE, rate="+12%", pitch="-2Hz")
    await comm.save(path)

def render_frame(t, total_time):
    """
    Renders 1080x1920 graphic frames based on timestamp t
    """
    img = Image.new("RGB", (1080, 1920), color="#080c16")
    draw = ImageDraw.Draw(img)

    # 1. Permanent Header
    draw.rectangle([(0, 0), (1080, 160)], fill="#0f172a")
    draw.line([(0, 160), (1080, 160)], fill="#38bdf8", width=3)
    draw.text((80, 60), "SOLID INTEGRATIONS // SYSTEMS TELEMETRY", fill="#38bdf8", font=get_font(34))
    draw.text((80, 105), "INFRASTRUCTURE AUDIT & LOGIC SIMULATION", fill="#94a3b8", font=get_font(24))

    # Phase Breakdown
    # 0s - 8s   : Scene 1 (AI vs Legacy SCADA)
    # 8s - 18s  : Scene 2 (Grid Frequency Crash)
    # 18s - 28s : Scene 3 (Solid OS Deterministic Firewall)
    # 28s - End : Scene 4 (System Stabilization & CTA)

    if t < 8.0:
        # --- SCENE 1: Stochastic AI vs Legacy Infrastructure ---
        draw.text((100, 240), "THE PROBLEM: STOCHASTIC COUPLING", fill="#facc15", font=get_font(44))
        draw.text((100, 295), "Connecting probabilistic LLMs to deterministic hardware", fill="#94a3b8", font=get_font(26))

        # Node A: AI Agent
        draw.rounded_rectangle([(140, 420), (460, 680)], radius=20, fill="#1e1b4b", outline="#818cf8", width=4)
        draw.text((190, 520), "AI AGENT", fill="#ffffff", font=get_font(42))
        draw.text((170, 580), "Stochastic / Probabilistic", fill="#a5b4fc", font=get_font(24))

        # Node B: Municipal / SCADA
        draw.rounded_rectangle([(620, 420), (940, 680)], radius=20, fill="#312e81", outline="#38bdf8", width=4)
        draw.text((660, 520), "GRID SCADA", fill="#ffffff", font=get_font(38))
        draw.text((650, 580), "Legacy 1980s Hardware", fill="#38bdf8", font=get_font(24))

        # Erratic Moving Packets
        cycle = (t * 4) % 1.0
        px = 460 + (620 - 460) * cycle
        py = 550 + math.sin(t * 12) * 45
        draw.line([(460, 550), (620, 550)], fill="#475569", width=4)
        draw.ellipse([(px-20, py-20), (px+20, py+20)], fill="#ef4444", outline="#ffffff", width=3)
        draw.text((px-50, py+30), "UNVERIFIED PACKET", fill="#ef4444", font=get_font(20))

        # Visual Warning Box
        draw.rounded_rectangle([(120, 840), (960, 1100)], radius=15, fill="#18181b", outline="#ef4444", width=3)
        draw.text((160, 890), "! 0.1% Hallucination = Physical Relay Trip", fill="#ef4444", font=get_font(36))
        draw.text((160, 955), "Legacy systems expect deterministic binary truth.", fill="#e4e4e7", font=get_font(28))
        draw.text((160, 1005), "A single stochastic drift triggers emergency lockout.", fill="#a1a1aa", font=get_font(26))

    elif t < 18.0:
        # --- SCENE 2: The Grid Frequency Crash ---
        draw.text((100, 240), "PHYSICAL IMPACT: FREQUENCY COLLAPSE", fill="#ef4444", font=get_font(44))
        draw.text((100, 295), "ERCOT Regional Interconnection Telemetry", fill="#94a3b8", font=get_font(26))

        # Dial / Gauge Center
        cx, cy, r = 540, 680, 260
        draw.arc([(cx-r, cy-r), (cx+r, cy+r)], start=140, end=400, fill="#334155", width=36)
        draw.arc([(cx-r, cy-r), (cx+r, cy+r)], start=140, end=250, fill="#ef4444", width=36) # Critical red
        draw.arc([(cx-r, cy-r), (cx+r, cy+r)], start=250, end=400, fill="#10b981", width=36) # Safe green

        # Sweeping Needle from 60.0 to 59.7 Hz
        progress = min(1.0, (t - 8.0) / 7.0)
        angle_deg = 360 - (progress * 130)
        rad = math.radians(angle_deg)
        nx = cx + (r - 40) * math.cos(rad)
        ny = cy + (r - 40) * math.sin(rad)
        draw.line([(cx, cy), (nx, ny)], fill="#ffffff", width=8)
        draw.ellipse([(cx-25, cy-25), (cx+25, cy+25)], fill="#facc15")

        freq_val = 60.00 - (progress * 0.28)
        draw.text((410, 840), f"{freq_val:.2f} Hz", fill="#ef4444" if freq_val < 59.85 else "#10b981", font=get_font(72))
        draw.text((450, 930), "CRITICAL TRIP POINT: 59.80 Hz", fill="#ef4444", font=get_font(26))

        # Alert Box
        draw.rounded_rectangle([(120, 1080), (960, 1340)], radius=15, fill="#450a0a", outline="#dc2626", width=4)
        draw.text((160, 1130), "AUTOMATIC GENERATION DROPOUT", fill="#fca5a5", font=get_font(38))
        draw.text((160, 1200), "Relays open. Substation disconnects.", fill="#ffffff", font=get_font(30))
        draw.text((160, 1250), "Hardware fail-safe locks down the sector.", fill="#fca5a5", font=get_font(26))

    elif t < 28.0:
        # --- SCENE 3: Solid OS Deterministic Logic Firewall ---
        draw.text((100, 240), "THE ARCHITECTURE: SOLID OS", fill="#38bdf8", font=get_font(44))
        draw.text((100, 295), "Deterministic Logic Verification & State Control", fill="#94a3b8", font=get_font(26))

        # Node A: AI
        draw.rounded_rectangle([(80, 480), (320, 700)], radius=16, fill="#1e1b4b", outline="#818cf8", width=3)
        draw.text((120, 560), "AI AGENT", fill="#ffffff", font=get_font(32))

        # Center: Solid OS Engine
        draw.rounded_rectangle([(390, 440), (690, 740)], radius=20, fill="#0284c7", outline="#facc15", width=5)
        draw.text((420, 540), "SOLID OS", fill="#ffffff", font=get_font(44))
        draw.text((420, 600), "DETERMINISTIC", fill="#fef08a", font=get_font(22))
        draw.text((420, 630), "FIREWALL LAYER", fill="#fef08a", font=get_font(22))

        # Node C: Grid
        draw.rounded_rectangle([(760, 480), (1000, 700)], radius=16, fill="#065f46", outline="#34d399", width=3)
        draw.text((820, 560), "SCADA", fill="#ffffff", font=get_font(32))

        # Verified Flow
        draw.line([(320, 590), (390, 590)], fill="#ef4444", width=5) # Inbound unverified
        draw.line([(690, 590), (760, 590)], fill="#10b981", width=5) # Outbound verified

        # Verification Box
        draw.rounded_rectangle([(120, 880), (960, 1280)], radius=15, fill="#0f172a", outline="#38bdf8", width=3)
        draw.text((160, 930), "IMMUTABLE AUDIT LOG & PACKET LOCK", fill="#38bdf8", font=get_font(34))
        draw.text((160, 1000), "• Eliminates stochastic drift before it hits hardware", fill="#ffffff", font=get_font(28))
        draw.text((160, 1060), "• Full SHA-256 state compliance & logging", fill="#ffffff", font=get_font(28))
        draw.text((160, 1120), "• Turnkey TRAIGA Safe-Harbor alignment", fill="#ffffff", font=get_font(28))
        draw.text((160, 1180), "• Zero unverified payload execution", fill="#10b981", font=get_font(28))

    else:
        # --- SCENE 4: Stabilization & CTA ---
        draw.text((100, 240), "SYSTEMS ONLINE // ZERO RISK", fill="#10b981", font=get_font(44))
        draw.text((100, 295), "Deterministic Grid & Enterprise Infrastructure", fill="#94a3b8", font=get_font(26))

        draw.rounded_rectangle([(120, 420), (960, 860)], radius=25, fill="#022c22", outline="#10b981", width=6)
        draw.text((260, 500), "STATUS: OPTIMAL", fill="#34d399", font=get_font(56))
        draw.text((230, 600), "FREQUENCY: 60.00 Hz [LOCKED]", fill="#ffffff", font=get_font(34))
        draw.text((230, 660), "LATENCY: 1.2ms [DETERMINISTIC]", fill="#ffffff", font=get_font(34))
        draw.text((230, 720), "COMPLIANCE: 100% OPERATIONAL", fill="#ffffff", font=get_font(34))

        # Bottom Big CTA Card
        draw.rounded_rectangle([(80, 1020), (1000, 1420)], radius=25, fill="#0f172a", outline="#facc15", width=5)
        draw.text((220, 1080), "SOLID INTEGRATIONS LLC", fill="#facc15", font=get_font(46))
        draw.text((160, 1160), "Sovereign Infrastructure & Systems Architecture", fill="#e2e8f0", font=get_font(28))
        
        draw.rounded_rectangle([(140, 1240), (940, 1340)], radius=15, fill="#2563eb")
        draw.text((230, 1270), "solid-integrations.polsia.io", fill="#ffffff", font=get_font(40))

    # Bottom Footer
    draw.rectangle([(0, 1820), (1080, 1920)], fill="#0f172a")
    draw.text((140, 1855), "CAGE: 20U61  |  UEI: XT2KK6DNSLR5  |  DALLAS, TX", fill="#64748b", font=get_font(24))

    return img

def main():
    script_text = (
        "Your company wants to plug an AI agent straight into production. Here is why that is an operational disaster. "
        "When an API connects to municipal power or transit, every single packet must be deterministic. "
        "If an LLM hallucinates an output by zero point one percent, frequency drops below fifty-nine point eight hertz, circuit breakers trip, and the entire sector goes dark. "
        "You cannot connect stochastic AI to legacy hardware without an immutable logic firewall. "
        "Solid OS intercepts and verifies every single packet before it reaches the physical layer. "
        "Stop guessing. Build deterministic infrastructure that does not fail at solid-integrations.polsia.io. Link in bio."
    )

    audio_path = "assets/audio/explainer_voice.mp3"
    asyncio.run(generate_voice(script_text, audio_path))

    # Calculate exact duration
    probe_cmd = ["ffmpeg", "-i", audio_path]
    res = subprocess.run(probe_cmd, stderr=subprocess.PIPE, text=True)
    duration = 34.0
    for line in res.stderr.split("\n"):
        if "Duration" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            duration = float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
            break

    fps = 24
    total_frames = int(duration * fps)
    print(f"[2/3] Generating {total_frames} animated infographic frames ({duration:.1f}s at {fps} fps)...")

    os.makedirs("output/frames", exist_ok=True)
    for frame_idx in range(total_frames):
        t = frame_idx / fps
        frame = render_frame(t, duration)
        frame.save(f"output/frames/frame_{frame_idx:05d}.png")
        if frame_idx % 72 == 0:
            print(f"  Frame {frame_idx}/{total_frames} ({int(frame_idx/total_frames*100)}%)...")

    print("[3/3] Encoding animated video with voiceover...")
    out_video = "output/solid_integrations_explainer.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-r", str(fps),
        "-i", "output/frames/frame_%05d.png",
        "-i", audio_path,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        out_video
    ]
    subprocess.run(cmd, check=True)
    print(f"\n[✓] VIRAL EXPLAINER VIDEO COMPLETE: {out_video}")
    subprocess.run(["open", out_video])

if __name__ == "__main__":
    main()
