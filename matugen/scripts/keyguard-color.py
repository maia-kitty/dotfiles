#!/usr/bin/env python3
#Sync Keyguard's Material You accent color to matugen's generated palette.
import json, sys, colorsys
from pathlib import Path

PRESETS = {
    "red": "#F44336", "pink": "#E91E63", "purple": "#9C27B0",
    "deep_purple": "#673AB7", "indigo": "#3F51B5", "blue": "#2196F3",
    "cyan": "#00BCD4", "teal": "#009688", "green": "#4CAF50",
    "light_green": "#8BC34A", "lime": "#CDDC39", "yellow": "#FFEB3B",
    "amber": "#FFC107", "orange": "#FF9800", "deep_orange": "#FF5722",
    "brown": "#795548", "gray": "#9E9E9E",
}

CANDIDATE_PATHS = [
    Path.home() / ".local/share/keyguard/settings",
    Path.home() / ".var/app/com.artemchep.keyguard/data/keyguard/settings",
]

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def closest(hex_color):
    r1, g1, b1 = hex_to_rgb(hex_color)
    h1, l1, s1 = colorsys.rgb_to_hls(r1/255, g1/255, b1/255)
    if s1 < 0.15:
        return "gray"
    best, best_dist = None, float("inf")
    for name, phex in PRESETS.items():
        r2, g2, b2 = hex_to_rgb(phex)
        h2, _, _ = colorsys.rgb_to_hls(r2/255, g2/255, b2/255)
        dist = min(abs(h1 - h2), 1 - abs(h1 - h2))
        if dist < best_dist:
            best, best_dist = name, dist
    return best

def main():
    if len(sys.argv) < 2:
        print("usage: keyguard-color.py <hex>", file=sys.stderr)
        sys.exit(1)

    settings_path = next((p for p in CANDIDATE_PATHS if p.exists()), None)
    if settings_path is None:
        # Keyguard isn't installed / hasn't run yet — nothing to do
        sys.exit(0)

    data = json.loads(settings_path.read_text())
    data["colors"] = closest(sys.argv[1])
    settings_path.write_text(json.dumps(data))

if __name__ == "__main__":
    main()
