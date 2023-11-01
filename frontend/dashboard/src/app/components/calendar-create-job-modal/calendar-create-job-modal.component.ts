import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-calendar-create-job-modal',
  templateUrl: './calendar-create-job-modal.component.html',
  styleUrls: ['./calendar-create-job-modal.component.scss']
})
export class CalendarCreateJobModalComponent {

  @Input()
  dt: Date

  @Input()
  jobIDs: string[]

  constructor(public activeModal: NgbActiveModal) {

    this.dt = new Date()
    this.jobIDs = []

  }

}
