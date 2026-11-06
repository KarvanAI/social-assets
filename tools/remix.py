"""Re-time reels to ElevenLabs VO (piecewise time warp) and render with VO only (no SFX/music)."""
import subprocess, sys
from reels import REELS, W, H

U = "/mnt/user-data/uploads/"
VO = {"r1": U + "4eb0c91e-New_tts_node-2.mp3", "r2": U + "79a12918-New_tts_node.mp3",
      "r3": U + "4cc4cc0e-New_tts_node-4.mp3", "r4": U + "3112c2ad-New_tts_node-5.mp3",
      "r5": U + "a1f061a2-New_tts_node-3.mp3"}

# (vo_start, vo_end, orig_start, orig_end)
WARP = {
    "r1": (20.4, [(0, 1.6, 0, .6), (1.6, 3.9, .6, 2.5), (3.9, 5.45, 2.5, 3.39), (5.45, 6.3, 7.4, 7.9), (6.3, 8.2, 7.9, 8.5),
                  (8.2, 10.66, 8.5, 9.1), (10.66, 13.1, 9.1, 10.99), (13.1, 16.4, 11, 12.99), (16.4, 20.4, 13, 14.99)]),
    "r2": (21.6, [(0, 1.2, 0, .6), (1.2, 2.76, .6, 1.3), (2.76, 3.9, 1.3, 1.7), (3.9, 5.42, 1.7, 2.3), (5.42, 6.4, 2.3, 3.19),
                  (6.4, 12.3, 3.2, 8.39), (12.3, 17.6, 8.4, 13.59), (17.6, 21.6, 13.6, 15.99)]),
    "r3": (18.6, [(0, 1.6, 0, .8), (1.6, 3.2, .8, 2.59), (3.2, 5.6, 2.6, 3.4), (5.6, 9.8, 3.4, 4.6), (9.8, 12.0, 4.6, 7.0),
                  (12.0, 13.0, 7.0, 8.4), (13.0, 15.6, 8.4, 11.19), (15.6, 18.6, 11.2, 13.99)]),
    "r4": (19.5, [(0, 2.0, 0, 2.59), (2.0, 2.2, 2.6, 2.9), (2.2, 6.8, 2.9, 5.1), (6.8, 10.0, 5.1, 7.3), (10.0, 13.2, 7.3, 9.5),
                  (13.2, 16.3, 9.5, 12.59), (16.3, 19.5, 12.6, 14.99)]),
    "r5": (20.4, [(0, 2.4, 0, 2.99), (2.4, 7.6, 3.0, 8.39), (7.6, 10.4, 8.4, 8.9), (10.4, 12.6, 8.9, 10.0),
                  (12.6, 15.6, 10.0, 11.1), (15.6, 17.4, 11.1, 13.59), (17.4, 20.4, 13.6, 15.99)]),
}


def warp(segs, t):
    for a, b, c, d in segs:
        if t < b:
            return c + (d - c) * (t - a) / (b - a)
    return segs[-1][3]


def render(k, fps=30):
    fn, orig_d, _ = REELS[k]
    D, segs = WARP[k]
    silent = f"/tmp/{k}_vo_v.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                          "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
    for i in range(int(D * fps)):
        t = i / fps
        # progress bar uses real time: pass warped time but bar follows orig duration -> fine
        p.stdin.write(fn(warp(segs, t)).tobytes())
    p.stdin.close(); p.wait()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", VO[k],
                    "-filter_complex", f"[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,apad,atrim=0:{D},afade=t=out:st={D - 0.4}:d=0.4[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-t", str(D), "-movflags", "+faststart", f"out/{k}.mp4"], check=True)
    print("rendered", k, D)


if __name__ == "__main__":
    for k in sys.argv[1:]:
        render(k)
