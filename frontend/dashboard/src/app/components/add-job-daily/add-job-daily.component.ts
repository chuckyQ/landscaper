import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/services/auth.service';

interface DailyJob {
  isSeasonal: boolean // always true
  seasonalType: string // always 'daily'

  startDate: string // ISO date
  startMonth: number // index of month (zero-based)
  startDay: number // specific date of month (November 9) -> 9
  startTimestamp: number // Unix timestamp in milliseconds
  startWeekday: number // Weekday index (Sunday -> 1, Monday -> 2, etc.)

  endDate: string // ISO date
  endMonth: number // index of month (zero-based)
  endDay: number // specific date of month (November 9) -> 9
  endTimestamp: number // Unix timestamp in milliseconds
  endWeekday: number // Weekday index (Sunday -> 1, Monday -> 2, etc.)

  name: string // Customer name
  address: string
  custID: string
  crews: string[] // List of crew ids
  notes: string
}

@Component({
  selector: 'add-job-daily',
  templateUrl: './add-job-daily.component.html',
  styleUrls: ['./add-job-daily.component.scss']
})
export class AddJobDailyComponent {

  @Input()
  custName: string

  @Input()
  address: string

  @Input()
  custID: string

  @Input()
  notes: string

  @Input()
  mainFormIsValid: boolean | null

  @Input()
  crewIDs: string[]

  constructor(public service: AuthService, public activeModal: NgbActiveModal) {
    this.custID = ""
    this.address = ""
    this.custName = ""
    this.mainFormIsValid = false
    this.notes = ""
    this.crewIDs = []

  }

  createDailyJob(startDate: string, endDate: string) {

    function getMonth(dt: string) {
      let d = new Date(dt)
      return [d.getTime(), d.getMonth(), d.getDate(), d.getDay()]
    }

    let [startTimestamp, startMonth, startDayOfMonth, startWeekday] = getMonth(startDate)
    let [endTimestamp, endMonth, endDayOfMonth, endWeekday] = getMonth(endDate)

    let d: DailyJob = {
      isSeasonal: true,
      seasonalType: "daily",

      startDate: startDate.split("T")[0],
      startTimestamp: startTimestamp,
      startMonth: startMonth,
      startDay: startDayOfMonth,
      startWeekday: startWeekday,

      endDate: endDate.split("T")[0],
      endTimestamp: endTimestamp,
      endMonth: endMonth,
      endDay: endDayOfMonth,
      endWeekday: endWeekday,

      name: this.custName,
      address: this.address,
      custID: this.custID,
      notes: this.notes,
      crews: this.crewIDs,
    }

  this.service.postJob(d).subscribe(
    {
    next: (resp: any) => {
      alert("Job created!")
      this.activeModal.close()
      window.location.reload()
    }
    }
  )

}

}
