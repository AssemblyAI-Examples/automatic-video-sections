import argparse
import re 

import assemblyai as aai

parser = argparse.ArgumentParser()
parser.add_argument('filename')

# define the LeMUR task
LEMUR_PROMPT = """
ROLE:
You are a YouTube content professional. You are very competent and able to come up with catchy names for the different sections of video transcripts that are submitted to you.
CONTEXT:
This transcript is of a logistics meeting at GitLab
INSTRUCTION:
You are provided information about the sections of the transcript under TIMESTAMPS, where the format for each line is `<TIMESTAMP> <SECTION SUMMARY>`."
TIMESTAMPS:
{timestamp_lines}
FORMAT:
<TIMESTAMP> <CATCHY SECTION TITLE>
OUTPUT:
""".strip()


def ms_to_hms(start):
    """ convert milliseconds to (hour, minutes, seconds) tuple """
    s, ms = divmod(start, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return h, m, s


def create_timestamps(chapters):
    """ given chapters, return timestamps formatted as (HH):MM:SS <CHAPTER_TITLE> """
    last_hour = ms_to_hms(chapters[-1].start)[0]
    time_format = "{m:02d}:{s:02d}" if last_hour == 0 else "{h:02d}:{m:02d}:{s:02d}"

    lines = []
    for idx, chapter in enumerate(chapters):
        # first YouTube timestamp must be at zero
        h, m, s = (0, 0, 0) if idx == 0 else ms_to_hms(chapter.start)
        lines.append(f"{time_format.format(h=h, m=m, s=s)} {chapter.headline}")
        
    return "\n".join(lines)


def filter_timestamps(text):
    lines = text.splitlines()
    timestamped_lines = [line for line in lines if re.match(r'\d+:\d+', line)]  # Use regex to filter lines starting with a timestamp
    filtered_text = '\n'.join(timestamped_lines)
    return filtered_text


def verify_timestamps(a, b):
    """ verify that the timestamps in two strings match """
    original = timestamp_lines.splitlines()
    filtered = filtered_output.splitlines()

    for o, f in zip(original, filtered):
        original_time = o.split(' ')[0]
        filtered_time = f.split(' ')[0]
        if not original_time == filtered_time:
            raise RuntimeError(f"Timestamp mismatch - original timestamp '{original_time}' does not match LLM timestamp '{filtered_time}'")


if __name__ == "__main__":
    args = parser.parse_args()

    # create transcriber. this object is responsible for performing our transcription
    transcriber = aai.Transcriber(
        # we add a TranscriptionConfig to turn on auto chapters, which is AssemblyAI's model for automatically determining video sections
        config=aai.TranscriptionConfig(auto_chapters=True)
    )

    # transcribe the file
    transcript = transcriber.transcribe(args.filename)

    if transcript.error: raise RuntimeError(transcript.error)

    # create transcript lines from the chapter information
    timestamp_lines = create_timestamps(transcript.chapters)

    # submit to lemur, extract the response, and filter out irrelevant lines
    prompt = LEMUR_PROMPT.format(timestamp_lines=timestamp_lines)
    result = transcript.lemur.task(prompt)
    output = result.response.strip()
    filtered_output = filter_timestamps(output)
    
    # verify the LLM did not modify timesteps
    verify_timestamps(timestamp_lines, filtered_output)

    # print the results
    print("TIMESTAMPS:")
    print(filtered_output)
