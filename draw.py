#!/usr/bin/env python3
"""news-23 b123 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.

31 stories: 3 hero scenes + 10 cards + 18 ALSO. Renders entry.png 1024x1024.
All facts come from the verified 23 Nov 2026 brief; nothing invented.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# palette
BLACK = (12, 12, 12)
PAPER = (250, 247, 238)
RED = (178, 24, 24)
DARKRED = (140, 18, 18)
GOLD = (198, 148, 28)
NAVY = (16, 32, 64)
GREEN = (28, 96, 58)
GREY = (90, 90, 90)
LGREY = (220, 218, 210)
MAPGREEN = (186, 214, 168)
MAPLINE = (140, 175, 125)
WHITE = (255, 255, 255)
CREAM = (244, 238, 220)


def wrap(draw, text, fnt, max_w):
    """Wrap text to fit max_w pixels; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def chip(draw, x, y, label, fill):
    """Small tag chip; returns right edge x."""
    f = font(SANS_B, 9)
    w = int(draw.textlength(label, font=f)) + 10
    draw.rounded_rectangle([x, y, x + w, y + 13], radius=2, fill=fill)
    draw.text((x + 5, y + 2), label, font=f, fill=WHITE)
    return x + w


def draw_kospi_scene(d, x, y, w, h):
    """Navy skyline + falling orange chart line."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    # lit windows skyline
    import random
    rnd = random.Random(23)
    bx = x + 6
    while bx < x + w - 18:
        bw = rnd.randint(16, 30)
        bh = rnd.randint(28, h - 42)
        by = y + h - bh
        d.rectangle([bx, by, bx + bw, y + h], fill=(24, 48, 88))
        for wy in range(by + 5, y + h - 5, 9):
            for wx in range(bx + 3, bx + bw - 3, 7):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
        bx += bw + 4
    # falling chart line with dots (starts right of the big -3.3% text)
    pts = []
    n = 7
    for i in range(n):
        px = x + 150 + i * (w - 174) / (n - 1)
        py = y + 46 + i * (h - 84) / (n - 1) + (5 if i % 2 else -3)
        pts.append((px, py))
    d.line(pts, fill=(255, 122, 26), width=3)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=WHITE,
                  outline=(255, 122, 26), width=2)
    d.text((x + 10, y + 8), "-3.3%", font=font(SANS_B, 30), fill=WHITE)
    # solid caption band so the caption never sits on lit windows
    d.rectangle([x, y + h - 22, x + w, y + h], fill=NAVY)
    d.text((x + 10, y + h - 19), "KOSPI 4,708.54  ·  -161 PTS",
           font=font(SANS_B, 11), fill=WHITE)


def draw_globe(d, cx, cy, r):
    """Simple wireframe globe."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 216, 178),
              outline=(240, 244, 230), width=2)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=(240, 244, 230), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(240, 244, 230), width=2)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 360,
          fill=(240, 244, 230), width=2)
    d.arc([cx - r, cy - r * 0.95, cx + r, cy + r * 0.95], 0, 360,
          fill=(240, 244, 230), width=1)


def draw_guterres_scene(d, x, y, w, h):
    """Green panel: big gold 150 + delegates text + globe."""
    d.rectangle([x, y, x + w, y + h], fill=GREEN)
    d.text((x + 14, y + 6), "150", font=font(SANS_B, 46), fill=GOLD)
    d.text((x + 14, y + 56), "DELEGATES", font=font(SANS_B, 17), fill=GOLD)
    d.text((x + 14, y + 76), "BACK A RISK", font=font(SANS_B, 17), fill=GOLD)
    d.text((x + 14, y + 96), "FRAMEWORK", font=font(SANS_B, 17), fill=GOLD)
    draw_globe(d, x + w - 62, y + h // 2, 44)


def draw_power_scene(d, x, y, w, h):
    """Asia Power Index bars."""
    d.rectangle([x, y, x + w, y + h], fill=CREAM)
    d.text((x + 10, y + 6), "NARROWEST SINCE 2018",
           font=font(SANS_B, 12), fill=BLACK)
    d.text((x + w - 78, y + 6), "GAP 5.3", font=font(SANS_B, 12), fill=RED)
    bars = [(78.9, "US", NAVY), (73.6, "CHINA", RED), (40.5, "INDIA", GOLD)]
    by = y + 30
    for val, name, col in bars:
        d.text((x + 10, by), f"{val}", font=font(SANS_B, 13), fill=BLACK)
        bw = int((w - 110) * val / 80.0)
        d.rectangle([x + 62, by + 2, x + 62 + bw, by + 18], fill=col)
        d.text((x + 68, by + 4), name, font=font(SANS_B, 11), fill=WHITE)
        by += 27


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 56], fill=BLACK)
    d.text((14, 6), "THE WORLD TODAY", font=font(SERIF_B, 40), fill=WHITE)
    d.text((W - 14 - d.textlength("MONDAY 23 NOVEMBER 2026",
           font=font(SANS_B, 17)), 18), "MONDAY 23 NOVEMBER 2026",
           font=font(SANS_B, 17), fill=GOLD)
    # ---- kicker ----
    d.rectangle([0, 56, W, 76], fill=RED)
    d.text((14, 61), "AI rout hits Asia  ·  UN chief urges AI rules  ·  "
           "US lead over China at record low  ·  Anthropic IPO $107.3B",
           font=font(SANS_B, 14), fill=WHITE)

    # ---- number strip: 2 rows x 5 cols ----
    strip = [
        ("-3.3%", "KOSPI"), ("5.3", "US-CHINA POWER GAP"),
        ("11,762", "EBOLA CASES, DRC"), ("10T won", "SEOUL STABILISATION FUND"),
        ("2%", "BILLIONAIRE TAX IN PARIS"),
        ("$450M", "SKUBAL DEAL"), ("165", "RUSSIAN MISSILES/WEEK"),
        ("12,000", "CLEARED IN MANCHESTER"), ("264 kg", "EXPLOSIVES SEIZED"),
        ("$107.3B", "ANTHROPIC IPO"),
    ]
    col_w = W // 5
    for i, (val, lab) in enumerate(strip):
        cx = (i % 5) * col_w + 12
        cy = 78 if i < 5 else 112
        d.text((cx, cy), val, font=font(SANS_B, 21), fill=BLACK)
        d.text((cx, cy + 23), lab, font=font(SANS, 9), fill=GREY)
    # ---- region bar ----
    regions = [("ASIA-PACIFIC 7", (16, 32, 64)), ("AMERICAS 8", (178, 24, 24)),
               ("MIDDLE EAST 6", (28, 96, 58)), ("EUROPE 5", (90, 60, 140)),
               ("AFRICA 3", (198, 148, 28)), ("WORLD 2", (90, 90, 90))]
    rx = 0
    seg = W // 6
    for name, col in regions:
        d.rectangle([rx, 148, rx + seg, 166], fill=col)
        tw = d.textlength(name, font=font(SANS_B, 10))
        d.text((rx + (seg - tw) / 2, 153), name, font=font(SANS_B, 10),
               fill=WHITE)
        rx += seg
    # ---- UTC strip ----
    d.rectangle([0, 166, W, 180], fill=(232, 228, 218))
    d.text((10, 169), "THE DAY IN UTC   ~00:00 Kospi dives  ·  ~05:30 "
           "Guterres opens  ·  ~09:00 Power Index  ·  ~12:00 Paris 2% tax  ·  "
           "~15:00 Kyiv missiles", font=font(SANS, 10), fill=GREY)
    d.text((W - 62, 169), "~ APPROX", font=font(SANS, 10), fill=GREY)

    # ---- heroes ----
    hx = [8, 346, 684]
    hw = 330
    sy, sh = 180, 112
    draw_kospi_scene(d, hx[0], sy, hw, sh)
    draw_guterres_scene(d, hx[1], sy, hw, sh)
    draw_power_scene(d, hx[2], sy, hw, sh)
    heroes = [
        ("AI ROUT HITS ASIA",
         "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. "
         "Samsung -3.1%, SK Hynix -2.5%.", "KOREA EXCHANGE"),
        ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         "UN chief urges global AI safety rules at the Bridgetown summit; "
         "150 back a risk framework.", "UNITED NATIONS"),
        ("US LEAD OVER CHINA AT RECORD LOW",
         "Asia Power Index 2026: US 78.9, China 73.6 - gap 5.3, narrowest "
         "since 2018. India third at 40.5.", "LOWY INSTITUTE"),
    ]
    for i, (head, body, src) in enumerate(heroes):
        x = hx[i]
        lines = wrap(d, head, font(SANS_B, 15), hw)
        ly = sy + sh + 6
        for ln in lines[:2]:
            d.text((x, ly), ln, font=font(SANS_B, 15), fill=BLACK)
            ly += 18
        blines = wrap(d, body, font(SANS, 10), hw)
        by = sy + sh + 46
        for ln in blines[:2]:
            d.text((x, by), ln, font=font(SANS, 10), fill=(40, 40, 40))
            by += 13
        d.text((x, sy + sh + 74), src, font=font(SANS, 9), fill=GREY)
        chip(d, x + hw - 62, sy + sh + 72, "REPORTED", NAVY)

    # ---- MORE OF THE DAY strip ----
    d.rectangle([0, 384, W, 402], fill=BLACK)
    d.text((10, 388), "MORE OF THE DAY  —  10 STORIES",
           font=font(SANS_B, 12), fill=WHITE)

    cards = [
        ("AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.",
         "WSJ", "REPORTED"),
        ("AMERICAS", "FBI PROBES NCIC HACK", "NCIC database hacked.",
         "AP", "REPORTED"),
        ("WHITE HOUSE", "TRUMP: IRAN STRIKES MAY RESUME",
         "May resume in New Year.", "Reuters", "REPORTED"),
        ("MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.",
         "Bloomberg", "REPORTED"),
        ("SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year, largest ever.",
         "AP", "REPORTED"),
        ("SPORT", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.",
         "ESPN", "REPORTED"),
        ("LEGAL", "STATES SUE SPACEX", "Ten states sue over AI.",
         "AP", "REPORTED"),
        ("TECH", "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.",
         "WSJ", "REPORTED"),
        ("EUROPE", "POLAND: 3 MISSILES CROSSED AIRSPACE",
         "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM"),
        ("SPACE", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.",
         "Reuters", "CLAIM"),
    ]
    cw, chh = 197, 72
    for i, (reg, head, body, src, tag) in enumerate(cards):
        row, col = divmod(i, 5)
        x = 8 + col * (cw + 5)
        y = 406 + row * (chh + 4)
        d.rectangle([x, y, x + cw, y + chh], outline=LGREY, width=1)
        d.text((x + 5, y + 4), reg, font=font(SANS_B, 8), fill=RED)
        d.text((x + cw - 14, y + 4), str(i + 1), font=font(SANS_B, 9),
               fill=RED)
        hlines = wrap(d, head, font(SANS_B, 11), cw - 10)
        hy = y + 16
        for ln in hlines[:2]:
            d.text((x + 5, hy), ln, font=font(SANS_B, 11), fill=BLACK)
            hy += 13
        d.text((x + 5, y + 44), body, font=font(SANS, 9), fill=(40, 40, 40))
        d.text((x + 5, y + 58), src, font=font(SANS, 8), fill=GREY)
        chip(d, x + cw - 62, y + 56, tag, NAVY if tag == "REPORTED" else RED)

    # ---- WHERE IT HAPPENED strip ----
    d.rectangle([0, 556, W, 574], fill=BLACK)
    d.text((10, 560), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=WHITE)

    # ---- map blobs ----
    map_y0, map_y1 = 578, 736
    # Americas
    d.polygon([(14, 600), (96, 584), (118, 620), (104, 668), (70, 700),
               (40, 726), (18, 700), (10, 650)], fill=MAPGREEN,
              outline=MAPLINE)
    # Europe / Africa
    d.polygon([(128, 590), (206, 584), (228, 620), (214, 668), (196, 720),
               (168, 732), (140, 700), (126, 640)], fill=MAPGREEN,
              outline=MAPLINE)
    # Asia
    d.polygon([(236, 592), (318, 586), (326, 630), (306, 676), (272, 700),
               (244, 676), (232, 634)], fill=MAPGREEN, outline=MAPLINE)
    pins = [
        (1, 292, 612), (2, 52, 716), (3, 276, 640), (4, 40, 640),
        (5, 74, 604), (6, 192, 606), (7, 152, 622), (8, 142, 602),
        (9, 202, 626), (10, 165, 600), (11, 206, 660), (12, 200, 686),
        (13, 176, 720),
    ]
    for num, px, py in pins:
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE,
                  width=2)
        t = str(num)
        tw = d.textlength(t, font=font(SANS_B, 9))
        d.text((px - tw / 2, py - 6), t, font=font(SANS_B, 9), fill=WHITE)
    legend = [
        "Pins 1-13:  1 Seoul · 2 Bridgetown · 3 Beijing",
        "4 Washington · 5 New York · 6 Kyiv · 7 Paris",
        "8 London · 9 Warsaw · 10 Manchester · 11 Beirut",
        "12 Gaza · 13 Khartoum",
    ]
    ly = 742
    for ln in legend:
        d.text((10, ly), ln, font=font(SANS, 9), fill=GREY)
        ly += 11

    # ---- ALSO list ----
    d.text((344, 580), "ALSO ON MONDAY", font=font(SANS_B, 12), fill=BLACK)
    also = [
        (14, "Paris: 100+ back 2% billionaire tax", False),
        (15, "Manchester: 12,000 cleared", False),
        (16, "Zelenskyy: 165 missiles in a week", False),
        (17, "COP31: the day after Antalya pact rejected", False),
        (18, "Israel unity talks resume", False),
        (19, "Gaza: two killed in Israeli strike", False),
        (20, "West Bank settler attacks", False),
        (21, "Iran war: no deal in sight", False),
        (22, "Lebanon seizes 264 kg explosives", False),
        (23, "Bahrain: strike hits plant, 2 hurt", False),
        (24, "Benghazi: UN demands probe [CLAIM]", True),
        (25, "Sudan: defences down drones [CLAIM]", True),
        (26, "DRC: fighting traps Ebola teams", False),
        (27, "Bangladesh: Hasina jailed if she returns", False),
        (28, "Seoul minister quits in exam row", False),
        (29, "SK Telecom -7.3% as hype cools", False),
        (30, "China eases margin rules", False),
        (31, "Seoul readies 10T-won fund", False),
    ]
    ay = 600
    for i, (num, txt, claim) in enumerate(also):
        col = 0 if i < 9 else 1
        row = i % 9
        ax = 344 if col == 0 else 690
        ayy = 600 + row * 20
        d.text((ax, ayy), f"{num}. {txt}", font=font(SANS, 10),
               fill=RED if claim else BLACK)

    # ---- DATE CHECK red box ----
    d.rectangle([8, 792, W - 8, 884], outline=RED, width=2)
    d.text((16, 798), "DATE CHECK  —  READ 23 NOV 2026, 23:59 UTC  ·  "
           "STORIES DATED 23 NOV ONLY", font=font(SANS_B, 12), fill=RED)
    d.text((16, 820), "LEFT OUT — NOT 23 NOV:  Dems reach 258 (22 Nov)  ·  "
           "Sparta II fire (22 Nov)  ·  El Chapo Isidro captured (22 Nov)",
           font=font(SANS, 10), fill=BLACK)
    d.text((16, 836), "EU–Indonesia pact (21 Nov)  ·  Nigeria boat (21 Nov)  ·  "
           "ICJ Myanmar ruling (19 Nov)", font=font(SANS, 10), fill=BLACK)
    d.text((16, 858), "NOT YET — Dymer search continues (14 missing)  ·  "
           "4 House races uncalled  ·  COP32 venue not set  ·  WHO evacuating "
           "trapped Ebola staff", font=font(SANS, 10), fill=BLACK)

    # ---- footer ----
    d.text((10, 892), "Sources: Reuters · AP · Bloomberg · AFP · Yonhap · BBC · "
           "WSJ · ESPN · Lowy Institute (Asia Power Index 2026).",
           font=font(SANS, 9), fill=GREY)
    d.text((10, 906), "CHIPS: REPORTED = confirmed by wires · CLAIM = one "
           "side's claim, not independently confirmed · ONGOING = still "
           "developing.", font=font(SANS, 9), fill=GREY)
    d.text((10, 920), "All times UTC. Figures as reported 23 Nov 2026. Scenes "
           "are drawn illustrations, not photographs.",
           font=font(SANS, 9), fill=GREY)
    gold = "THE WORLD TODAY  ·  Monday 23 November 2026  ·  31 stories  ·  6 regions"
    tw = d.textlength(gold, font=font(SANS_B, 12))
    d.text(((W - tw) / 2, 946), gold, font=font(SANS_B, 12), fill=GOLD)

    img.save(OUT, "PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
