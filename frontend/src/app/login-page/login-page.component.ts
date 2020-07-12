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
  buttonThinking = false

  constructor(private authService: AuthService) {}

  ngOnInit(): void {}

  submitLogin() {
    this.buttonText = 'wait...'
    this.buttonThinking = true
    const credsOk = this.authService.checkCredentials(this.potentialUser)
    if (!credsOk) {
      this.buttonText = 'login'
      this.buttonThinking = false
    }
  }
}
