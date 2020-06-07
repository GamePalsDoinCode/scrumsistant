import {async, ComponentFixture, TestBed} from '@angular/core/testing'
import {HttpClientTestingModule} from '@angular/common/http/testing'
import {DashboardComponent} from './dashboard.component'
import {RouterTestingModule} from '@angular/router/testing'
import {of} from 'rxjs'
import {AuthService} from '../auth.service'
import {Component, Input} from '@angular/core'
import {FormsModule} from '@angular/forms'

@Component({selector: 'app-nav', template: ''})
class NavComponentStub {
  @Input() showSecondaryLinks = false
}

@Component({selector: 'app-current-team', template: ''})
class CurrentTeamComponentStub {}

const testUser: Scrum.User = {
  displayName: 'User Display Name',
  pk: 1,
  email: 'user@user.com',
  is_PM: false,
}

const authServiceStub: Partial<AuthService> = {
  getUserInfo: () => of(testUser),
  queryUser: (prop: keyof Scrum.User) => of(testUser[prop]),
}

describe('DashboardComponent', () => {
  let component: DashboardComponent
  let fixture: ComponentFixture<DashboardComponent>

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        DashboardComponent,
        NavComponentStub,
        CurrentTeamComponentStub,
      ],
      imports: [HttpClientTestingModule, RouterTestingModule, FormsModule],
      providers: [{provide: AuthService, useValue: authServiceStub}],
    }).compileComponents()
  }))

  beforeEach(() => {
    fixture = TestBed.createComponent(DashboardComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it('should create', () => {
    component.ngOnInit()
    expect(component).toBeTruthy()
  })
})
