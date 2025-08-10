from flask import Flask,request,jsonify
from flask_cors import CORS
import pandas as pd
import os
import logging
import gdown

FILE_ID = "1f9gF8CeFpgCdJzxMAYliZxgwxaiOWy-N"
OUTPUT_FILE = "song_recommender.parquet"

# Download if not already present
if not os.path.exists(OUTPUT_FILE):
    print("Downloading dataset...")
    url = f"https://drive.google.com/uc?id={FILE_ID}"
    gdown.download(url, OUTPUT_FILE, quiet=False)

# Now load the pickle
df = pd.read_parquet(OUTPUT_FILE)
print(f"Dataset loaded with {len(df)} rows")

logging.basicConfig(
    level=logging.INFO,          # Minimum level to log
    format='%(asctime)s - %(levelname)s - %(message)s'
)
app=Flask(__name__)
CORS(app)

@app.route('/recommend-songs',methods=['POST'])
def recommend_somgs():
  logging.info("Application started") 
  data=request.get_json()
  
  song_name=data['song']
  
  song=df[df['name'].str.lower()==song_name.lower()]
  if song.empty:
    return jsonify({"error":"Song not found"}),404
  cluster_id=song['cluster'].values[0]
  similiar_songs=df[df['cluster']==cluster_id].sample(5)
  result=similiar_songs[['name','artist']].to_dict(orient='records')
  return jsonify(result)

@app.route('/songs',methods=['GET'])
def get_songs():
    return jsonify('get songs')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
