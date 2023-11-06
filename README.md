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


### Install the requirements

```shell
pip install -r requirements.txt
```

### Run the program

`python main.py <FILENAME>`, where `<FILENAME>` is either a publicly-accessible remote URL or a local filepath.

Example:
```shell
python main.py https://storage.googleapis.com/aai-web-samples/meeting.mp4
```

Output:
```plaintext
TIMESTAMPS:
00:00 Proposing Department Key Reviews
01:40 Clarifying Merge Request Rate Definitions
03:51 Fixing the Wider Merge Request Rate Metric
08:18 Confirming Wider Rate is Community-Only
08:40 Data Team Lag Issues
09:40 Discussing Postgres Replication
13:05 Defect Tracking and SLO Update
18:32 Smaller Security Metric Decline Seen as Improvement
20:42 Investigating Below-Target Narrow Merge Request Rate
23:50 Wrapping Up the Meeting
```