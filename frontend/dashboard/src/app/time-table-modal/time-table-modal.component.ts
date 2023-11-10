import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

interface Crew {
  name: string
  selected: boolean
}

function zfill(n: number) {

  if(n < 10) {
    return `0${n}`
  }

  return n.toString()

}

// Number of timeslots in a day
// at 30min increments.
const NUM_OF_TIMESLOTS = 24 * 2

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

  timeslots: string[]

  constructor(public activeModal: NgbActiveModal) {
    this.date = ""
    this.time = ""

    this.timeslots = []

    var j = 0;
    for(let i = 0; i < NUM_OF_TIMESLOTS; i++) {
      if(i % 2 == 0) {
        this.timeslots.push(`${zfill(j)}:00:00`)
        continue
      }
      this.timeslots.push(`${zfill(j)}:30:00`)
    }


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
