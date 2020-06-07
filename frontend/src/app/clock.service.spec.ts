import {TestBed} from '@angular/core/testing'
import {HttpClientTestingModule} from '@angular/common/http/testing'

import {ClockService} from './clock.service'

describe('ClockService', () => {
  let service: ClockService

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
    })
    service = TestBed.inject(ClockService)
  })

  it('should be created', () => {
    expect(service).toBeTruthy()
  })
})
