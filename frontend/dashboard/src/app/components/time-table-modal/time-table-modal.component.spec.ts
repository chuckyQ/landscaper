import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TimeTableModalComponent } from './time-table-modal.component';

describe('TimeTableModalComponent', () => {
  let component: TimeTableModalComponent;
  let fixture: ComponentFixture<TimeTableModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TimeTableModalComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TimeTableModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
