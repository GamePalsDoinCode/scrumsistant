import {TestBed} from '@angular/core/testing'

import {PmCanActivateService} from './pm-can-activate.service'

describe('PmCanActivateService', () => {
  let service: PmCanActivateService

  beforeEach(() => {
    TestBed.configureTestingModule({})
    service = TestBed.inject(PmCanActivateService)
  })

  it('should be created', () => {
    expect(service).toBeTruthy()
  })
})
