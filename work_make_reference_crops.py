from pathlib import Path
from PIL import Image

SRC = Path("/private/var/folders/m6/54dvn2xj5ys2qr3t7dnw8v280000gn/T/codex-clipboard-354ac278-c40a-4272-9c7e-48fc303fd1ef.png")
OUT = Path("/Users/henryhuang/Developer/football/assets/reference_crops")
OUT.mkdir(parents=True, exist_ok=True)

img = Image.open(SRC).convert("RGBA")


def remove_white(im, threshold=242):
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r >= threshold and g >= threshold and b >= threshold:
                px[x, y] = (255, 255, 255, 0)
            elif r >= 225 and g >= 225 and b >= 225:
                na = int(a * (255 - min(r, g, b)) / 35)
                px[x, y] = (r, g, b, max(0, min(a, na)))
    return im


def trim(im, pad=18):
    box = im.getbbox()
    if not box:
        return im
    l, t, r, b = box
    l = max(0, l - pad)
    t = max(0, t - pad)
    r = min(im.width, r + pad)
    b = min(im.height, b + pad)
    return im.crop((l, t, r, b))


def save(name, box, size=512, pad=28):
    crop = remove_white(img.crop(box))
    crop = trim(crop, pad=pad)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    scale = min((size - 36) / crop.width, (size - 36) / crop.height)
    nw, nh = int(crop.width * scale), int(crop.height * scale)
    crop = crop.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas.alpha_composite(crop, ((size - nw) // 2, (size - nh) // 2))
    canvas.save(OUT / name)


crops = {
    "shooter_front.png": (255, 150, 430, 455),
    "shooter_side.png": (455, 150, 600, 455),
    "shooter_back.png": (630, 150, 785, 455),
    "shooter_expression_focused.png": (835, 140, 950, 260),
    "shooter_expression_confident.png": (975, 140, 1090, 260),
    "shooter_expression_shouting.png": (1115, 140, 1235, 260),
    "shooter_pose_slide.png": (790, 310, 940, 465),
    "shooter_pose_dribble.png": (970, 310, 1095, 465),
    "shooter_pose_kick.png": (1110, 310, 1245, 465),
    "shooter_avatar.png": (900, 845, 1025, 970),
    "goalkeeper_front.png": (250, 535, 430, 800),
    "goalkeeper_side.png": (455, 535, 600, 800),
    "goalkeeper_back.png": (625, 535, 790, 800),
    "goalkeeper_expression_alert.png": (835, 535, 950, 650),
    "goalkeeper_expression_focused.png": (975, 535, 1090, 650),
    "goalkeeper_expression_shouting.png": (1115, 535, 1235, 650),
    "goalkeeper_pose_dive_left.png": (790, 700, 930, 805),
    "goalkeeper_pose_ready.png": (970, 700, 1095, 805),
    "goalkeeper_pose_dive_right.png": (1120, 690, 1245, 805),
    "goalkeeper_avatar.png": (1010, 845, 1135, 970),
}

for name, box in crops.items():
    save(name, box)

(OUT / "SOURCE.txt").write_text(
    "Cropped from the supplied high-quality model sheet reference image, with white background removed.\n",
    encoding="utf-8",
)
print(OUT)
