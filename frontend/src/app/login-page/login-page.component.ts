import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.scss']
})
export class LoginPageComponent implements OnInit {

  potentialUser = {
    email: '',
    password: '',
  }

  constructor() { }

  ngOnInit(): void {
  }

  submitLogin(){
    console.log(this.potentialUser)
  }

}
