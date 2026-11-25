#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成公众号横版封面：九部经典口径，站点纸墨配色。"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 900, 383
PAPER = (247, 244, 238)
INK = (27, 25, 23)
MUTED = (107, 97, 82)
ACCENT = (140, 58, 46)
RING = (196, 168, 148)
LINE = (220, 211, 196)

FD = "/usr/share/fonts/opentype/noto"
SERIF_B = f"{FD}/NotoSerifCJK-Bold.ttc"
SERIF_M = f"{FD}/NotoSerifCJK-SemiBold.ttc"
SANS_R = f"{FD}/NotoSansCJK-Regular.ttc"
SANS_M = f"{FD}/NotoSansCJK-Medium.ttc"

def font(path, size, idx=0):
    return ImageFont.truetype(path, size, index=idx)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# 左侧竖细分隔线
d.line([(70, 78), (70, H - 78)], fill=LINE, width=1)

# 顶部小字：系列名
d.text((96, 66), "润泽说 · 道可道", font=font(SANS_M, 26), fill=MUTED)
# 副标题：九部
d.text((96, 112), "经典六部 · 字学甲骨文 · 蒙学千字文 / 三字经",
       font=font(SANS_R, 19), fill=MUTED)

# 主标题（两行）
d.text((94, 168), "把字放回源头", font=font(SERIF_B, 58), fill=INK)
d.text((94, 244), "重读九部经典", font=font(SERIF_B, 58), fill=INK)

# 底部注脚
d.text((96, 326), "以「佛说 A，即非 A，是名 A」为标尺的逐字重解",
       font=font(SERIF_M, 20), fill=ACCENT)

# 右侧开环圆 + 环内字
cx, cy, R = 690, 192, 108
d.arc([cx - R, cy - R, cx + R, cy + R], start=-40, end=300, fill=RING, width=10)
# 环内字
f_center = font(SERIF_B, 40)
txt = "道可道"
bb = d.textbbox((0, 0), txt, font=f_center)
tw, th = bb[2] - bb[0], bb[3] - bb[1]
d.text((cx - tw / 2 - bb[0], cy - th / 2 - bb[1]), txt, font=f_center, fill=RING)

out = "docs/assets/cover-series-zh.png"
os.makedirs(os.path.dirname(out), exist_ok=True)
img.save(out, optimize=True)
print("saved", out, img.size, os.path.getsize(out), "bytes")
