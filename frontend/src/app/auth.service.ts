import {Injectable} from '@angular/core'
import {HttpClient} from '@angular/common/http'
import {Router, CanActivate, ActivatedRouteSnapshot} from '@angular/router'
import {tap, switchMap} from 'rxjs/operators'
import {of, Observable} from 'rxjs'
import {WebsocketService} from './websocket.service'

type valueof<T> = T[keyof T]
interface LoginReturnType{
  user: Scrum.User;
  auth: string;
}


@Injectable({
  providedIn: 'root',
})
export class AuthService implements CanActivate {
  errorMessage = ''
  user: Scrum.User

  constructor(private http: HttpClient, private router: Router, private websocket: WebsocketService) {}

  isAuthenticated() {
    // TODO: is this a bad idea to hit the backend on any route change?  Let's say no!
    return this.http
      .get<Scrum.User>('api/is_authenticated')
      .pipe(tap(user => (this.user = user)))
  }


  private clearUser(){
    this.user = {email: '', pk: null, displayName: '', is_PM: false}
  }
  checkCredentials(
    user: {email: string; password: string},
    redirectTo: string | null = null
  ) {
    this.errorMessage = ''
    this.http.post<LoginReturnType>('/api/login', {...user}).subscribe(
      successResponse => {
        this.user = successResponse.user
        this.websocket.openConnection().subscribe(connOk => {
          if (connOk !== false){
            const redirectDefault = this.user.is_PM ? '/pm_tools' : '/app/dashboard'
            this.router.navigate([redirectTo || redirectDefault])
          } else {
            this.errorMessage = 'Unknown Error: Please Try Again'
            this.clearUser()
          }
        })
      },
      error => {
        this.errorMessage = "Invalid Credentials!  We've got a saboteur!"
        this.clearUser()
      }
    )
    return false
  }

  logout() {
    this.websocket.closeSocket()
    this.http.get('/api/logout').subscribe(
      () => this.router.navigate(['/login']),
      () => this.router.navigate(['/login'])
    )
  }

  private getUserHelper(propertyFunc: (user: Scrum.User) => valueof<Scrum.User> | Scrum.User ) {
    const propertyOf /*get it?!*/ = (user: Scrum.User) => of(propertyFunc(user))
    return this.user === null ?
      this.isAuthenticated().pipe(
        switchMap(() => propertyOf(this.user))
      ) :
      propertyOf(this.user)
  }

  queryUser(property: keyof Scrum.User) {
    return this.getUserHelper(user => user[property]) as Observable<valueof<Scrum.User>>
  }

  getUserInfo() {
    return this.getUserHelper(user => user) as Observable<Scrum.User>
  }

  async canActivate(route: ActivatedRouteSnapshot) {
    // TODO: this should probably be moved into its own AuthGuard service
    // TODO theres _def_ a better way to do this with something out of rxjs - find!
    // tbh having the endpoint return something instead of error codes and using map might be nicer?
    try {
      await this.isAuthenticated().toPromise()
      return true
    } catch (_) {
      this.router.navigate(['/login'])
      return false
    }
  }
}
