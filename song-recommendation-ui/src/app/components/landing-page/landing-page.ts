import { Component, inject ,ChangeDetectorRef} from '@angular/core';
import { CommonModule } from '@angular/common';
import { RecommendationService } from '../../service/recommendation-service';
import { Observable } from 'rxjs';
import { Song } from '../../models/song.model';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-landing-page',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './landing-page.html',
  styleUrls: ['./landing-page.css']
})
export class LandingPage {
  recommendationService: RecommendationService = inject(RecommendationService);
  cdr = inject(ChangeDetectorRef);

 list: Song[] = [];
  songName = '';
  loading :boolean=false // Loader flag

  constructor() {}


  getRecommendations(songName: string) {
    if (!songName.trim()) return;

    this.loading = true;
    this.list = [];

    this.recommendationService.getRecommendations(songName).subscribe(
  (data: Song[]) => {
    console.log('Raw API data:', data);
    this.list = Array.isArray(data) ? data : [];
    this.loading = false;
    this.cdr.detectChanges();
  },
  (error) => {
    console.error('Error fetching recommendations:', error);
    this.loading = false;
    this.cdr.detectChanges();
  }
);
    console.log(this.loading)
  }
  
}
