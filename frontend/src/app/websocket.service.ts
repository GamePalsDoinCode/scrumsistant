import {Injectable, OnDestroy} from '@angular/core'
import {HttpClient} from '@angular/common/http'
import {webSocket, WebSocketSubject} from 'rxjs/webSocket'
import {BehaviorSubject, of, Subscription, Observable} from 'rxjs'
import {switchMap} from 'rxjs/operators'

interface WebsocketAuthObj {
  signedToken: string
  verifyKey: string
}

@Injectable({
  providedIn: 'root',
})
export class WebsocketService implements OnDestroy {
  socket$: WebSocketSubject<any>
  authEmitter: BehaviorSubject<boolean> = new BehaviorSubject(false)
  authSub: Subscription

  constructor(private http: HttpClient) {}

  ngOnDestroy() {
    this.closeSocket()
  }

  closeSocket() {
    if (this.authSub) {
      this.authSub.unsubscribe()
    }
    if (this.socket$) {
      this.socket$.complete()
      this.socket$ = null
    }
  }

  requestWebsocketAuthToken() {
    return this.http.get<WebsocketAuthObj>('api/get_websocket_auth_token')
  }

  openConnection() {
    if (!this.socket$) {
      this.requestWebsocketAuthToken().subscribe(authObj => {
        this.socket$ = webSocket('ws://localhost:8000')
        const authMessage = {
          msg: 'authTokenVerification',
          data: authObj,
        }
        this.socket$.subscribe(
          message => console.log('master sub message', message),
          err => console.log('master sub error', err),
          () => {
            console.log('master sub closed!')
          }
        )
        const authObs = this.multiplexHelper(
          authMessage,
          null,
          msg => msg.channel === 'auth'
        )
        this.authSub = authObs.subscribe(
          success => this.authEmitter.next(true),
          err => this.authEmitter.next(false),
          () => {}
        )
      })
    }
    return this.authEmitter
  }

  private multiplexHelper(
    initialMessage: any,
    closeMessage: any,
    filterFunc: (message: any) => boolean
  ) {
    return this.socket$.multiplex(
      () => initialMessage ?? {},
      () => closeMessage ?? {},
      filterFunc
    )
  }

  getSocketChannel(initialMessage: any, filterFunc: (message: any) => boolean) {
    return this.openConnection().pipe(
      switchMap((connOK: boolean) =>
        connOK
          ? this.multiplexHelper(initialMessage, {}, filterFunc)
          : of(false)
      )
    )
  }
}
