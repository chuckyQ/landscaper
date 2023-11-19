import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddJobWeeklyComponent } from './add-job-weekly.component';

describe('AddJobWeeklyComponent', () => {
  let component: AddJobWeeklyComponent;
  let fixture: ComponentFixture<AddJobWeeklyComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AddJobWeeklyComponent]
    });
    fixture = TestBed.createComponent(AddJobWeeklyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
