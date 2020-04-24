import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';


@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private _isAuthenticated = false
  private sessionExpireTime = new Date() // god I hope I don't regret not using moment at the get go
  errorMessage = ''

  constructor(
    private http: HttpClient,
    private router: Router,
  ) { }

  isAuthenticated() {
    return (
      new Date() < this.sessionExpireTime &&
      this._isAuthenticated
     )
  }

  checkCredentials(user: {email: string, password: string}, redirectTo: string | null = null){
    this.errorMessage = ''
    this.http.post('/api/login', {...user}).subscribe(
      success => {
        this._isAuthenticated = true
        this.sessionExpireTime = new Date(this.sessionExpireTime.setFullYear(2021)) // TODO tmp, get expire time from backend
        this.router.navigate([redirectTo || '/app/dashboard'])
      },
      error => {
        this.errorMessage = "Invalid Credentials!  We've got a saboteur!"
       }
      )
    return false
  }

  checkSessionCookie(){
    console.log('checking if already logged in')
    return false
  }

}
