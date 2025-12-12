import math
from pathlib import Path

import ffmpeg
import speech_recognition as sr


def format_time(seconds):
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"

    return formatted_time


def extract_audio(video):
    extracted_audio = f"audio-{video.stem}.wav"
    stream = ffmpeg.input(video)
    stream = ffmpeg.output(stream, extracted_audio)
    ffmpeg.run(stream, overwrite_output=True)

    return extracted_audio


def transcribe(audio, model_size):
    audio_data = sr.AudioData.from_file(audio)
    r = sr.Recognizer()
    print("Starting translation and transcription.")
    transcription = r.recognize_whisper(
        audio_data, task="translate", show_dict=True, model=model_size
    )
    video_language = transcription["language"]
    segments = transcription["segments"]

    # Delete the temp audio file.
    Path(audio).unlink(missing_ok=True)

    return video_language, segments


def generate_subtitle_file(language, segments, video):
    subtitle_file = video.with_name(f"{video.stem}.{language}.srt")
    text = ""
    for index, segment in enumerate(segments):
        segment_start = format_time(segment["start"])
        segment_end = format_time(segment["end"])
        text += f"{str(index + 1)} \n"
        text += f"{segment_start} --> {segment_end} \n"
        text += f"{segment['text']} \n"
        text += "\n"

    with open(subtitle_file, "w") as f:
        f.write(text)

    return subtitle_file


def add_subtitle_to_video(soft_subtitle, subtitle_file, subtitle_language, video):
    video_input_stream = ffmpeg.input(video)
    subtitle_input_stream = ffmpeg.input(subtitle_file)
    output_video = str(video.with_name(f"output-{video.name}"))
    subtitle_track_title = subtitle_file.stem

    if soft_subtitle:
        stream = ffmpeg.output(
            video_input_stream,
            subtitle_input_stream,
            output_video,
            **{"c": "copy", "c:s": "mov_text"},
        ).global_args(
            "-metadata:s:s:0",
            f"language={subtitle_language}",
            "-metadata:s:s:0",
            f"title={subtitle_track_title}",
        )
        ffmpeg.run(stream, overwrite_output=True)
    else:
        stream = ffmpeg.output(
            video_input_stream, output_video, vf=f"subtitles={subtitle_file}"
        )

        ffmpeg.run(stream, overwrite_output=True)
