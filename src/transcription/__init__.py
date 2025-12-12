import enum
from pathlib import Path

import click

from transcription.transcribe import (
    add_subtitle_to_video,
    extract_audio,
    generate_subtitle_file,
    transcribe,
)


class EmbedType(enum.Enum):
    no = enum.auto()
    soft = enum.auto()
    hard = enum.auto()


class ModelSizeType(enum.Enum):
    tiny = "tiny"
    base = "base"
    small = "small"
    medium = "medium"
    large = "large"


@click.command()
@click.option(
    "--embed-subtitles",
    "-e",
    type=click.Choice(EmbedType, case_sensitive=False),
    help="Embed subtitles into the video.",
    default=EmbedType.no,
    show_default=True,
)
@click.option(
    "--model-size",
    "-m",
    type=click.Choice(ModelSizeType, case_sensitive=False),
    help="OpenAI Whisper model size.",
    default=ModelSizeType.medium,
    show_default=True,
)
@click.option(
    "--video-path",
    "-v",
    help="File path(s) of videos to translate.",
    multiple=True,
    required=True,
)
def main(embed_subtitles, model_size, video_path):
    """
    Tool for translating and transcribing videos locally using OpenAI Whisper.
    """
    print(f"Saving subtitles using embed option '{embed_subtitles}'.")

    for v in video_path:
        path = Path(v)
        print(f"Translating and transcribing '{path.resolve()}'.")
        extracted_audio = extract_audio(path)
        _, segments = transcribe(audio=extracted_audio, model_size=model_size.value)
        subtitle_file = generate_subtitle_file(
            language="eng",
            segments=segments,
            video=path,
        )

        if embed_subtitles != EmbedType.no:
            add_subtitle_to_video(
                soft_subtitle=embed_subtitles == EmbedType.soft,
                subtitle_file=subtitle_file,
                subtitle_language="eng",
                video=path,
            )
