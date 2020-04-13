import { Component, OnInit } from '@angular/core';
import {ClockService} from '../clock.service'

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
  votes: number[] = []
  outlier: number | undefined = undefined
  average: number | undefined = undefined


  constructor(private clockService: ClockService) {}

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


    // TEMP WIHLE THERES NOT OTHER FRIENDS
    this.votes.push(Math.floor(Math.random() * 20 + 1))
    this.voteAverage()
    this.voteOutliers()
  }

  beginVote(){
    if (this.votingStates[this.votingStateIndex] !== 'preVoting') {
      return
    }
    this.votingStateIndex = 1
    this.clockService.getTimer(
      this.allowedVotingTimeSeconds,
      1000,
      () => this.allowedVotingTimeSeconds = this.allowedVotingTimeSeconds - 1,
      () => this.votingStateIndex = 2,
    )

    // let timer$ = timer((this.allowedVotingTimeSeconds + 1) * 1000)
    // let tickSource$ = interval(1000)
    // tickSource$.pipe(takeUntil(timer$)).subscribe(
    //   tick => {
    //     this.allowedVotingTimeSeconds = this.allowedVotingTimeSeconds - 1
    //   },
    //   () => {}, //onError
    //   () => {
    //     this.votingStateIndex = 2
    //   },
    // )
  }

  voteAverage(){
    let average = this.votes.reduce((acc, vote) => acc + vote, 0) / this.votes.length
    let diffs = this.points.map(point => Math.abs(point - average))
    let lowest = Math.min(...diffs)
    let lowestIdx = diffs.findIndex(diff => diff == lowest)
    this.average = this.points[lowestIdx]
  }

  voteOutliers(){
    // TEMP
    let names = ['Alfonso', 'Alice', 'Amelia']
    let outlier = this.votes.find(vote => Math.abs(this.average - vote) > 1)
    this.outlier = outlier
  }


}
