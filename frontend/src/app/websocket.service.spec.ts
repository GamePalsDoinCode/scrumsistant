import {WebsocketService} from './websocket.service'
import {
  HttpClientTestingModule,
  HttpTestingController,
} from '@angular/common/http/testing'
import {TestBed, getTestBed} from '@angular/core/testing'

describe('WebsocketService', () => {
  let service: WebsocketService
  let injector: TestBed
  let httpMock: HttpTestingController

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
    })
    service = TestBed.inject(WebsocketService)
    injector = getTestBed()
    httpMock = injector.inject(HttpTestingController)
  })

  it('should be created', () => {
    expect(service).toBeTruthy()
  })

  it('should hit the right api', () => {
    const testResponse = {
      signedToken: 'hello',
      verifyKey: 'yes',
    }
    service.requestWebsocketAuthToken().subscribe(resp => {
      expect(resp).toBe(testResponse)
    })
    const req = httpMock.expectOne('api/get_websocket_auth_token')
    req.flush(testResponse)
  })
})
