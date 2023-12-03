import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/services/auth.service';

interface MonthlyJob {
  isRecurring: boolean // always true
  recurringType: string // always 'monthly'
  startDate: string // date
  endDate: string // date or empty string
  recurrences: number // number of recurrences
  day: number // index of weekday (0-Sunday, 1-Monday, etc...)
  custID: string
  crews: string[] // List of crew ids
  notes: string

  isSpecificDay: boolean // On a specific month and day or not (ex every first Sunday)
  // (first -> 1, second -> 2, third -> 3, fourth -> 4, last -> 5)
  nDay: number | null
}

interface Day {
  name: string
  selected: boolean
  index: number
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

  days: Day[]

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
      { name: "Sunday", selected: false, index: 0},
      { name: "Monday", selected: false, index: 1},
      { name: "Tuesday", selected: false, index: 2},
      { name: "Wednesday", selected: false, index: 3},
      { name: "Thursday", selected: false, index: 4},
      { name: "Friday", selected: false ,index: 5},
      { name: "Saturday", selected: false, index: 6},
    ]

  }

  createMonthlyJob(isSpecificDay: boolean, nDay: number, day: number) {

    let d: MonthlyJob = {
      isRecurring: true,
      recurringType: "monthly",
      day: day,
      custID: this.custID,
      notes: this.notes,
      crews: this.crewIDs,
      startDate: this.startDate,
      endDate: this.endDate,
      recurrences: this.recurrences,

      // The "first" Sunday of every month (not specific date)
      isSpecificDay: isSpecificDay,
      nDay: nDay,
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
