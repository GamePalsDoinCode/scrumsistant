import { TestBed } from '@angular/core/testing';

import { NonAuthGuardService } from './non-auth-guard.service';

describe('NonAuthGuardService', () => {
  let service: NonAuthGuardService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(NonAuthGuardService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
