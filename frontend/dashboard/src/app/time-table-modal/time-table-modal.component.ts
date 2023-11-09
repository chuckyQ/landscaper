import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

interface Crew {
  name: string
  selected: boolean
}


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

  crews: Crew[]

  constructor(public activeModal: NgbActiveModal) {
    this.date = ""
    this.time = ""

    this.crews = [
      {
        name: "Gutters",
        selected: false,
      },
      {
        name: "Lawn Care",
        selected: false,
      }
    ]

  }

  createJob(dt: string, name: string, address: string) {
  }

}
