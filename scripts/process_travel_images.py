#!/usr/bin/env python3
"""清除旅行照片元数据，修正方向、缩放并输出适合网页的 WebP。"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageOps


SUPPORTED_SUFFIXES = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}


def iter_images(inputs: list[Path]) -> list[tuple[Path, Path]]:
    images: list[tuple[Path, Path]] = []
    for item in inputs:
        item = item.expanduser().resolve()
        if item.is_file() and item.suffix.lower() in SUPPORTED_SUFFIXES:
            images.append((item, Path(item.stem)))
        elif item.is_dir():
            for image in sorted(item.rglob("*")):
                if image.is_file() and image.suffix.lower() in SUPPORTED_SUFFIXES:
                    images.append((image, image.relative_to(item).with_suffix("")))
        else:
            print(f"跳过不支持或不存在的路径：{item}")
    return images


def process_image(source: Path, destination: Path, max_edge: int, quality: int) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened)
        image.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)
        if image.mode not in {"RGB", "RGBA"}:
            image = image.convert("RGBA" if "transparency" in image.info else "RGB")
        image.save(
            destination,
            format="WEBP",
            quality=quality,
            method=6,
            exif=b"",
            icc_profile=None,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path, help="一个或多个图片文件/目录")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs/assets/images/footprints/processed"),
        help="WebP 输出目录",
    )
    parser.add_argument("--max-edge", type=int, default=1920, help="最长边像素，默认 1920")
    parser.add_argument("--quality", type=int, default=84, choices=range(1, 101), metavar="1-100")
    args = parser.parse_args()

    if args.max_edge < 320:
        parser.error("--max-edge 不能小于 320")

    images = iter_images(args.inputs)
    if not images:
        print("没有找到可处理的图片。")
        return 1

    output_dir = args.output_dir.expanduser().resolve()
    for source, relative in images:
        destination = output_dir / relative.with_suffix(".webp")
        process_image(source, destination, args.max_edge, args.quality)
        before = source.stat().st_size
        after = destination.stat().st_size
        reduction = 100 * (1 - after / before) if before else 0
        print(f"{source.name} -> {destination}（减少 {reduction:.1f}%）")

    print(f"处理完成：{len(images)} 张；原始文件未修改，输出不包含 EXIF 元数据。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
