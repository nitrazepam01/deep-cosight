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
