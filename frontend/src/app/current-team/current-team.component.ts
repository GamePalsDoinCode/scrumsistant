import {Component, OnInit, OnDestroy, Input} from '@angular/core'
import {UserService, DisplayAndID} from '../user.service'
import {AuthService} from '../auth.service'
import {concat, Subscription} from 'rxjs'
import {WebsocketService} from '../websocket.service'

@Component({
  selector: 'app-current-team',
  templateUrl: './current-team.component.html',
  styleUrls: ['./current-team.component.scss'],
})
export class CurrentTeamComponent implements OnInit, OnDestroy {
  currentTeam: DisplayAndID[]
  currentUser: Scrum.User
  socketSubscription: Subscription

  @Input() closeFunction: () => void

  constructor(
    private userService: UserService,
    private authService: AuthService,
    private websocketService: WebsocketService
  ) {}

  async ngOnInit() {
    this.currentTeam = await this.userService.currentlyLoggedIn().toPromise()
    this.socketSubscription = this.websocketService
      .getSocketChannel(
        {},
        msg => msg.channel === 'currentTeam' && !!msg.message
      )
      .subscribe(
        msg => this.handleMessage(msg.message),
        err => console.log('currentTeamError', err),
        () => console.log('currentTeamClosed')
      )
  }
  ngOnDestroy() {
    if (this.socketSubscription) {
      this.socketSubscription.unsubscribe()
    }
  }

  private handleMessage(msg: any) {
    let newUser: DisplayAndID
    let pkToRemove = -1
    if (msg.userLeft) {
      pkToRemove = msg.userLeft
    }
    if (msg.userJoined) {
      pkToRemove = msg.userJoined[1]
      newUser = msg.userJoined
    } else if (msg.userUpdated) {
      pkToRemove = msg.userUpdated[1]
      newUser = msg.userUpdated
    }

    this.currentTeam = this.currentTeam.filter(
      member => member[1] !== pkToRemove
    )
    if (newUser) {
      this.currentTeam.push(newUser)
    }
  }
}
