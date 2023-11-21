import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/services/auth.service';

interface MonthlyJob {
  isSeasonal: boolean // always true
  seasonalType: string // always 'monthly'
  startMonth: number // index of month (zero-based)
  endMonth: number // index of month (zero-based)
  day: number // index of weekday (0-Sunday, 1-Monday, etc...)
  name: string // Customer name
  address: string
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

  months: string[]
  startMonth: number
  endMonth: number

  days: Day[]

  certainDay: boolean
  certainDate: boolean

  constructor(public service: AuthService, public activeModal: NgbActiveModal) {
    this.custID = ""
    this.address = ""
    this.custName = ""
    this.notes = ""
    this.mainFormIsValid = false

    this.startMonth = 3
    this.endMonth = 7

    this.certainDay = true
    this.certainDate = false

    this.crewIDs = []

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
      { name: "Sunday", selected: false, index: 0},
      { name: "Monday", selected: false, index: 1},
      { name: "Tuesday", selected: false, index: 2},
      { name: "Wednesday", selected: false, index: 3},
      { name: "Thursday", selected: false, index: 4},
      { name: "Friday", selected: false ,index: 5},
      { name: "Saturday", selected: false, index: 6},
    ]

  }

  createMonthlyJob(startMonth: number, endMonth: number,
    isSpecificDay: boolean, nDay: number, day: number) {

    let d: MonthlyJob = {
      isSeasonal: true,
      seasonalType: "monthly",
      startMonth: startMonth,
      endMonth: endMonth,
      day: day,
      name: this.custName,
      address: this.address,
      custID: this.custID,
      notes: this.notes,
      crews: this.crewIDs,

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

  getMonthRange() {

    let values: number[] = []
    for(let i = 0; i < Math.abs(this.startMonth - this.endMonth) + 1; i++) {
      values.push(i + 1)
    }
    return values
  }

}
