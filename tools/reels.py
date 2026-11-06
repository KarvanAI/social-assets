import sys
from lib import *

W, H = 1080, 1920
BGI = background(W, H)
M = 90  # margin
CW = W - 2 * M


def base(tag, t, dur):
    im = BGI.copy()
    logo(im, (M, 150), 40)
    text(im, (W - M, 160), tag, "s", 26, MUTED, anchor="ra")
    # progress bar
    rrect(im, (M, 230, W - M, 236), 3, fill=LINE)
    rrect(im, (M, 230, M + max(8, CW * t / dur), 236), 3, fill=ORANGE)
    return im


def out_alpha(t, end, d=0.3):
    return 1 - clamp((t - (end - d)) / d)


def endcard(im, t, s, line1, small="Rakamlar örnek veridir. KarvanAI bağımsızdır; Amazon ile bağlantılı değildir."):
    a = prog(t, s, 0.5)
    logo(im, (W / 2, 640 - 30 * (1 - a)), 110, a, anchor="m")
    text(im, (W / 2, 820), wrap(line1, "s", 50, CW), "s", 50, INK, a, anchor="ma", align="center", spacing=14)
    a2 = prog(t, s + 0.5)
    rrect(im, (M + 90, 1080, W - M - 90, 1200), 60, fill=ORANGE, alpha=a2)
    text(im, (W / 2, 1140), "Erken erişim: profildeki link", "b", 42, (20, 12, 4), a2, anchor="mm")
    text(im, (W / 2, 1290), wrap(small, "r", 28, CW), "r", 28, MUTED, prog(t, s + 0.8), anchor="ma", align="center")


def row(im, y, k, v, a, vc=INK, x0=M + 50, x1=W - M - 50):
    text(im, (x0, y), k, "m", 44, MUTED, a)
    text(im, (x1, y), v, "db", 52, vc, a, anchor="ra")


# ---------------- Reel 1: Haftanın boşa giden kelimesi #1
def r1(t):
    D = 15
    im = base("HAFTANIN BOŞA GİDEN KELİMESİ · #1", t, D)
    if t < 3.4:
        a = prog(t, 0.2) * out_alpha(t, 3.4)
        text(im, (M, 520), "Bu arama terimi", "db", 92, INK, a)
        text(im, (M, 630), "30 günde", "db", 92, INK, a)
        n = 2180 * ease((t - 0.6) / 1.6)
        text(im, (M, 780), tl(n) + " TL", "dk", 190, ORANGE, prog(t, 0.6) * out_alpha(t, 3.4))
        text(im, (M, 1020), "harcadı. Satış: 0", "db", 92, RED, prog(t, 2.5) * out_alpha(t, 3.4))
    elif t < 7.4:
        s = 3.4
        a = prog(t, s) * out_alpha(t, 7.4)
        text(im, (M, 430), "Arama terimi raporundan", "m", 44, MUTED, a)
        rrect(im, (M, 510, W - M, 1260), 40, fill=CARD, outline=LINE, alpha=a)
        text(im, (M + 50, 570), "“termos bardak ucuz”", "db", 66, INK, a)
        rows = [("Tıklama", "214", INK), ("Harcama", "2.180 TL", ORANGE), ("Sipariş", "0", RED), ("Satış", "0 TL", RED)]
        for i, (k, v, c) in enumerate(rows):
            ra = prog(t, s + 0.5 + i * 0.4) * out_alpha(t, 7.4)
            y = 720 + i * 125
            rrect(im, (M + 50, y - 22, W - M - 50, y - 20), 1, fill=LINE, alpha=ra)
            row(im, y, k, v, ra, c)
    elif t < 11:
        s = 7.4
        a = prog(t, s) * out_alpha(t, 11)
        text(im, (M, 470), "Neden?", "dk", 120, AMBER, a)
        lines = [("Ürünün:", "1 L çelik termos, 899 TL"), ("Arayan:", "ucuz bir bardak istiyor"), ("Sonuç:", "tıklıyor, fiyata bakıp çıkıyor")]
        for i, (k, v) in enumerate(lines):
            la = prog(t, s + 0.5 + i * 0.6) * out_alpha(t, 11)
            y = 680 + i * 190
            text(im, (M, y), k, "m", 44, MUTED, la)
            text(im, (M, y + 60), v, "db", 62, INK, la)
    elif t < 13:
        s = 11
        a = prog(t, s) * out_alpha(t, 13)
        text(im, (M, 560), "Çözüm", "m", 48, MUTED, a)
        text(im, (M, 630), wrap("Bu terimi exact negatif olarak ekle.", "dx", 100, CW), "dx", 100, GREEN, a, spacing=16)
        text(im, (M, 1000), wrap("İyi aramaları kesmemek için phrase ya da broad değil, exact ile başla.", "m", 44, CW), "m", 44, MUTED, prog(t, s + 0.6) * out_alpha(t, 13), spacing=12)
    else:
        endcard(im, t, 13, "KarvanAI bu terimleri her gece senin yerine bulur.")
    return im


R1 = (r1, 15, [(0.6, "whoosh", .5), (2.5, "thud", .9), (3.4, "whoosh", .6)] + [(3.9 + i * .4, "pop", .7) for i in range(4)] +
      [(7.4, "whoosh", .6)] + [(7.9 + i * .6, "pop", .6) for i in range(3)] + [(11, "ding", .7), (13, "whoosh", .5)] +
      [(0.6 + i * 0.08, "tick", .25) for i in range(20)])


# ---------------- Reel 2: Düşük ACoS kâr demek değil
def product(im, t, s, e, title, price, fees, cost, acos, good):
    a = prog(t, s) * out_alpha(t, e)
    be = (price - fees - cost) / price * 100
    profit = price - fees - cost - price * acos / 100
    text(im, (M, 400), title, "db", 76, INK, a)
    rrect(im, (M, 510, W - M, 1000), 40, fill=CARD, outline=LINE, alpha=a)
    rows = [("Satış fiyatı", f"{price} TL"), ("Amazon ücretleri", f"−{fees} TL"), ("Ürün maliyeti", f"−{cost} TL")]
    for i, (k, v) in enumerate(rows):
        row(im, 560 + i * 110, k, v, prog(t, s + 0.3 + i * 0.3) * out_alpha(t, e))
    ka = prog(t, s + 1.3) * out_alpha(t, e)
    rrect(im, (M + 50, 878, W - M - 50, 880), 1, fill=LINE, alpha=ka)
    row(im, 905, "Kâr sınırı (başabaş ACoS)", f"%{be:.0f}", ka, AMBER)
    # bar chart: ACoS vs sınır
    ba = prog(t, s + 1.9) * out_alpha(t, e)
    x0, x1, y = M, W - M, 1120
    scale = (x1 - x0) / 50
    rrect(im, (x0, y, x1, y + 70), 35, fill=(36, 33, 58), alpha=ba)
    fillw = scale * acos * ease((t - s - 2.0) / 0.9)
    col = RED if not good else GREEN
    if fillw > 70:
        rrect(im, (x0, y, x0 + fillw, y + 70), 35, fill=col, alpha=ba)
    lx = x0 + scale * be
    rrect(im, (lx - 4, y - 30, lx + 4, y + 100), 3, fill=AMBER, alpha=ba)
    text(im, (lx, y + 120), f"sınır %{be:.0f}", "s", 34, AMBER, ba, anchor="ma")
    text(im, (x0, y - 80), f"ACoS %{acos}", "db", 52, col, ba)
    ra = prog(t, s + 3.0) * out_alpha(t, e)
    sign = "+" if profit > 0 else "−"
    text(im, (M, 1330), f"Satış başına {sign}{abs(profit):.0f} TL", "dk", 96, col, ra)
    text(im, (M, 1450), "kâr" if good else "zarar", "db", 60, MUTED, ra)


def r2(t):
    D = 16
    im = base("GERÇEK KÂR", t, D)
    if t < 3.2:
        a = out_alpha(t, 3.2)
        text(im, (M, 520), "ACoS %20", "dk", 150, INK, prog(t, 0.2) * a)
        text(im, (M, 700), "ve zarar ediyorsun.", "db", 80, RED, prog(t, 0.6) * a)
        text(im, (M, 900), "ACoS %30", "dk", 150, INK, prog(t, 1.3) * a)
        text(im, (M, 1080), "ve kâr ediyorsun.", "db", 80, GREEN, prog(t, 1.7) * a)
        text(im, (M, 1260), "Nasıl mı?", "m", 56, MUTED, prog(t, 2.3) * a)
    elif t < 8.4:
        product(im, t, 3.2, 8.4, "Ürün A · 300 TL", 300, 105, 150, 20, False)
    elif t < 13.6:
        product(im, t, 8.4, 13.6, "Ürün B · 600 TL", 600, 180, 210, 30, True)
    else:
        a = prog(t, 13.6)
        text(im, (M, 560), wrap("Düşük ACoS kâr demek değil.", "dx", 100, CW), "dx", 100, INK, a, spacing=16)
        text(im, (M, 820), wrap("Her ürünün kendi kâr sınırı var. ACoS'u ona göre oku.", "m", 52, CW), "m", 52, MUTED, prog(t, 14.1), spacing=14)
        logo(im, (M, 1150), 70, prog(t, 14.6))
        text(im, (M, 1260), "Kâr sınırını her ürün için otomatik hesaplar.", "m", 38, MUTED, prog(t, 14.8))
        text(im, (M, 1330), "Rakamlar örnek veridir. Erken erişim profilde.", "r", 30, MUTED, prog(t, 15))
    return im


R2 = (r2, 16, [(0.2, "pop", .6), (1.3, "pop", .6), (3.2, "whoosh", .6), (5.2, "whoosh", .3), (6.2, "thud", .9),
               (8.4, "whoosh", .6), (10.4, "whoosh", .3), (11.4, "ding", .7), (13.6, "whoosh", .5)])


# ---------------- Reel 3: Yapay zekâ önerir, sen onaylarsın
def r3(t):
    D = 14
    im = base("ÜRÜN ÖNİZLEMESİ · ÖRNEK VERİ", t, D)
    if t < 2.6:
        a = out_alpha(t, 2.6)
        text(im, (M, 600), "Yapay zekâ önerir.", "dx", 104, INK, prog(t, 0.2) * a)
        text(im, (M, 740), "Kararı sen verirsin.", "dx", 104, alpha=prog(t, 0.8) * a, grad=True)
    elif t < 11.2:
        s = 2.6
        a = prog(t, s) * out_alpha(t, 11.2)
        text(im, (M, 420), "Bugünün önerileri", "db", 64, INK, a)
        rrect(im, (M, 530, W - M, 1170), 40, fill=CARD, outline=LINE, alpha=a)
        rrect(im, (M + 50, 580, M + 230, 640), 30, fill=(60, 36, 110), alpha=a)
        text(im, (M + 140, 610), "Öneri", "s", 30, VIOLET, a, anchor="mm")
        text(im, (M + 50, 680), wrap("“spor matara” teklifini %25 düşür", "db", 56, CW - 100), "db", 56, INK, a, spacing=10)
        wa = prog(t, s + 0.8) * out_alpha(t, 11.2)
        text(im, (M + 50, 840), "Neden?", "s", 36, AMBER, wa)
        text(im, (M + 50, 890), wrap("ACoS %52, bu ürünün kâr sınırı %30. Son 14 günde 38 tıklama, 1 satış.", "m", 38, CW - 100), "m", 38, MUTED, wa, spacing=10)
        # buttons
        ba = prog(t, s + 1.6) * out_alpha(t, 11.2)
        applied = t > 7.0
        rrect(im, (M + 50, 1040, M + 330, 1120), 40, fill=(36, 33, 58), alpha=ba)
        text(im, (M + 190, 1080), "Geç", "s", 38, MUTED, ba, anchor="mm")
        bc = GREEN if applied else ORANGE
        rrect(im, (W - M - 380, 1040, W - M - 50, 1120), 40, fill=bc, alpha=ba)
        text(im, (W - M - 215, 1080), "Uygulandı ✓" if applied else "Uygula", "b", 38, (15, 12, 8), ba, anchor="mm")
        # cursor
        if 4.6 < t < 8.2:
            p = ease((t - 4.6) / 2.0)
            cx = W / 2 + (W - M - 215 - W / 2) * p
            cy = 1500 + (1085 - 1500) * p
            press = 0.85 if 6.8 < t < 7.1 else 1
            L = Layer(im)
            sz = 46 * press
            L.d.polygon([(cx, cy), (cx, cy + sz), (cx + sz * .28, cy + sz * .75), (cx + sz * .62, cy + sz * .72)], fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))
            L.done(ba)
        if t > 8.4:
            ta = prog(t, 8.4) * out_alpha(t, 11.2)
            rrect(im, (M, 1250, W - M, 1370), 30, fill=(30, 50, 40), outline=GREEN, alpha=ta)
            text(im, (M + 40, 1310), "Değişiklik kaydedildi", "s", 38, INK, ta, anchor="lm")
            text(im, (W - M - 40, 1310), "Geri al", "b", 38, GREEN, ta, anchor="rm")
            text(im, (M, 1430), "Her değişiklik tek tıkla geri alınabilir.", "m", 40, MUTED, prog(t, 9.0) * out_alpha(t, 11.2))
    else:
        endcard(im, t, 11.2, "Onayın olmadan hiçbir şey değişmez.", small="Ürün önizlemesi; rakamlar örnek veridir.")
    return im


R3 = (r3, 14, [(0.2, "pop", .5), (0.8, "pop", .5), (2.6, "whoosh", .6), (3.4, "pop", .4), (6.95, "pop", .9), (7.05, "ding", .7),
               (8.4, "whoosh", .4), (11.2, "whoosh", .5)])


# ---------------- Reel 4: Haftada 15 dakikalık reklam kontrolü
STEPS4 = [("5 dk", "Arama terimi raporu", "Çok tıklanıp satış getirmeyenleri negatif ekle."),
          ("4 dk", "ACoS'u kâr sınırıyla kıyasla", "Sınırın üstündeki hedeflerde teklifi düşür."),
          ("3 dk", "Bütçesi erken bitenler", "Kârlıysa bütçeyi kademeli artır."),
          ("3 dk", "Kazananları taşı", "Satan terimleri manuel exact kampanyaya ekle.")]


def r4(t):
    D = 15
    im = base("REKLAM KONTROL RUTİNİ", t, D)
    if t < 2.6:
        a = out_alpha(t, 2.6)
        text(im, (M, 560), "Haftada", "db", 92, INK, prog(t, 0.2) * a)
        text(im, (M, 670), "15 dakika", "dk", 170, alpha=prog(t, 0.5) * a, grad=True)
        text(im, (M, 900), wrap("Amazon reklamını kontrol altında tutan rutin. Kaydet, her pazartesi aç.", "m", 52, CW), "m", 52, MUTED, prog(t, 1.1) * a, spacing=14)
    elif t < 12.6:
        s = 2.6
        e = 12.6
        mins = 0
        for i, (dk, title, desc) in enumerate(STEPS4):
            st = s + 0.3 + i * 2.2
            a = prog(t, st) * out_alpha(t, e)
            if t >= st:
                mins += int(dk.split()[0]) * clamp((t - st) / 1.6)
            y = 470 + i * 250
            rrect(im, (M, y, W - M, y + 220), 32, fill=CARD, outline=LINE, alpha=a)
            rrect(im, (M + 30, y + 30, M + 190, y + 100), 35, fill=(60, 36, 110), alpha=a)
            text(im, (M + 110, y + 65), dk, "b", 36, VIOLET, a, anchor="mm")
            text(im, (M + 220, y + 40), title, "db", 48, INK, a)
            text(im, (M + 30, y + 130), wrap(desc, "m", 36, CW - 60), "m", 36, MUTED, a, spacing=8)
        ca = prog(t, s) * out_alpha(t, e)
        text(im, (W / 2, 1520), f"{int(round(mins))} / 15 dk", "dk", 70, ORANGE, ca, anchor="ma")
    else:
        endcard(im, t, 12.6, "KarvanAI bu rutini her gece senin yerine yapar; sen sadece onaylarsın.", small="KarvanAI bağımsızdır; Amazon ile bağlantılı değildir.")
    return im


R4 = (r4, 15, [(0.5, "whoosh", .5)] + [(2.9 + i * 2.2, "pop", .7) for i in range(4)] + [(11.6, "ding", .6), (12.6, "whoosh", .5)])


# ---------------- Reel 5: Kasım indirimleri öncesi
def r5(t):
    D = 16
    im = base("KASIM İNDİRİMLERİ", t, D)
    if t < 3.0:
        a = out_alpha(t, 3.0)
        text(im, (M, 520), wrap("İndirim yaptığında kâr sınırın da düşer.", "dx", 104, CW), "dx", 104, INK, prog(t, 0.2) * a, spacing=16)
        text(im, (M, 1010), "Çoğu satıcı bunu reklamda unutur.", "m", 50, MUTED, prog(t, 1.0) * a)
    elif t < 8.4:
        s, e = 3.0, 8.4
        a = prog(t, s) * out_alpha(t, e)
        text(im, (M, 420), "Aynı ürün, aynı maliyet", "db", 64, INK, a)
        for i, (lab, price, fees, be) in enumerate([("Normal fiyat", 500, 150, 35), ("İndirimli fiyat", 400, 120, 26)]):
            ca = prog(t, s + 0.4 + i * 1.6) * out_alpha(t, e)
            y = 540 + i * 440
            rrect(im, (M, y, W - M, y + 400), 40, fill=CARD, outline=LINE if i == 0 else ORANGE, alpha=ca)
            text(im, (M + 50, y + 40), f"{lab} · {price} TL", "db", 52, INK, ca)
            text(im, (M + 50, y + 120), f"Amazon ücreti ~{fees} TL · maliyet 175 TL", "m", 38, MUTED, ca)
            text(im, (M + 50, y + 200), "Kâr sınırı", "m", 40, MUTED, ca)
            v = be if i == 0 else 35 - (35 - 26) * ease((t - s - 2.2) / 1.2)
            text(im, (M + 50, y + 250), f"%{v:.0f}", "dk", 120, AMBER if i == 0 else ORANGE, ca)
        text(im, (M, 1440), "ACoS hedefini indirimden önce güncelle.", "s", 44, INK, prog(t, s + 3.6) * out_alpha(t, e))
    elif t < 13.6:
        s, e = 8.4, 13.6
        a = prog(t, s) * out_alpha(t, e)
        text(im, (M, 420), "İndirimden önce 3 kontrol", "db", 66, INK, a)
        items = [("1", "Kâr sınırını indirimli fiyatla yeniden hesapla."),
                 ("2", "Bütçeyi sadece kârlı kampanyalarda artır."),
                 ("3", "Reklam verdiğin ürünün stoğu dönemi çıkaracak mı, kontrol et.")]
        for i, (n, s_) in enumerate(items):
            ia = prog(t, s + 0.5 + i * 1.1) * out_alpha(t, e)
            y = 560 + i * 280
            text(im, (M, y), n, "dk", 130, alpha=ia, grad=True)
            text(im, (M + 140, y + 20), wrap(s_, "s", 50, CW - 140), "s", 50, INK, ia, spacing=12)
    else:
        endcard(im, t, 13.6, "Kâr sınırını her ürün için, güncel fiyatla hesaplar.")
    return im


R5 = (r5, 16, [(0.2, "whoosh", .5), (3.0, "whoosh", .6), (3.4, "pop", .5), (5.0, "pop", .5), (5.4, "thud", .6),
               (8.4, "whoosh", .6)] + [(8.9 + i * 1.1, "pop", .7) for i in range(3)] + [(13.6, "ding", .5)])

REELS = {"r1": R1, "r2": R2, "r3": R3, "r4": R4, "r5": R5}

if __name__ == "__main__":
    for k in sys.argv[1:]:
        fn, d, cues = REELS[k]
        if "--still" in sys.argv:
            continue
        render_video(k, fn, d, cues)
