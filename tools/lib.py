import math, subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

F = "/usr/share/fonts/opentype/inter/"
FONTS = {"r": F + "Inter-Regular.otf", "m": F + "Inter-Medium.otf", "s": F + "Inter-SemiBold.otf",
         "b": F + "Inter-Bold.otf", "db": F + "InterDisplay-Bold.otf", "dx": F + "InterDisplay-ExtraBold.otf",
         "dk": F + "InterDisplay-Black.otf"}
_fc = {}


def font(w, s):
    k = (w, s)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FONTS[w], s)
    return _fc[k]


BG = (11, 10, 20)
INK = (245, 245, 250)
MUTED = (160, 160, 185)
PURPLE = (124, 58, 237)
VIOLET = (167, 139, 250)
ORANGE = (249, 115, 22)
AMBER = (251, 191, 36)
GREEN = (134, 239, 172)
RED = (248, 113, 113)
CARD = (24, 22, 40)
LINE = (52, 48, 80)


def clamp(x, a=0, b=1):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def prog(t, s, d=0.45):
    return ease((t - s) / d)


def background(W, H, seed=0):
    img = Image.new("RGB", (W, H), BG)
    g = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(g)
    r = int(W * 0.55)
    d.ellipse([-r * 0.6, -r * 0.5, r * 1.0, r * 1.1], fill=(70, 30, 150))
    d.ellipse([W - r * 0.9, H - r * 1.2, W + r * 0.7, H + r * 0.4], fill=(150, 60, 10))
    g = g.filter(ImageFilter.GaussianBlur(W * 0.18))
    img = Image.blend(img, g, 0.55)
    # subtle grid
    d = ImageDraw.Draw(img)
    img = Image.blend(Image.new("RGB", (W, H), BG), img, 1.0)
    return img


def grad_text_img(text, f, c1=VIOLET, c2=ORANGE):
    bbox = f.getbbox(text)
    w, h = bbox[2] + 4, bbox[3] + 8
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).text((0, 0), text, font=f, fill=255)
    grad = Image.new("RGB", (w, h))
    gd = ImageDraw.Draw(grad)
    for x in range(w):
        p = x / max(1, w - 1)
        gd.line([(x, 0), (x, h)], fill=tuple(int(c1[i] + (c2[i] - c1[i]) * p) for i in range(3)))
    return grad, mask


def paste_alpha(base, img, mask, xy, alpha):
    if alpha <= 0:
        return
    m = mask.point(lambda v: int(v * alpha))
    base.paste(img, (int(xy[0]), int(xy[1])), m)


class Layer:
    """Draw on an RGBA overlay with global alpha, then composite."""

    def __init__(self, base):
        self.base = base
        self.ov = Image.new("RGBA", base.size, (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.ov)

    def done(self, alpha=1.0):
        if alpha < 1:
            a = self.ov.getchannel("A").point(lambda v: int(v * alpha))
            self.ov.putalpha(a)
        self.base.paste(self.ov, (0, 0), self.ov)


def text(base, xy, s, w, size, color=INK, alpha=1.0, anchor="la", dy=0, grad=False, spacing=10, align="left"):
    if alpha <= 0:
        return
    f = font(w, size)
    x, y = xy[0], xy[1] + dy
    if grad:
        img, mask = grad_text_img(s, f)
        if anchor[0] == "m":
            x -= img.width / 2
        paste_alpha(base, img, mask, (x, y), alpha)
        return
    L = Layer(base)
    L.d.multiline_text((x, y), s, font=f, fill=color + (int(255 * alpha),), anchor=anchor, spacing=spacing, align=align)
    L.done()


def rrect(base, box, r, fill=CARD, outline=None, width=2, alpha=1.0):
    if alpha <= 0:
        return
    L = Layer(base)
    L.d.rounded_rectangle(box, r, fill=fill + (255,) if fill else None, outline=outline + (255,) if outline else None, width=width)
    L.done(alpha)


def wrap(s, w, size, maxw):
    f = font(w, size)
    out = []
    for para in s.split("\n"):
        line = ""
        for word in para.split(" "):
            t = (line + " " + word).strip()
            if f.getlength(t) <= maxw:
                line = t
            else:
                out.append(line)
                line = word
        out.append(line)
    return "\n".join(out)


def logo(base, xy, size=44, alpha=1.0, anchor="l"):
    f = font("dx", size)
    s1, s2 = "Karvan", "AI"
    w1 = f.getlength(s1)
    w2 = f.getlength(s2)
    x, y = xy
    if anchor == "m":
        x -= (w1 + w2) / 2
    text(base, (x, y), s1, "dx", size, INK, alpha)
    text(base, (x + w1 + 2, y), s2, "dx", size, alpha=alpha, grad=True)


def tl(n):
    return f"{n:,.0f}".replace(",", ".")


def render_video(name, frame_fn, dur, cues, fps=30, W=1080, H=1920, music_vol=0.35):
    """frame_fn(t)->PIL RGB. cues: list of (time, sfxname, vol)."""
    os.makedirs("out", exist_ok=True)
    silent = f"/tmp/{name}_v.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                          "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
    n = int(dur * fps)
    for i in range(n):
        p.stdin.write(frame_fn(i / fps).tobytes())
    p.stdin.close()
    p.wait()
    # audio mix
    inputs = ["-i", silent, "-i", "sfx/bed.wav"]
    filt = [f"[1:a]atrim=0:{dur},afade=t=in:d=0.6,afade=t=out:st={dur - 1.2}:d=1.2,volume={music_vol}[m]"]
    labels = ["[m]"]
    for k, (ts, s, v) in enumerate(cues):
        inputs += ["-i", f"sfx/{s}.wav"]
        ms = int(ts * 1000)
        filt.append(f"[{k + 2}:a]adelay={ms}|{ms},volume={v}[c{k}]")
        labels.append(f"[c{k}]")
    filt.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0,alimiter=limit=0.9[a]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt),
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-t", str(dur), "-movflags", "+faststart", f"out/{name}.mp4"], check=True)
    print("rendered", name)
