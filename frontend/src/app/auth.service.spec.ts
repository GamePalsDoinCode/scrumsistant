import {
  HttpClientTestingModule,
  HttpTestingController,
} from '@angular/common/http/testing'
import {AuthService} from './auth.service'
import {RouterTestingModule} from '@angular/router/testing'
import {TestBed, getTestBed, fakeAsync, tick} from '@angular/core/testing'

const testUser: Scrum.User = {
  displayName: 'User Display Name',
  pk: 1,
  email: 'user@user.com',
  is_PM: false,
}

let httpMock: HttpTestingController

describe('AuthService', () => {
  let service: AuthService
  let injector: TestBed

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule, RouterTestingModule],
    })
    service = TestBed.inject(AuthService)
    injector = getTestBed()
    httpMock = injector.get(HttpTestingController)
  })

  it('should be created', () => {
    expect(service).toBeTruthy()
  })

  it('should get properties of authenticated user', async () => {
    service.user = testUser
    Object.entries(testUser).forEach(async ([key, val]) => {
      const queriedVal = await service.queryUser(key).toPromise()
      expect(queriedVal).toEqual(testUser[key])
    })
  })
  it('should get the entire authenticated user', async () => {
    service.user = testUser
    const queriedUser = await service.getUserInfo().toPromise()
    expect(queriedUser).toBe(testUser)
  })

  it('should return the authed user when creds are right', () => {
    ;(service as any)
      .submitCreds('rightemail@email.com', 'goodPassword')
      .subscribe((ret: {user: Scrum.User; auth: string}) => {
        expect(ret.user).toEqual(testUser)
      })
    const request = httpMock.expectOne('/api/login')
    request.flush({user: testUser})
    expect(request.request.method).toBe('POST')
  })
})
