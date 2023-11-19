import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/services/auth.service';

interface MonthlyJob {
  isSeasonal: boolean // always true
  seasonalType: string // always 'monthly'
  startMonth: number // index of month (zero-based)
  endMonth: number // index of month (zero-based)
  numOfWeeks: number // every 2 weeks, every 3 weeks, etc...
  day: number // index of weekday (0-Sunday, 1-Monday, etc...)
  name: string // Customer name
  address: string
  custID: string
  crews: string[] // List of crew ids
  notes: string
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

  days: Day[]

  constructor(public service: AuthService, public activeModal: NgbActiveModal) {
    this.custID = ""
    this.address = ""
    this.custName = ""
    this.notes = ""
    this.mainFormIsValid = false

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

  createMonthlyJob(name: string, address: string,
    notes: string, startMonth: string,
    endMonth: string, numOfWeeks: number,
    day: string) {


    let d: MonthlyJob = {
      isSeasonal: true,
      seasonalType: "monthly",
      startMonth: this.months.indexOf(startMonth),
      endMonth: this.months.indexOf(endMonth),
      numOfWeeks: numOfWeeks,
      day: Object.keys(this.days).indexOf(day),
      name: name,
      address: address,
      custID: this.custID,
      notes: notes,
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
