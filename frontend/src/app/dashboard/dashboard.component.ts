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
  isPM = false

  constructor(
    private authService: AuthService,
    private websocket: WebsocketService,
    private userService: UserService
  ) {}

  async ngOnInit() {
    this.socketObserver = this.websocket.getSocketChannel(
      {},
      msg => msg.channel === 'dashboard'
    )
    this.socketSubscription = this.socketObserver.subscribe(
      serverMsg => this.handleIncoming(serverMsg),
      err => console.log('dashboard channel err', err),
      () => console.log('dashboard channel closed')
    )
    this.authService.getUserInfo().subscribe(user => (this.user = user))
    this.isPM = !!(await this.authService.queryUser('is_PM').toPromise())
  }
  ngOnDestroy() {
    this.socketSubscription.unsubscribe()
  }

  saveName(): void {
    this.userService.save(this.user).subscribe()
  }

  handleIncoming(msg: any) {}

  logout() {
    this.authService.logout()
  }
}
