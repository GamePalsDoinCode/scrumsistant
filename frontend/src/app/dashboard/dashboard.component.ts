import {Component, OnInit, OnDestroy} from '@angular/core'
import {delay} from 'rxjs/operators'
import {UserService} from '../user.service'
import {WebsocketService} from '../websocket.service'
import {Subscription, Observable} from 'rxjs'
import {AuthService} from '../auth.service'
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class DashboardComponent implements OnInit, OnDestroy {
  socketObserver: Observable<any>
  socketSubscription: Subscription
  user: Scrum.User
  nameLocked = false
  broadcastMsg = ''
  usernames: string[] = []

  constructor(
    private authService: AuthService,
    private websocket: WebsocketService,
  ) {}

  async ngOnInit() {
    this.socketObserver = this.websocket.getSocketChannel(
      {},
      msg => msg.channel === 'dashboard',
    )
    this.socketSubscription = this.socketObserver.subscribe(
      serverMsg => this.handleIncoming(serverMsg),
      err => console.log('dashboard channel err', err),
      () => console.log('dashboard channel closed')
    )
    this.authService.getUserInfo().subscribe(
      user => this.user = user
    )
  }
  ngOnDestroy(){
    this.socketSubscription.unsubscribe()
  }

  lockName(): void {
    this.nameLocked = true
    this.dashboardService.userJoined(this.user).subscribe(d => console.log(d))
    // this.socket.next({
    //   type: 'userJoined',
    //   name: this.user.name,
    // })
    // this.socket.next({
    //   type: 'getUsernames',
    // })
  }

  handleIncoming(msg: any) {
    console.log(msg)
    if (msg.type === 'userJoined') {
      if (msg.name !== this.user.displayName) {
        this.broadcastMsg = `Say hello to ${msg.name}!`
        console.log(this.broadcastMsg)
        this.usernames.push(msg.name)
      }
    } else if (msg.type === 'confirmJoined') {
      this.user.pk = msg.pk
    } else if (msg.type === 'userLeft') {
      this.usernames = this.usernames.filter(name => name !== msg.name)
    }
  }
}
