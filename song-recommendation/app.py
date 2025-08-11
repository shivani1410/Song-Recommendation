from dotenv import load_dotenv
load_dotenv()

from flask import Flask,request,jsonify
from flask_cors import CORS
import pandas as pd
import os
import logging
from supabase import create_client,Client

logging.basicConfig(
    level=logging.INFO,         
    format='%(asctime)s - %(levelname)s - %(message)s'
)
SUPABASE_URL=os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY=os.getenv('SUPABASE_ANON_KEY')

supabase:Client=create_client(SUPABASE_URL,SUPABASE_ANON_KEY)
app=Flask(__name__)
CORS(app)

@app.route('/recommend-songs',methods=['POST'])
def recommend_songs():
  logging.info("Application started")
 
  data=request.get_json()
  song_name=data['song']
  song_data=supabase.table('Song Recommender').select('*').ilike("name",song_name).execute()
  if not song_data.data:
      return jsonify({"error": "Song not found"}), 404
  cluster_id=song_data.data[0]["cluster"]
  recommend_song_list=(supabase.table('Song Recommender').select("name","artist").eq("cluster",cluster_id).limit(5).execute())
  return jsonify(recommend_song_list.data)
@app.route('/songs',methods=['GET'])
def get_songs():
    return jsonify('get songs')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
