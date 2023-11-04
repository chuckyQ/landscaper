import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-time-table-modal',
  templateUrl: './time-table-modal.component.html',
  styleUrls: ['./time-table-modal.component.scss']
})
export class TimeTableModalComponent {

  @Input()
  date: string

  @Input()
  time: string

  constructor(public activeModal: NgbActiveModal) {
    this.date = ""
    this.time = ""
  }

}
