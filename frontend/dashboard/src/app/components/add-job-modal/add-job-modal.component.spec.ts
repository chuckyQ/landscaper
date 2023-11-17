import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddJobModalComponent } from './add-job-modal.component';

describe('AddJobModalComponent', () => {
  let component: AddJobModalComponent;
  let fixture: ComponentFixture<AddJobModalComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AddJobModalComponent]
    });
    fixture = TestBed.createComponent(AddJobModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
