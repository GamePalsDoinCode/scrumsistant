import {HttpClientTestingModule} from '@angular/common/http/testing'
import {Component, Input} from '@angular/core'
import {FormsModule} from '@angular/forms'
import {By} from '@angular/platform-browser'
import {RouterTestingModule} from '@angular/router/testing'
import {} from 'jasmine'
import {of, Subject} from 'rxjs'
import {AuthService} from '../auth.service'
import {UserService} from '../user.service'
import {WebsocketService} from '../websocket.service'
import {DashboardComponent} from './dashboard.component'

import {
  async,
  ComponentFixture,
  TestBed,
  fakeAsync,
  tick,
} from '@angular/core/testing'

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
  'logout',
])
const getUserInfoSpy = fakeAuthService.getUserInfo.and.returnValue(of(testUser))
const queryUserSpy = fakeAuthService.queryUser.and.returnValue(of(false))
const logoutSpy = fakeAuthService.logout.and.returnValue()

const fakeUserService = jasmine.createSpyObj('UserService', ['save'])
const userSaveSpy = fakeUserService.save.and.returnValue()

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
        {provide: UserService, useValue: fakeUserService},
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

  it('should call user save when save is clicked', fakeAsync(() => {
    const saveButton = fixture.debugElement.query(By.css('#saveButton'))
    saveButton.nativeElement.click()
    tick()
    expect(userSaveSpy).toHaveBeenCalled()
  }))

  it('should have the websocket hooks linked up properly', fakeAsync(() => {
    spyOn(component, 'handleIncoming')
    spyOn(window.console, 'log')
    fakeWebsocket.next('normal message')
    tick()
    expect(component.handleIncoming).toHaveBeenCalled()
    fakeWebsocket.error('error!')
    tick()
    expect(window.console.log).toHaveBeenCalledTimes(1)
  }))
  it('should call auth logout when logout button is clicked', fakeAsync(() => {
    const logoutButton = fixture.debugElement.query(
      By.css('div.ceremonyContainer > button:nth-child(4)')
    ) // obv this is a hack shortcut while I wait for someone to style the page
    logoutButton.nativeElement.click()
    tick()
    expect(logoutSpy).toHaveBeenCalled()
  }))
})
