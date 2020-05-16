import {Injectable} from '@angular/core'
import {HttpClient} from '@angular/common/http'
import {Router, CanActivate, ActivatedRouteSnapshot} from '@angular/router'
import {tap} from 'rxjs/operators'

type valueof<T> = T[keyof T]

@Injectable({
  providedIn: 'root',
})
export class AuthService implements CanActivate {
  errorMessage = ''
  user: Scrum.User = {email: '', pk: null, displayName: '', is_PM: false}

  constructor(private http: HttpClient, private router: Router) {}

  isAuthenticated() {
    // TODO: is this a bad idea to hit the backend on any route change?  Let's say no!
    return this.http
      .get<Scrum.User>('api/is_authenticated')
      .pipe(tap(user => (this.user = user)))
  }
  requestWebsocketAuthToken() {
    return this.http.get('api/get_websocket_auth_token')
  }

  getUserInfo() {
    return this.user
  }

  checkCredentials(
    user: {email: string; password: string},
    redirectTo: string | null = null
  ) {
    this.errorMessage = ''
    this.http.post('/api/login', {...user}).subscribe(
      success => {
        this.user.email = user.email
        const redirectDefault = this.user.is_PM ? '/pm_tools' : '/app/dashboard'
        this.router.navigate([redirectTo || redirectDefault])
      },
      error => {
        this.errorMessage = "Invalid Credentials!  We've got a saboteur!"
        this.user = {email: '', pk: null, displayName: '', is_PM: false}
      }
    )
    return false
  }

  logout() {
    this.http.get('/api/logout').subscribe(
      () => this.router.navigate(['/login']),
      () => this.router.navigate(['/login'])
    )
  }

  queryUser(property: string) {
    return this?.user[property] ?? null
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
