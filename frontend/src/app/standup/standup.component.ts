import { Component, OnInit } from '@angular/core';
import {ClockService} from '../clock.service'


@Component({
  selector: 'app-standup',
  templateUrl: './standup.component.html',
  styleUrls: ['./standup.component.scss']
})
export class StandupComponent implements OnInit {

  constructor(private clockService: ClockService) { }

  maxSpeakingTimeSeconds = 5
  participants = ['You', 'Dr. Tuttle', 'Judge Bostrum', 'Professor Stromburg']
  speakerIdx: number | undefined = undefined

  spokenIdxs = new Set()
  standupOver = false
  curSpeakingTime = 5

  ngOnInit(): void {
    this.speakerIdx = Math.random() < 0.5 ? 0 : 1;
    this.spokenIdxs.add(this.speakerIdx)
    this.setUpClock()
  }

  setUpClock(){
    this.curSpeakingTime = this.maxSpeakingTimeSeconds
    this.clockService.getTimer(
      this.maxSpeakingTimeSeconds,
      1000,
      () => this.curSpeakingTime = this.curSpeakingTime - 1,
      () => this.chooseNextSpeaker(),
    )
  }

  chooseNextSpeaker(){

    let availableIdxs: number[] = []
    this.participants.map((_, idx) => {
      if (!this.spokenIdxs.has(idx)){
        availableIdxs.push(idx)
      }
    })
    let nextIdx = Math.floor(Math.random() * availableIdxs.length)
    this.speakerIdx = availableIdxs[nextIdx]
    this.spokenIdxs.add(this.speakerIdx)
    this.setUpClock()

  }

  endTurn(){
    if (this.spokenIdxs.size == this.participants.length){
      this.standupOver = true
    } else {
      this.chooseNextSpeaker()
    }


  }

}
