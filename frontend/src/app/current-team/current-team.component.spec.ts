import {async, ComponentFixture, TestBed} from '@angular/core/testing'
import {HttpClientTestingModule} from '@angular/common/http/testing'
import {CurrentTeamComponent} from './current-team.component'
import {RouterTestingModule} from '@angular/router/testing'

describe('CurrentTeamComponent', () => {
  let component: CurrentTeamComponent
  let fixture: ComponentFixture<CurrentTeamComponent>

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [CurrentTeamComponent],
      imports: [HttpClientTestingModule, RouterTestingModule],
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
