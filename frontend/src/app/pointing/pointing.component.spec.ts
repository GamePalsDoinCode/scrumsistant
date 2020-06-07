import {async, ComponentFixture, TestBed} from '@angular/core/testing'

import {PointingComponent} from './pointing.component'
import {Component} from '@angular/core'

@Component({selector: 'app-nav', template: ''})
class NavComponentStub {}

describe('PointingComponent', () => {
  let component: PointingComponent
  let fixture: ComponentFixture<PointingComponent>

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [PointingComponent, NavComponentStub],
    }).compileComponents()
  }))

  beforeEach(() => {
    fixture = TestBed.createComponent(PointingComponent)
    component = fixture.componentInstance
    fixture.detectChanges()
  })

  it('should create', () => {
    expect(component).toBeTruthy()
  })
})
