import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot } from '@angular/router';

import { AuthService } from './auth.service'

@Injectable({
  providedIn: 'root'
})
export class NonAuthGuardService implements CanActivate {

  constructor() { }
  
  async canActivate(route: ActivatedRouteSnapshot){
    // TODO: this should probably be moved into its own AuthGuard service
    // TODO theres _def_ a better way to do this with something out of rxjs - find!
      // tbh having the endpoint return something instead of error codes and using map might be nicer?
    try{
      await this.isAuthenticated().toPromise()
      return true
    } catch (_){
      this.router.navigate(['/login'])
      return false
    }
  }
}
