#!/usr/bin/env python3
"""쿠팡 이미지 규칙 검사기.

CLAUDE.md 의 파일명·규격 규칙을 자동으로 확인한다.
사용법: python3 scripts/check_images.py [파일 또는 폴더 ...]
  인자가 없으면 coupang/ 전체를 검사한다.
문제가 하나라도 있으면 종료 코드 1.
"""
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MAX_KB = 500
PRODUCT = re.compile(r"^[A-Z]+\d+-C\d+(-v\d+)?\.jpg$")  # YL134-C4.jpg
ALLOWED_NAME = re.compile(r"^[A-Za-z0-9_-]+(\.[a-z]+)$")
SKIP = {"_connection-test.jpg"}


def check(path: Path) -> list[str]:
    errs = []
    name = path.name
    if not ALLOWED_NAME.match(name):
        errs.append("파일명에 영문·숫자·하이픈 외 문자가 있음")
    kb = path.stat().st_size / 1024
    if kb > MAX_KB:
        errs.append(f"용량 {kb:.0f}KB (최대 {MAX_KB}KB)")
    try:
        with Image.open(path) as im:
            size, mode = im.size, im.mode
    except Exception as e:  # 이미지가 아니거나 깨짐
        return errs + [f"이미지를 열 수 없음: {e}"]

    if PRODUCT.match(name):
        if size != (1000, 1000):
            errs.append(f"상품컷은 1000x1000 이어야 함 (현재 {size[0]}x{size[1]})")
        if mode != "RGB":
            errs.append(f"상품컷은 RGB 여야 함 (현재 {mode})")
    elif path.suffix == ".png":
        if size[0] != 780:
            errs.append(f"안내 이미지는 가로 780px 이어야 함 (현재 {size[0]}px)")
    else:
        errs.append("규칙에 맞지 않는 이름 (상품컷: 모델-C번호.jpg / 안내: 이름.png)")
    return errs


def main(args: list[str]) -> int:
    targets = [Path(a) for a in args] or [ROOT / "coupang"]
    files = []
    for t in targets:
        files += sorted(p for p in t.rglob("*") if p.is_file()) if t.is_dir() else [t]
    bad = 0
    for f in files:
        if f.name in SKIP:
            continue
        errs = check(f)
        if errs:
            bad += 1
            print(f"✗ {f.relative_to(ROOT) if f.is_absolute() else f}")
            for e in errs:
                print(f"    - {e}")
    print(f"\n검사 {len(files)}개 중 문제 {bad}개" if bad else f"✓ {len(files)}개 모두 규칙에 맞음")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
