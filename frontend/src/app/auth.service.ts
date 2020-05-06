import {Injectable} from '@angular/core'
import {HttpClient} from '@angular/common/http'
import {Router, CanActivate, ActivatedRouteSnapshot} from '@angular/router'

@Injectable({
  providedIn: 'root',
})
export class AuthService implements CanActivate {
  errorMessage = ''
  user: Scrum.User = {email: '', pk: null, displayName: ''}

  constructor(private http: HttpClient, private router: Router) {}

  isAuthenticated() {
    // TODO: is this a bad idea to hit the backend on any route change?
    return this.http.get('api/is_authenticated')
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
        this.router.navigate([redirectTo || '/app/dashboard'])
      },
      error => {
        this.errorMessage = "Invalid Credentials!  We've got a saboteur!"
        this.user = {email: '', pk: null, displayName: ''}
      }
    )
    return false
  }

  checkSessionCookie() {
    console.log('checking if already logged in')
    return false
  }

  logout() {
    this.http.get('/api/logout').subscribe(
      () => this.router.navigate(['/login']),
      () => this.router.navigate(['/login'])
    )
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
