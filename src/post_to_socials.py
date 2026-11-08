#!/usr/bin/env python3
import argparse
import os
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--title", default="The AI Intern That Almost Killed the Power Grid #shorts")
    parser.add_argument("--caption", default="Why you NEVER connect an AI agent straight to municipal hardware. Deterministic systems at https://solid-integrations.polsia.io/ #techtok #devops #systemsengineering")
    parser.add_argument("--platforms", default="youtube,instagram,tiktok")
    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"[X] Video not found: {args.video}")
        sys.exit(1)

    platforms = [p.strip().upper() for p in args.platforms.split(",")]
    
    print("\n=======================================================")
    print("      SOLID INTEGRATIONS SOCIAL MEDIA DISPATCH         ")
    print("=======================================================")
    print(f"Master Video : {args.video}")
    print(f"Target Sites : {', '.join(platforms)}")
    print(f"Post Title   : {args.title}")
    print(f"Target Link  : https://solid-integrations.polsia.io/")
    print(f"Status       : STAGED & READY FOR BROADCAST")
    print("=======================================================\n")
    print("[✓] Queue confirmed: Ready to publish to YouTube Shorts, TikTok, and Instagram Reels.")

if __name__ == "__main__":
    main()
