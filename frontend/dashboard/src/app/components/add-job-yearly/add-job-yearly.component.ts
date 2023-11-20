import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/services/auth.service';

interface YearlyJob {
  isSeasonal: boolean // always true
  seasonalType: string // Always 'yearly'
  month: number // index of month (0-Jan, 1-Feb, etc...)
  day: number // index of weekday (0-Sunday, 1-Monday, etc...)
  name: string // Customer name
  address: string
  custID: string
  crews: string[] // List of crew ids
  notes: string
}


@Component({
  selector: 'add-job-yearly',
  templateUrl: './add-job-yearly.component.html',
  styleUrls: ['./add-job-yearly.component.scss']
})
export class AddJobYearlyComponent {

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
  days: string[]

  every: boolean
  onEvery: boolean

  constructor(public service: AuthService, public activeModal: NgbActiveModal) {
    this.custID = ""
    this.address = ""
    this.custName = ""
    this.notes = ""
    this.mainFormIsValid = false
    this.crewIDs = []

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

  createYearlyJob(name: string, address: string, notes: string, month: string, day: number) {


    let d: YearlyJob = {
      isSeasonal: true,
      seasonalType: "yearly",
      month: this.months.indexOf(month),
      day: day,
      name: name,
      address: address,
      notes: notes,
      crews: this.crewIDs,
      custID: this.custID,
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

}
