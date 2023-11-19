import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddJobSingleComponent } from './add-job-single.component';

describe('AddJobSingleComponent', () => {
  let component: AddJobSingleComponent;
  let fixture: ComponentFixture<AddJobSingleComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AddJobSingleComponent]
    });
    fixture = TestBed.createComponent(AddJobSingleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
