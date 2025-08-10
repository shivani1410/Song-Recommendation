from flask import Flask,request,jsonify
from flask_cors import CORS
import pandas as pd
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pkl_path = os.path.join(BASE_DIR, "song_recommender.pkl")

df=pd.read_pickle(pkl_path)
app=Flask(__name__)
CORS(app)

@app.route('/recommend-songs',methods=['POST'])
def recommend_somgs():
  data=request.get_json()
  song_name=data['song']
  
  song=df[df['track_name'].str.lower()==song_name.lower()]
  if song.empty:
    return jsonify({"error":"Song not found"}),404
  cluster_id=song['cluster'].values[0]
  similiar_songs=df[df['cluster']==cluster_id].sample(5)
  result=similiar_songs[['track_name','artist']].to_dict(orient='records')
  return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
