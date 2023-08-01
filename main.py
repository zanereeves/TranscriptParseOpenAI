from youtube_transcript_api import YouTubeTranscriptApi as yta
import scrapetube
import pandas as pd
import openai

# insert api-key below
openai.api_key = ''
from openai.embeddings_utils import get_embedding

# insert path to csv to save embedding data
csv_path = r''
# insert your channel URL with all @s removed
channel_url = 'https://www.youtube.com/BBCNews'


videos = scrapetube.get_channel(channel_url=channel_url, limit=3)

transcript = []
vids = []
for vid in videos:
    data = yta.get_transcript(vid['videoId'])
    vids.append(vid['videoId'])
    curr_video = ''
    for value in data:
        for key, val in value.items():
            if key == 'text' and len(curr_video) < 4000:
                curr_video += val + ' '
    transcript.append(curr_video)


embedding_model = "text-embedding-ada-002"
df = pd.DataFrame(transcript, columns=['Text'])
df['embedding'] = df['Text'].apply(lambda x: get_embedding(x, engine=embedding_model))
df['videoId'] = vids


df.to_csv(csv_path)
print(df)