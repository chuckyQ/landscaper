import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddJobYearlyComponent } from './add-job-yearly.component';

describe('AddJobYearlyComponent', () => {
  let component: AddJobYearlyComponent;
  let fixture: ComponentFixture<AddJobYearlyComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AddJobYearlyComponent]
    });
    fixture = TestBed.createComponent(AddJobYearlyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
