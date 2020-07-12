import {async, ComponentFixture, TestBed} from '@angular/core/testing'
import {HttpClientTestingModule} from '@angular/common/http/testing'
import {LoginPageComponent} from './login-page.component'
import {RouterTestingModule} from '@angular/router/testing'
import {FormsModule} from '@angular/forms'

describe('LoginPageComponent', () => {
  let component: LoginPageComponent
  let fixture: ComponentFixture<LoginPageComponent>

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [LoginPageComponent],
      imports: [HttpClientTestingModule, RouterTestingModule, FormsModule],
    }).compileComponents()
  }))

  beforeEach(() => {
    fixture = TestBed.createComponent(LoginPageComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it('should create', () => {
    expect(component).toBeTruthy()
  })
})
