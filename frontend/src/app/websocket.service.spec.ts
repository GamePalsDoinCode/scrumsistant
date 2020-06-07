import {TestBed} from '@angular/core/testing'

import {WebsocketService} from './websocket.service'
import {HttpClientTestingModule} from '@angular/common/http/testing'

describe('WebsocketService', () => {
  let service: WebsocketService

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
    })
    service = TestBed.inject(WebsocketService)
  })

  it('should be created', () => {
    expect(service).toBeTruthy()
  })
})
