import {Component, OnInit} from '@angular/core'
import {UserService, DisplayAndID} from '../user.service'
import {WebsocketService} from '../websocket.service'
import {Subscription} from 'rxjs'

@Component({
  selector: 'app-standup',
  templateUrl: './standup.component.html',
  styleUrls: ['./standup.component.scss'],
})
export class StandupComponent implements OnInit {
  currentSpeakerIdx = 0
  currentTeam: DisplayAndID[]
  socketSubscription: Subscription

  constructor(
    private userService: UserService,
    private websocketService: WebsocketService
  ) {}

  async ngOnInit() {
    this.currentTeam = await this.userService.currentlyLoggedIn().toPromise()
    this.socketSubscription = this.websocketService
      .getSocketChannel({}, msg => msg.channel === 'daily' && !!msg.message)
      .subscribe(
        msg => this.handleMessage(msg.message),
        err => console.log('DailyError', err),
        () => console.log('DailyClose')
      )
  }

  getCurrentSpeaker() {
    return this.currentTeam[this.currentSpeakerIdx]
  }

  handleMessage(message: any) {
    console.log(message)
  }
}
