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
It calls a local HTTP music-recognition service and normalizes returned
song candidates for later source checking.

Default endpoint:

```text
http://127.0.0.1:12400
```

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
