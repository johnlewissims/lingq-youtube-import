#!/usr/bin/env python3
import argparse
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_OUTPUT_DIR = Path.cwd() / "lingq-imports"


def find_yt_dlp() -> str:
    candidate = shutil.which("yt-dlp")
    if candidate:
        return candidate
    try:
        subprocess.run([sys.executable, "-m", "yt_dlp", "--version"], check=True, stdout=subprocess.DEVNULL)
        return f"{sys.executable} -m yt_dlp"
    except Exception as exc:
        raise SystemExit("yt-dlp not found. Install it with: python3 -m pip install --user yt-dlp") from exc


def find_ffmpeg() -> str:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        return ffmpeg
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as exc:
        raise SystemExit(
            "ffmpeg not found and imageio_ffmpeg is unavailable. "
            "Install it with: python3 -m pip install --user imageio-ffmpeg"
        ) from exc


def split_command(command: str) -> list[str]:
    return command.split()


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def print_metadata(yt_dlp: str, url: str) -> None:
    try:
        subprocess.run(
            split_command(yt_dlp)
            + [
                "--no-playlist",
                "--extractor-args",
                "youtube:player_client=android",
                "--print",
                "%(title)s\n%(id)s\n%(duration_string)s",
                "--skip-download",
                url,
            ],
            check=False,
        )
    except Exception:
        pass


def main() -> int:
    parser = argparse.ArgumentParser(description="Download a single YouTube video as an MP3 for LingQ import.")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("-o", "--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--quality", default="0", help="yt-dlp audio quality; 0 is best VBR")
    parser.add_argument("--format", default="18", help="yt-dlp format selector; default is 18 for a broadly available 360p MP4 source")
    parser.add_argument("--keep-video", action="store_true", help="Keep the downloaded MP4 after extraction")
    parser.add_argument("--allow-playlist", action="store_true", help="Allow yt-dlp to process a playlist URL")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    yt_dlp = find_yt_dlp()
    ffmpeg = find_ffmpeg()

    print_metadata(yt_dlp, args.url)

    cmd = split_command(yt_dlp) + [
        "--extractor-args",
        "youtube:player_client=android",
    ]
    if not args.allow_playlist:
        cmd.append("--no-playlist")
    cmd += [
        "--ffmpeg-location",
        ffmpeg,
        "-f",
        args.format,
        "-x",
        "--audio-format",
        "mp3",
        "--audio-quality",
        args.quality,
        "-o",
        str(args.output_dir / "%(id)s.%(ext)s"),
        args.url,
    ]
    if args.keep_video:
        cmd.append("-k")
    run(cmd)

    mp3s = sorted(args.output_dir.glob("*.mp3"), key=lambda path: path.stat().st_mtime, reverse=True)
    if mp3s:
        latest = mp3s[0]
        size_mb = latest.stat().st_size / 1024 / 1024
        print(f"MP3: {latest}")
        print(f"Size: {size_mb:.2f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
