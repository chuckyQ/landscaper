import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { TimeTableModalComponent } from 'src/app/components/time-table-modal/time-table-modal.component';
import { AuthService } from 'src/app/services/auth.service';

interface Timeslot {
  time: string
  hasEvent: boolean
  length: number // Number of rows to span
  date: string
}

function zfill(n: number) {

  if(n < 10) {
    return `0${n}`
  }

  return n.toString()

}

interface Job {
  address: string
  notes: string
}

@Component({
  selector: 'app-calendar-day',
  templateUrl: './calendar-day.component.html',
  styleUrls: ['./calendar-day.component.scss']
})
export class CalendarDayComponent {

  year: number | null
  month: number | null
  day: number | null
  date: string
  startTimestamp: number
  endTimestamp: number
  jobs: Job[]

  constructor(public modal: NgbModal, public ar: ActivatedRoute, public service: AuthService) {


    this.year = null
    this.month = null
    this.day = null
    this.date = ""
    this.startTimestamp = -1
    this.endTimestamp = -1
    this.jobs = []

    let year = this.ar.snapshot.paramMap.get('year')
    let month = this.ar.snapshot.paramMap.get('month')
    let day = this.ar.snapshot.paramMap.get('day')

    if(year === null || month === null || day === null) {
      return
    }

    this.year = +year
    this.month = +month
    this.day = +day

    this.startTimestamp = new Date(this.year, this.month - 1, this.day - 1).getTime()
    this.endTimestamp = new Date(this.year, this.month - 1 , this.day).getTime()

    this.date = `${this.year}-${this.month}-${this.day}`

    this.service.getJobBetweenTimestamps(this.startTimestamp, this.endTimestamp)
    .subscribe(
      {
        next: (resp: any) => {
          this.jobs = resp
        }
      }
    )

  }

}
