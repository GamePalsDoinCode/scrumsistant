import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';


@Injectable({
  providedIn: 'root'
})
export class AuthService {

  errorMessage = ''

  constructor(
    private http: HttpClient,
    private router: Router,
  ) { }

  isAuthenticated() {
    // TODO: is this a bad idea to hit the backend on any route change?
    return this.http.get('api/is_authenticated')
  }

  checkCredentials(user: {email: string, password: string}, redirectTo: string | null = null){
    this.errorMessage = ''
    this.http.post('/api/login', {...user}).subscribe(
      success => {
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

  logout(){
    this.http.get('/api/logout').subscribe(
      () => this.router.navigate(['/login']),
      () => this.router.navigate(['/login']),
    )
  }

  
}
