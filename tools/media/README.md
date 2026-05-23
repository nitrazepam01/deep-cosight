# Local Media Utilities

`youtobe_tool` can use project-local media utilities before falling back
to the host environment. Put optional executables here:

```text
tools/media/bin/yt-dlp-script.py
tools/media/bin/ffmpeg.exe
tools/media/bin/ffprobe.exe
```

When using `yt-dlp-script.py`, keep its Python package dependencies under:

```text
tools/media/pydeps/
```

On non-Windows systems, use the corresponding executable names without `.exe`.

If this directory is empty, the tool falls back to conda base discovery.

## Local Music Recognition

`music_recognition_lookup` is a generic adapter for short local audio clips.
It calls a local NetEase-compatible HTTP music-recognition service and
normalizes returned song candidates for later source checking.
Before calling the service, it tries to normalize input audio to the format
expected by the NetEase recognition package:

```text
48 kHz, stereo, WAV
```

The normalized file is written next to the source audio as
`<name>_ncm_48k.wav`.

This project uses `MerlinCN/ncm-recognize-api` as the local backend. The
service is installed under:

```text
tools/media/ncm-recognize-api/
```

Start it from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File tools/start_music_recognition_backend.ps1
```

Or start it in the background:

```powershell
powershell -ExecutionPolicy Bypass -File tools/start_music_recognition_backend.ps1 -Background
```

Default endpoint:

```text
http://127.0.0.1:12400
```

`music_recognition_lookup` will first try this default endpoint. If the
service is not already reachable and `tools/media/ncm-recognize-api` has
dependencies installed, the tool can start `server.js` in the background and
wait briefly before sending the recognition request.

Override with one of:

```text
MUSIC_RECOGNITION_URL
NCM_RECOGNIZE_API_URL
NCM_RECOGNIZE_URL
```

Only local endpoints such as `127.0.0.1`, `localhost`, or `::1` are allowed
by default. The request body is JSON:

```json
{"file":"C:/path/to/short-audio.wav"}
```

The response is treated as candidate evidence only; the agent should verify
the returned song title and artist/composer against reliable sources before
using it as a final answer.

For video music recognition, extract a short audio clip with `youtobe_tool`,
then call `music_recognition_lookup`. General speech transcription or
humming-style lookup services are not good substitutes for this local
background-music recognition path.
