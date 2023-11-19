import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddJobMonthlyComponent } from './add-job-monthly.component';

describe('AddJobMonthlyComponent', () => {
  let component: AddJobMonthlyComponent;
  let fixture: ComponentFixture<AddJobMonthlyComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AddJobMonthlyComponent]
    });
    fixture = TestBed.createComponent(AddJobMonthlyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
