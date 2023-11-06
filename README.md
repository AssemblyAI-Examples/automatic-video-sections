# Automatically chapterize a video or audio file

Automatically generate named chapters with timestamps for an input audio or video file

## Usage

### Set your AssemblyAI key

Set your AssemblyAI API key as an environment variable. You can get one for free [here](https://www.assemblyai.com/dashboard/signup).

```shell
# Mac/Linux:
export ASSEMBLYAI_API_KEY=<YOUR_KEY>

# Windows:
set ASSEMBLYAI_API_KEY=<YOUR_KEY>
```

### Run the program

`python main.py <FILENAME>`, where `<FILENAME>` is either a publicly-accessible remote URL or a local filepath.

Example:
```shell
python main.py https://storage.googleapis.com/aai-web-samples/meeting.mp4
```

Output:
```plaintext

```