import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private _isAuthenticated = false
  private sessionExpireTime = Date.now() // god I hope I don't regret not using moment at the get go


  constructor() { }

  isAuthenticated() {
    return Date.now() < this.sessionExpireTime && this._isAuthenticated
  }

  checkCredentials(user: {email: string, password: string}){
    console.log('checking to see if ', user, ' is valid')
    return false
  }

  checkSessionCookie(){
    console.log('checking if already logged in')
    return false
  }

}
