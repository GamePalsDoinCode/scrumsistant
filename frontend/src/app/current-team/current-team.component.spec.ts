import {async, ComponentFixture, TestBed} from '@angular/core/testing'

import {CurrentTeamComponent} from './current-team.component'

describe('CurrentTeamComponent', () => {
  let component: CurrentTeamComponent
  let fixture: ComponentFixture<CurrentTeamComponent>

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [CurrentTeamComponent],
    }).compileComponents()
  }))

  beforeEach(() => {
    fixture = TestBed.createComponent(CurrentTeamComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it('should create', () => {
    expect(component).toBeTruthy()
  })
})
