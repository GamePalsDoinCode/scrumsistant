import {async, ComponentFixture, TestBed} from '@angular/core/testing'

import {StandupComponent} from './standup.component'
import {Component} from '@angular/core'

@Component({selector: 'app-nav', template: ''})
class NavComponentStub {}

describe('StandupComponent', () => {
  let component: StandupComponent
  let fixture: ComponentFixture<StandupComponent>

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [StandupComponent, NavComponentStub],
    }).compileComponents()
  }))

  beforeEach(() => {
    fixture = TestBed.createComponent(StandupComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it('should create', () => {
    expect(component).toBeTruthy()
  })
})
