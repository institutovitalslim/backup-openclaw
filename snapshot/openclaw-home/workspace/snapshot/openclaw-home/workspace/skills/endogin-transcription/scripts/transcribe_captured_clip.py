from pathlib import Path
import os
import sys

from openai import OpenAI


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: python transcribe_captured_clip.py <audio-or-video-path> [out-txt]")

    input_path = Path(sys.argv[1]).expanduser().resolve()
    out_path = (
        Path(sys.argv[2]).expanduser().resolve()
        if len(sys.argv) > 2
        else input_path.with_suffix(".transcript.txt")
    )

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is not set")

    client = OpenAI(api_key=api_key)
    with input_path.open("rb") as fh:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=fh,
            language="pt",
        )

    out_path.write_text(transcript.text.strip() + "\n", encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
