import openai
openai.api_key = ''

from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
from ast import literal_eval
import numpy as np


# Insert search query into the string below
search_query = 'Tunisian unrest grows amid inflation'
data_path = r''
df = pd.read_csv(data_path)
df['embedding'] = df.embedding.apply(literal_eval).apply(np.array)


def search_reviews(df, description, n=3, pprint=False):
    desc_embedding = get_embedding(
        description,
        engine='text-embedding-ada-002'
    )
    df['similarity'] = df.embedding.apply(lambda x: cosine_similarity(x, desc_embedding))

    result = (
        df.sort_values('similarity', ascending=False)
        .head(n)
    )

    if pprint:
        for r in result:
            print(r[:200])
            
            print()

    return result


result = search_reviews(df, search_query, n=3)
print(result)