#!/usr/bin/env python3
"""Draw the front page for Thursday 19 November 2026 as a 1024x1024 PNG.

Every story was verified against live reporting on the morning of
19 November 2026 (Yonhap, Nikkei, Reuters, Sotheby's, NASA, JMA).
Run: python3 build_frontpage.py  -> writes entry.png in this directory.
Deterministic: same bytes on every run (fixed layout, fixed fonts,
no timestamps, fixed PNG compression).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (20, 20, 20)
GREY = (90, 86, 78)
RED = (163, 18, 26)
NAVY = (31, 58, 95)
GOLD = (176, 141, 60)
LIGHT = (232, 226, 212)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_DIR = "/usr/share/fonts/truetype/liberation"


def font(name, size, directory=FONT_DIR):
    return ImageFont.truetype(os.path.join(directory, name), size)


SERIF_B = lambda s: font("LiberationSerif-Bold.ttf", s, SERIF_DIR)
SERIF = lambda s: font("LiberationSerif-Regular.ttf", s, SERIF_DIR)
SERIF_I = lambda s: font("LiberationSerif-Italic.ttf", s, SERIF_DIR)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit in width."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def tracked(draw, xy, text, fnt, fill, spacing=1):
    """Draw text with extra letter spacing (for kickers)."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + spacing


def para(draw, x, y, width, text, fnt, fill=INK, leading=None):
    """Draw a wrapped paragraph; returns the y after the last line."""
    if leading is None:
        leading = int(fnt.size * 1.32)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def headline(draw, x, y, width, text, fnt, fill=INK, leading=None):
    """Draw a wrapped headline; returns the y after the last line."""
    if leading is None:
        leading = int(fnt.size * 1.08)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x, y, width, weight=1, fill=INK):
    draw.rectangle([x, y, x + width, y + weight - 1], fill=fill)


def draw_globe(draw, cx, cy, r):
    """Stylised globe: circle, meridians, latitude lines, land blobs."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=4)
    for k in (-2, -1, 0, 1, 2):
        rx = int(r * abs(k) / 3.2)
        if rx < 3:
            draw.line([cx, cy - r, cx, cy + r], fill=NAVY, width=2)
        else:
            draw.ellipse([cx - rx, cy - r, cx + rx, cy + r],
                         outline=NAVY, width=2)
    for dy in (-int(r * 0.55), 0, int(r * 0.55)):
        w = int((r * r - dy * dy) ** 0.5)
        draw.arc([cx - w, cy + dy - 8, cx + w, cy + dy + 8],
                 start=180, end=360, fill=NAVY, width=2)
        draw.arc([cx - w, cy + dy - 8, cx + w, cy + dy + 8],
                 start=0, end=180, fill=NAVY, width=2)
    # land blobs
    draw.ellipse([cx - r + 18, cy - r + 26, cx - r + 62, cy - r + 58],
                 fill=(196, 214, 176))
    draw.ellipse([cx + 6, cy + 8, cx + 52, cy + 44], fill=(196, 214, 176))
    draw.ellipse([cx - 52, cy + 30, cx - 8, cy + 62], fill=(196, 214, 176))


def draw_flag(draw, x, y, w, h, kind):
    """Tiny stylised flag: us / cn / ru."""
    if kind == "us":
        for i in range(7):
            draw.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                           fill=(178, 34, 52) if i % 2 == 0 else PAPER)
        draw.rectangle([x, y, x + int(w * 0.42), y + h // 2], fill=NAVY)
        for r in range(3):
            for c in range(4):
                draw.ellipse([x + 4 + c * 9, y + 4 + r * 7,
                              x + 8 + c * 9, y + 8 + r * 7], fill=PAPER)
    elif kind == "cn":
        draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
        draw.ellipse([x + 5, y + 5, x + 15, y + 15], fill=(255, 222, 0))
        for sx, sy in ((24, 6), (28, 12), (28, 19), (24, 24)):
            draw.ellipse([x + sx, y + sy, x + sx + 5, y + sy + 5],
                         fill=(255, 222, 0))
    elif kind == "ru":
        draw.rectangle([x, y, x + w, y + h // 3], fill=(245, 245, 245))
        draw.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(0, 57, 166))
        draw.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(213, 0, 50))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 36                      # side margin
    CW = W - 2 * MX              # content width

    # ---- top info bar ----
    y = 26
    tracked(d, (MX, y), "THURSDAY 19 NOVEMBER 2026", SANS_B(13), INK, 1)
    right = "ONE DAY  ·  ONE PAGE"
    tracked(d, (W - MX - d.textlength(right, font=SANS_B(13)) - 18, y),
            right, SANS_B(13), INK, 1)
    rule(d, MX, 48, CW, 2)
    rule(d, MX, 52, CW, 1)

    # ---- masthead ----
    title = "THE WORLD TODAY"
    tf = SERIF_B(68)
    d.text(((W - d.textlength(title, font=tf)) / 2, 60), title,
           font=tf, fill=INK)
    sub = "The world's news of Thursday 19 November 2026, summed up in a single page"
    sf = SERIF_I(17)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 138), sub,
           font=sf, fill=GREY)
    rule(d, MX, 168, CW, 3)
    rule(d, MX, 173, CW, 1)

    # ---- lead story: Shenzhen trilateral ----
    y = 190
    tracked(d, (MX, y), "SHENZHEN  ·  APEC  ·  DIPLOMACY", SANS_B(14), RED, 2)
    y = headline(d, MX, y + 26, 620,
                 "XI, TRUMP AND PUTIN MEET IN FIRST-EVER TRILATERAL SUMMIT",
                 SERIF_B(41), leading=46)
    y = para(d, MX, y + 12, 620,
             "The three leaders sit down in Shenzhen to talk nuclear arms, "
             "Ukraine and Iran \u2014 the first meeting of its kind.",
             SERIF_I(19), fill=INK, leading=26)
    y = para(d, MX, y + 10, 620,
             "The summit, on the sidelines of the APEC leaders' meeting, "
             "is set for 2.30pm local time and expected to last about an "
             "hour. A separate Trump\u2013Xi summit comes first. Putin is "
             "attending an APEC summit in person for the first time in "
             "nine years.",
             SERIF(15), fill=GREY, leading=21)
    # globe + flags illustration, right of the lead
    draw_globe(d, 838, 268, 78)
    fx, fy, fw, fh = 700, 372, 88, 56
    for i, (kind, label) in enumerate((("us", "U.S."), ("cn", "CHINA"),
                                       ("ru", "RUSSIA"))):
        x = fx + i * 100
        draw_flag(d, x, fy, fw, fh, kind)
        lab = SANS_B(13)
        d.text((x + (fw - d.textlength(label, font=lab)) / 2, fy + fh + 8),
               label, font=lab, fill=INK)
    rule(d, MX, 486, CW, 2)

    # ---- row 2: GTA VI | Van Gogh ----
    y = 506
    col_w = (CW - 24) // 2
    # GTA VI, left
    x = MX
    tracked(d, (x, y), "GAMES  ·  CULTURE", SANS_B(13), RED, 2)
    y2 = headline(d, x, y + 24, col_w, "GTA VI IS HERE \u2014 AFTER 13 YEARS",
                  SERIF_B(26), leading=30)
    y2 = para(d, x, y2 + 8, col_w,
              "Rockstar's epic launches at midnight around the world, New "
              "Zealand first in. Critics score it 99 on Metacritic; "
              "pre-orders top 15 million copies.",
              SERIF(14.5), fill=GREY, leading=20)
    # small skyline thumb under GTA text
    bx, by, bw, bh = x, 622, col_w, 62
    d.rectangle([bx, by, bx + bw, by + bh], fill=NAVY)
    for sx, sw, sh in ((8, 26, 34), (42, 18, 48), (66, 30, 26), (104, 22, 44),
                       (134, 16, 30), (158, 34, 52), (200, 20, 36),
                       (228, 28, 46), (264, 18, 28), (290, 30, 40),
                       (330, 22, 50), (362, 26, 32), (396, 20, 44)):
        d.rectangle([bx + sx, by + bh - sh, bx + sx + sw, by + bh],
                    fill=(246, 241, 231))
    d.ellipse([bx + bw - 52, by + 8, bx + bw - 12, by + 48], fill=(255, 190, 60))
    # Van Gogh, right
    x = MX + col_w + 24
    tracked(d, (x, y), "ART  ·  AUCTION", SANS_B(13), RED, 2)
    y2 = headline(d, x, y + 24, col_w,
                  "VAN GOGH SELLS FOR $190.4M \u2014 A RECORD", SERIF_B(26),
                  leading=30)
    y2 = para(d, x, y2 + 8, col_w,
              "\u201cCh\u00e2taigniers en fleurs\u201d (1890) smashes the "
              "artist's auction record at Sotheby's New York, a day after a "
              "Nazi-era ownership dispute was settled.",
              SERIF(14.5), fill=GREY, leading=20)
    # small framed blossom thumb under Van Gogh text
    bx, by, bw, bh = x, 622, col_w, 62
    d.rectangle([bx - 3, by - 3, bx + bw + 3, by + bh + 3], fill=GOLD)
    d.rectangle([bx, by, bx + bw, by + bh], fill=(122, 158, 196))
    for cx, cy, r, col in ((60, 30, 12, (240, 230, 200)),
                           (110, 44, 10, (255, 255, 255)),
                           (160, 26, 13, (240, 230, 200)),
                           (215, 42, 11, (255, 244, 214)),
                           (270, 28, 12, (255, 255, 255)),
                           (325, 44, 10, (240, 230, 200)),
                           (380, 30, 12, (255, 244, 214)),
                           (430, 44, 10, (255, 255, 255))):
        d.ellipse([bx + cx - r, by + cy - r, bx + cx + r, by + cy + r],
                  fill=col)
    d.rectangle([bx, by + 52, bx + bw, by + bh], fill=(74, 110, 62))
    rule(d, MX, 700, CW, 2)

    # ---- row 3: Hormuz | ICJ | Voyager ----
    y = 720
    col_w = (CW - 48) // 3
    stories = [
        ("MIDDLE EAST", "IRAN SAYS THREE TANKERS HIT MINES",
         "Tehran claims three tankers caught fire east of the Strait of "
         "Hormuz; Reuters could not verify it. An ADNOC vessel was struck, "
         "one crew member missing, 11 hurt."),
        ("THE HAGUE  ·  LAW", "WORLD COURT RULES ON ROHINGYA TODAY",
         "The ICJ delivers its verdict on whether Myanmar committed "
         "genocide against the Rohingya \u2014 seven years after The Gambia "
         "brought the case."),
        ("SPACE", "VOYAGER 1, ONE LIGHT-DAY AWAY",
         "NASA's 1977 probe passes 25.9 billion km from Earth. A radio "
         "message now takes a full day to reach it \u2014 and a day to come "
         "back."),
    ]
    for i, (kick, head, body) in enumerate(stories):
        x = MX + i * (col_w + 24)
        tracked(d, (x, y), kick, SANS_B(12), RED, 1)
        y2 = headline(d, x, y + 22, col_w, head, SERIF_B(20), leading=23)
        y2 = para(d, x, y2 + 7, col_w, body, SERIF(13.5), fill=GREY,
                  leading=18)
        if i < 2:
            d.line([x + col_w + 12, y, x + col_w + 12, 872], fill=LIGHT,
                   width=1)
    rule(d, MX, 890, CW, 2)

    # ---- bottom band: Kumamoto quake ----
    y = 908
    tracked(d, (MX, y), "JAPAN  ·  2.22 AM", SANS_B(13), RED, 2)
    y = headline(d, MX, y + 24, CW, "M5.7 QUAKE JOLTS KUMAMOTO", SERIF_B(24),
                 leading=28)
    y = para(d, MX, y + 6, CW,
             "Minamata orders 22,000 people to evacuate; no tsunami. An "
             "aftershock of July's M7.1.",
             SERIF(14.5), fill=GREY, leading=20)

    # ---- footer ----
    rule(d, MX, 988, CW, 1)
    foot = ("THE WORLD TODAY  ·  19 NOVEMBER 2026  ·  Sources: Yonhap, "
            "Nikkei, Reuters, Sotheby's, NASA, Japan Meteorological Agency")
    ff = SANS(11)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 998), foot, font=ff,
           fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, "PNG", compress_level=6)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
