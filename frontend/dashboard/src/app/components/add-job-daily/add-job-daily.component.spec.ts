import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddJobDailyComponent } from './add-job-daily.component';

describe('AddJobDailyComponent', () => {
  let component: AddJobDailyComponent;
  let fixture: ComponentFixture<AddJobDailyComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AddJobDailyComponent]
    });
    fixture = TestBed.createComponent(AddJobDailyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
