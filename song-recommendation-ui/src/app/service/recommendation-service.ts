import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Song } from '../models/song.model';


@Injectable({
  providedIn: 'root'
})
export class RecommendationService {
  constructor(private http: HttpClient) {}
 list:any=[]
  getRecommendations(song:string): Observable<Song[]> {

   
    return this.http.post<Song[]>('https://song-recommendation-2ph2.onrender.com/recommend-songs', {
    
      song: song,})
  }
}
  