---
name: lingq-youtube-import
description: Import a YouTube video into LingQ as an audio lesson by creating an MP3, uploading it, adding the YouTube video link, and verifying the saved lesson.
---

# LingQ YouTube Import

Use this skill when the user asks to import a YouTube video into LingQ, make a LingQ lesson from a YouTube link, or repeat the workflow of downloading an MP3 and attaching the YouTube video to a LingQ lesson.

## Workflow

1. Prepare the MP3 locally before using the browser.
   - Use `scripts/youtube_to_mp3.py <youtube-url>` unless the user already provided an MP3.
   - The script defaults to `./lingq-imports` under the current working directory. Use `--output-dir` when the user wants a specific destination.
   - The script uses `--no-playlist` by default. If the URL contains playlist parameters, import only the single video unless the user explicitly requests a playlist workflow.
   - The script installs no new tools. It expects `yt-dlp` and uses either system `ffmpeg` or `imageio_ffmpeg` if available.
   - If `yt-dlp` or `imageio_ffmpeg` is missing, install the missing Python package with `python3 -m pip install --user ...` only when needed.

2. Use the existing signed-in LingQ browser session when available.
   - If LingQ is already open, reuse that tab.
   - If not, open LingQ and navigate to the import/editor page for the target language. If the language is ambiguous, use the language already selected in LingQ or ask a concise question before importing.
   - If LingQ shows a logged-out page, login form, expired session, SSO prompt, two-factor prompt, CAPTCHA, or any other authentication blocker, pause and ask the user to sign in directly in the browser. Do not ask for, type, or store passwords, one-time codes, or recovery codes. After the user says they are signed in, continue from the current LingQ page.
   - Do not change account settings, course organization, sharing permissions, or target language unless the user asks.

3. In LingQ, create the lesson.
   - Choose `Audio Transcription`.
   - Upload the generated `.mp3`.
   - Continue to `Review & Import`.
   - Set a concise title based on the YouTube title.
   - Keep the LingQ language/course values already selected unless the user specified different ones.
   - Click `Import`.
   - Verify LingQ shows either the generated reader page or a message that the learning content is being generated.

4. Add the YouTube video link after the lesson exists.
   - Open the lesson reader if needed.
   - Use the lesson menu (`...`) and choose `Edit Lesson`.
   - On `Details`, use `Add Video`, paste the original YouTube URL, wait for the YouTube preview/player, then click `Add Video`.
   - Save the lesson.
   - Verify the page says changes were saved and that the editor shows an embedded YouTube player or video card.
   - Return to the reader and verify an additional video control appears.

## Browser Safety

Uploading the MP3 to LingQ is a file upload to a third-party service. The user's request to import the specific YouTube video into their LingQ account authorizes uploading the generated MP3 for that video and adding that same YouTube URL. Ask for confirmation before uploading any unrelated file, changing lesson sharing away from private, deleting content, or submitting information not needed for this workflow.

Authentication is user-handled. If login is needed, ask the user to take over in the browser and tell you when the LingQ account is ready. Do not attempt to solve CAPTCHAs, handle two-factor codes, or collect credentials.

## Reporting

At completion, report:

- The local MP3 path.
- The LingQ lesson title.
- Whether the YouTube video was added and saved.
- Any blocker, such as LingQ upload limits, failed video preview, authentication, or a CAPTCHA.
