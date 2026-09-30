# LingQ YouTube Importer

Codex skill for importing a YouTube video into LingQ as an audio lesson, then attaching the original YouTube video to the saved lesson.

## Quick Start

The fastest way is to hand this repo to Codex and let it install the skill for you.

Copy this prompt into Codex:

```text
Clone and install this Codex skill:
https://github.com/johnlewissims/lingq-youtube-import.git

Install any required local Python dependencies, copy the skill into my Codex skills directory as `lingq-youtube-import`, and tell me when it is ready to use.
```

Codex should run the equivalent of:

```bash
git clone https://github.com/johnlewissims/lingq-youtube-import.git
cd lingq-youtube-import
python3 -m pip install --user yt-dlp imageio-ffmpeg
mkdir -p ~/.codex/skills
cp -R . ~/.codex/skills/lingq-youtube-import
```

Restart Codex or reload skills if needed.

Then use it:

```text
Use lingq-youtube-import for this video:
https://www.youtube.com/watch?v=VIDEO_ID
```

Or, if your Codex UI supports skill mentions:

```text
$lingq-youtube-import https://www.youtube.com/watch?v=VIDEO_ID
```

Codex will download the MP3, upload it to LingQ, import the lesson, add the YouTube video, save, and verify.

## Requirements

- Codex with skill support.
- A LingQ account.
- Python 3.
- `yt-dlp`.
- `ffmpeg` or `imageio-ffmpeg`.

If you already have system `ffmpeg`, `imageio-ffmpeg` is optional. The quick-start install command includes it so most users do not need to think about ffmpeg setup.

## Login

Sign in to LingQ in the browser when Codex asks.

The skill does not collect, type, or store passwords, one-time codes, or recovery codes. If LingQ shows login, SSO, 2FA, CAPTCHA, or an expired session, Codex should pause until you sign in directly.

## What The Skill Does

1. Downloads one YouTube video as an MP3.
2. Opens or reuses LingQ.
3. Uses `Audio Transcription`.
4. Uploads the MP3.
5. Sets a title from the YouTube title.
6. Imports the lesson.
7. Opens `Edit Lesson`.
8. Adds the original YouTube URL as a video.
9. Saves and verifies the lesson.

Playlist URLs are treated as a single-video import by default.

## Helper Script

Run the downloader directly:

```bash
python3 scripts/youtube_to_mp3.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Default output:

```text
./lingq-imports
```

Custom output directory:

```bash
python3 scripts/youtube_to_mp3.py "https://www.youtube.com/watch?v=VIDEO_ID" \
  --output-dir ~/Downloads/lingq-imports
```

Keep the downloaded video too:

```bash
python3 scripts/youtube_to_mp3.py "https://www.youtube.com/watch?v=VIDEO_ID" \
  --keep-video
```

Allow playlist processing:

```bash
python3 scripts/youtube_to_mp3.py "https://www.youtube.com/watch?v=VIDEO_ID&list=PLAYLIST_ID" \
  --allow-playlist
```

## Safety

Your request to import a specific YouTube video authorizes Codex to upload only that generated MP3 to LingQ and attach only that YouTube URL.

Codex should ask before it uploads unrelated files, changes sharing, changes account settings, deletes anything, enters credentials, or handles CAPTCHA/2FA.

## Troubleshooting

`yt-dlp not found`

```bash
python3 -m pip install --user yt-dlp
```

`ffmpeg not found`

```bash
python3 -m pip install --user imageio-ffmpeg
```

LingQ says the file is too large: use a shorter video, lower audio quality, or split the source.

LingQ stays on "Your learning content is being generated": wait and refresh. Long videos can take several minutes. Do not create a duplicate lesson just because generation is slow.

YouTube preview does not load in LingQ: check that the YouTube URL opens normally and allows embedding. If LingQ cannot load it, keep the audio lesson and report the video-attachment failure.
