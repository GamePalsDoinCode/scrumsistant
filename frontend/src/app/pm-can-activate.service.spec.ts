import {TestBed} from '@angular/core/testing'
import {HttpClientTestingModule} from '@angular/common/http/testing'

import {PmCanActivateService} from './pm-can-activate.service'
import {RouterTestingModule} from '@angular/router/testing'

describe('PmCanActivateService', () => {
  let service: PmCanActivateService

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule, RouterTestingModule],
    })
    service = TestBed.inject(PmCanActivateService)
  })

  it('should be created', () => {
    expect(service).toBeTruthy()
  })
})
