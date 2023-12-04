import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/services/auth.service';

interface YearlyJob {
  isRecurring: boolean // always true
  recurringType: string // Always 'yearly'
  month: number // index of month (0-Jan, 1-Feb, etc...)
  day: number // Day of month (1-31)
  startDate: string
  endDate: string
  endAfter: number
  recurrences: number
  useEndDate: boolean
  custID: string
  crews: string[] // List of crew ids
  notes: string
  ordinal: number
  weekday: number
}


@Component({
  selector: 'add-job-yearly',
  templateUrl: './add-job-yearly.component.html',
  styleUrls: ['./add-job-yearly.component.scss']
})
export class AddJobYearlyComponent {

  @Input()
  custID: string

  @Input()
  notes: string

  @Input()
  mainFormIsValid: boolean | null

  @Input()
  crewIDs: string[]

  months: string[]
  days: string[]

  every: boolean
  onEvery: boolean

  @Input()
  startDate: string
  endDate: string
  useEndAfter: boolean
  recurrences: number
  recurringIsValid: boolean

  constructor(public service: AuthService, public activeModal: NgbActiveModal) {
    this.custID = ""
    this.notes = ""
    this.mainFormIsValid = false
    this.crewIDs = []

    this.startDate = ""
    this.endDate = ""
    this.useEndAfter = false
    this.recurrences = 1
    this.recurringIsValid = false

    this.every = true
    this.onEvery = false

    this.months = [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ]

    this.days = [
      "Sunday",
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday",
    ]

  }

  getMonthDays(monthIndex: number) {

    let i = 0
    let days: number[] = []
    while(true) {
      // We use 2023 as a base year because
      // it does not have a leap day
      let dt = new Date(2023, monthIndex, i + 1)

      if(monthIndex === 11) {
        // Case of December
        if(dt.getMonth() == 0) {
          break
        }
      }

      if (dt.getMonth() == monthIndex + 1) {
        break
      }

      days.push(i + 1)
      i++

    }

    return days

  }

  createYearlyJob(month: number, day: number, ordinal: number, weekday: number) {

    let d: YearlyJob = {
      isRecurring: true,
      recurringType: "yearly",
      month: month,
      day: day,
      notes: this.notes,
      crews: this.crewIDs,
      custID: this.custID,
      weekday: weekday,
      ordinal: ordinal,
      recurrences: this.recurrences,
      startDate: this.startDate,
      endDate: this.endDate,
      endAfter: this.recurrences,
      useEndDate: !this.useEndAfter,
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

  toggle() {
    this.every = !this.every
    this.onEvery = !this.onEvery
  }

  setValid(event: boolean) {
    this.recurringIsValid = event
  }

}
