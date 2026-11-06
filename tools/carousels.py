from lib import *

W, H = 1080, 1350
BGC = background(W, H)
M = 90
CW = W - 2 * M


def slide(series, i, n):
    im = BGC.copy()
    logo(im, (M, 80), 36)
    text(im, (W - M, 88), f"{series} · {i}/{n}", "s", 24, MUTED, anchor="ra")
    if i < n:
        text(im, (W - M, H - 100), "Kaydır →", "s", 28, MUTED, anchor="ra")
    return im


def cover(series, n, kicker, title, sub):
    im = slide(series, 1, n)
    text(im, (M, 330), kicker, "s", 34, ORANGE)
    text(im, (M, 400), wrap(title, "dx", 104, CW), "dx", 104, INK, spacing=18)
    text(im, (M, 900), wrap(sub, "m", 44, CW), "m", 44, MUTED, spacing=12)
    return im


def step(series, i, n, num, title, body, note=None, note_col=AMBER):
    im = slide(series, i, n)
    text(im, (M, 230), num, "dk", 190, grad=True)
    text(im, (M, 480), wrap(title, "dx", 76, CW), "dx", 76, INK, spacing=14)
    tb = wrap(title, "dx", 76, CW).count("\n")
    y = 600 + tb * 90
    text(im, (M, y), wrap(body, "m", 42, CW), "m", 42, MUTED, spacing=14)
    if note:
        bh = wrap(note, "s", 38, CW - 80).count("\n") + 1
        rrect(im, (M, 1000, W - M, 1000 + 70 + bh * 50), 30, fill=CARD, outline=note_col)
        text(im, (M + 40, 1035), wrap(note, "s", 38, CW - 80), "s", 38, note_col, spacing=12)
    return im


def cta(series, n, title, body, small="KarvanAI bağımsız bir hizmet sağlayıcıdır; Amazon ile bağlantılı değildir."):
    im = slide(series, n, n)
    logo(im, (W / 2, 330), 100, anchor="m")
    text(im, (W / 2, 500), wrap(title, "db", 60, CW), "db", 60, INK, anchor="ma", align="center", spacing=14)
    text(im, (W / 2, 700), wrap(body, "m", 40, CW), "m", 40, MUTED, anchor="ma", align="center", spacing=12)
    rrect(im, (M + 110, 930, W - M - 110, 1040), 55, fill=ORANGE)
    text(im, (W / 2, 985), "Profildeki linkten katıl", "b", 40, (20, 12, 4), anchor="mm")
    text(im, (W / 2, 1120), wrap(small, "r", 26, CW), "r", 26, MUTED, anchor="ma", align="center")
    return im


def save(name, slides):
    os.makedirs(f"out/{name}", exist_ok=True)
    for k, im in enumerate(slides, 1):
        im.save(f"out/{name}/{name}-{k:02d}.png", optimize=True)
    print(name, len(slides))


# C1 — Arama terimi raporunu 5 dakikada oku
S = "ARAMA TERİMİ RAPORU"
n = 7
save("c1", [
    cover(S, n, "5 DAKİKALIK REHBER", "Arama terimi raporunu böyle oku.", "Boşa giden reklam parası çoğu zaman bu raporda saklı. 5 adımda bul, kes, büyüt."),
    step(S, 2, n, "1", "Raporu indir", "Amazon Ads konsolu → Ölçüm ve raporlama → Sponsored ads raporları → Sponsored Products → Arama terimi.", "En az son 30 günü seç; az veriyle karar verme."),
    step(S, 3, n, "2", "Harcamaya göre sırala", "Büyükten küçüğe. Önce en çok harcayan terimlere bak; en büyük sızıntı genelde en üsttedir."),
    step(S, 4, n, "3", "Satış getirmeyenleri işaretle", "Çok tıklanmış ama hiç sipariş getirmemiş terimler ilk adaylar. Eşik ürünün dönüşüm oranına göre değişir.", "Örnek: dönüşüm oranın %10 ise, 20–30 tıklamada hâlâ 0 sipariş varsa dikkat."),
    step(S, 5, n, "4", "Alakasız olanı negatif ekle", "Ürününle ilgisi olmayan ya da yanlış niyetli aramaları exact negatif olarak ekle. Alakalı ama pahalı olanda önce teklifi düşür.", "Alakalı terimi hemen kesme; teklif ayarı çoğu zaman yeter.", GREEN),
    step(S, 6, n, "5", "Satanı exact'e taşı", "Otomatik ya da broad kampanyada satış getiren terimi manuel exact kampanyaya ekle, eski kampanyada negatif yap.", "Haftada bir tekrarla. 15 dakika yeter."),
    cta(S, n, "Bu raporu her gece senin yerine okuyan asistan.", "KarvanAI boşa giden terimleri bulur, gerekçesiyle önerir; sen onaylarsın."),
])

# C2 — En sık 5 hata
S = "EN SIK 5 HATA"
n = 7
save("c2", [
    cover(S, n, "AMAZON REKLAMI", "Reklam bütçesini sessizce eriten 5 hata.", "Hangisini yapıyorsun? Kaydır, sonra yorumlara numarasını yaz."),
    step(S, 2, n, "1", "Sadece ACoS'a bakmak", "ACoS reklamın verimini gösterir, kârını değil. Aynı ACoS bir üründe kâr, diğerinde zarar olabilir.", "Her ürünün kâr sınırını (başabaş ACoS) hesapla."),
    step(S, 3, n, "2", "Negatif kelime eklememek", "Alakasız aramalar her gün tıklama alır. Arama terimi raporunu açmayan satıcı bunu hiç görmez.", "Haftada bir rapora bak, alakasızı exact negatif ekle."),
    step(S, 4, n, "3", "Kampanyaları birbirine rakip yapmak", "Aynı terim hem otomatik hem manuel kampanyada açıksa kendi teklifinle yarışırsın.", "Manuele taşıdığın terimi otomatikte negatif yap."),
    step(S, 5, n, "4", "Az veriyle teklif değiştirmek", "Birkaç tıklama, sonuç hakkında çok az şey söyler. Erken kesilen terim belki kazanan olacaktı.", "Karar için en az 2 haftalık veriye bak."),
    step(S, 6, n, "5", "Kârlı kampanyayı bütçesiz bırakmak", "Bütçe öğlen bitiyorsa günün geri kalanında satış rakibe gider.", "ACoS kâr sınırının altındaysa bütçeyi kademeli artır, 3–5 gün izle.", GREEN),
    cta(S, n, "Beşini de her gün kontrol eden asistan.", "KarvanAI hataları bulur, ne yapman gerektiğini Türkçe önerir. Onayın olmadan hiçbir şey değişmez."),
])

# C3 — Kapalı beta
S = "KAPALI BETA"
n = 6
save("c3", [
    cover(S, n, "KAPALI BETA", "Kapalı beta başlıyor. Kimleri arıyoruz?", "İlk grubu küçük tutuyoruz, böylece her satıcıyla birebir çalışabiliyoruz."),
    step(S, 2, n, "1", "Kimler için?", "amazon.com.tr, Avrupa ya da ABD'de satış yapan ve Sponsored Products reklamını kendisi yöneten satıcılar.", "Ayda 10.000 TL ve üzeri reklam harcıyorsan tam aradığımız kişisin."),
    step(S, 3, n, "2", "Ne alırsın?", "Kapalı beta boyunca ücretsiz erişim, kurulumda birebir destek ve ücretli sürüme geçince kurucu üye fiyat kilidi.", None),
    step(S, 4, n, "3", "Bizden ne istiyoruz?", "Haftada 15 dakikalık geri bildirim. Neyin işe yaradığını, neyin yaramadığını açıkça söylemen.", None),
    step(S, 5, n, "4", "Kontrol sende", "Önerileri sen onaylamadan hiçbir kampanya, teklif ya da bütçe değişmez. Her değişiklik geri alınabilir.", "Davetler küçük gruplar hâlinde gönderilir.", GREEN),
    cta(S, n, "Bekleme listesine katıl, davetini al.", "Kontenjan sınırlı. Kayıt 30 saniye sürer."),
])
