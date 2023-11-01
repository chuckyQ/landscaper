import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CalendarCreateJobModalComponent } from './calendar-create-job-modal.component';

describe('CalendarCreateJobModalComponent', () => {
  let component: CalendarCreateJobModalComponent;
  let fixture: ComponentFixture<CalendarCreateJobModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CalendarCreateJobModalComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CalendarCreateJobModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
