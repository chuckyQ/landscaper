import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/services/auth.service';

interface MonthlyJob {
  isRecurring: boolean // always true
  recurringType: string // always 'monthly'
  startDate: string // date
  endDate: string // date or empty string
  useEndDate: boolean
  recurrences: number // number of recurrences
  day: number // Specific date (1, 2...31)
  custID: string
  crews: string[] // List of crew ids
  notes: string

  isSpecificDay: boolean // On a specific month and day or not (ex every first Sunday)
  // (first -> 1, second -> 2, third -> 3, fourth -> 4, last -> 5)
  ordinal: number
  nMonths: number
  weekday: number
}

@Component({
  selector: 'add-job-monthly',
  templateUrl: './add-job-monthly.component.html',
  styleUrls: ['./add-job-monthly.component.scss']
})
export class AddJobMonthlyComponent {

  @Input()
  custID: string

  @Input()
  notes: string

  @Input()
  mainFormIsValid: boolean | null

  @Input()
  crewIDs: string[]

  @Input()
  startDate: string
  endDate: string
  useEndDate: boolean
  useEndAfter: boolean
  recurrences: number
  recurringIsValid: boolean

  days: string[]

  certainDay: boolean
  certainDate: boolean

  constructor(public service: AuthService, public activeModal: NgbActiveModal) {
    this.custID = ""
    this.notes = ""
    this.mainFormIsValid = false

    this.startDate = ""
    this.endDate = ""
    this.useEndDate = true
    this.useEndAfter = false
    this.recurrences = 1
    this.recurringIsValid = false

    this.certainDay = true
    this.certainDate = false

    this.crewIDs = []

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

  createMonthlyJob(day: number, nMonths: number,
                   ordinal: number, weekday: number, nMonths2: number,
                   certainDate: boolean) {

    var months = -1
    if(this.certainDay) {
      // Every 1 day every 2 months
      months = nMonths
    } else {
      // Every first Monday every 2 months
      months = nMonths2
    }

    let d: MonthlyJob = {
      isRecurring: true,
      recurringType: "monthly",

      custID: this.custID,
      notes: this.notes,
      crews: this.crewIDs,
      useEndDate: !this.useEndAfter,
      startDate: this.startDate,
      endDate: this.endDate,
      recurrences: this.recurrences,

      // Day 2 of every N months
      day: day,
      nMonths: months,

      // Every first Monday of N months
      isSpecificDay: certainDate,
      ordinal: ordinal,
      weekday: weekday,
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
    this.certainDay = !this.certainDay
    this.certainDate = !this.certainDate
  }

  daySelection() {

    // Generate a list containing the numbers
    // [1-31] inclusive
    let values: number[] = []
    for(let i = 0; i < 31; i++) {
      values.push(i + 1)
    }

    return values
  }

  setValid(event: boolean) {
    this.recurringIsValid = event
  }

}
