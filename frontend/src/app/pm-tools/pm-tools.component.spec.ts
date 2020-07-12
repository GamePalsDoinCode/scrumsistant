import {async, ComponentFixture, TestBed} from '@angular/core/testing'
import {HttpClientTestingModule} from '@angular/common/http/testing'

import {PmToolsComponent} from './pm-tools.component'

describe('PmToolsComponent', () => {
  let component: PmToolsComponent
  let fixture: ComponentFixture<PmToolsComponent>

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [PmToolsComponent],
      imports: [HttpClientTestingModule],
    }).compileComponents()
  }))

  beforeEach(() => {
    fixture = TestBed.createComponent(PmToolsComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it('should create', () => {
    expect(component).toBeTruthy()
  })
})
