import {Component, OnInit} from '@angular/core'
import {AuthService} from '../auth.service'

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.scss'],
})
export class LoginPageComponent implements OnInit {
  potentialUser = {
    email: '',
    password: '',
  }

  buttonText = 'login'

  constructor(private authService: AuthService) {}

  ngOnInit(): void {}

  submitLogin() {
    this.buttonText = 'wait...'
    this.authService.checkCredentials(this.potentialUser)
  }
}
