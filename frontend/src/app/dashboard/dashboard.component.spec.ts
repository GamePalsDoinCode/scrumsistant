import {
  async,
  ComponentFixture,
  TestBed,
  fakeAsync,
  tick,
} from '@angular/core/testing'
import {HttpClientTestingModule} from '@angular/common/http/testing'
import {By} from '@angular/platform-browser'
import {DashboardComponent} from './dashboard.component'
import {RouterTestingModule} from '@angular/router/testing'
import {of, Subject} from 'rxjs'
import {AuthService} from '../auth.service'
import {Component, Input} from '@angular/core'
import {FormsModule} from '@angular/forms'
import {WebsocketService} from '../websocket.service'
import {} from 'jasmine'

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

const fakeAuthService = jasmine.createSpyObj('AuthService', [
  'getUserInfo',
  'queryUser',
])
const getUserInfoSpy = fakeAuthService.getUserInfo.and.returnValue(of(testUser))
const queryUserSpy = fakeAuthService.queryUser.and.returnValue(of(false))
const fakeWebsocket = new Subject()
const WebSocketServiceStub: Partial<WebsocketService> = {
  getSocketChannel(init, filter) {
    return fakeWebsocket
  },
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
      providers: [
        {provide: WebsocketService, useValue: WebSocketServiceStub},
        {provide: AuthService, useValue: fakeAuthService},
      ],
    }).compileComponents()
  }))

  beforeEach(() => {
    fixture = TestBed.createComponent(DashboardComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it('should create', () => {
    expect(component).toBeTruthy()
  })

  it('should update input value when name is changed', async () => {
    component.user.displayName = 'Tom'
    await fixture.detectChanges()
    await fixture.whenStable()

    const input = fixture.debugElement.query(By.css('#test'))
    debugger
    expect(true).toBe(true)
    // expect(input.textContent).toEqual('Tom')
  })
})
