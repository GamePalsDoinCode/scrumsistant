import { Component, OnInit } from '@angular/core';
import {timer, interval} from 'rxjs';
import {takeUntil} from 'rxjs/operators'

@Component({
  selector: 'app-pointing',
  templateUrl: './pointing.component.html',
  styleUrls: ['./pointing.component.scss']
})
export class PointingComponent implements OnInit {

  // TODO: points should be configurable I guess?
  points: number[] = [
  1,
  2,
  3,
  5,
  8,
  13,
  20,
]

  votingStates = [
    'preVoting',
    'periVoting',
    'postVoting',
  ]
  votingStateIndex = 0

  allowedVotingTimeSeconds = 3

  numVoters: number = 1 // TODO this will be more sophisticated
  votes: number[]


  constructor() { }

  ngOnInit(): void {
  }

  selectPoint(pointValue: number){
    this.votes.push(pointValue)
    this.checkIfDone()
  }

  checkIfDone(){
    if (
      this.votes.length === this.numVoters &&
      this.votingStateIndex === 1
     ){
      this.votingStateIndex = 2
    }
  }

  beginVote(){
    if (this.votingStates[this.votingStateIndex] !== 'preVoting') {
      return
    }
    this.votingStateIndex = 1

    let timer$ = timer((this.allowedVotingTimeSeconds + 1) * 1000)
    let tickSource$ = interval(1000)
    tickSource$.pipe(takeUntil(timer$)).subscribe(
      tick => {
        this.allowedVotingTimeSeconds = this.allowedVotingTimeSeconds - 1
      },
      () => {}, //onError
      () => {
        this.votingStateIndex = 2
      },
    )
  }

}
