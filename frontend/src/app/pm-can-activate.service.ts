import {Injectable} from '@angular/core'
import {Router, CanActivate, ActivatedRouteSnapshot} from '@angular/router'
import {AuthService} from './auth.service'
@Injectable({
  providedIn: 'root',
})
export class PmCanActivateService implements CanActivate {
  constructor(private authService: AuthService) {}

  async canActivate(route: ActivatedRouteSnapshot) {
    const isPM = await this.authService.queryUser('is_PM').toPromise()
    return !!isPM
  }
}
