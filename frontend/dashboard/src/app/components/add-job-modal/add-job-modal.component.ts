import { Component } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/services/auth.service';

interface Crew {
  crewID: string
  name: string
  selected: boolean
}

interface Customer {
  name: string
  address: string
  custID: string
}

interface Day {
  name: string
  selected: boolean
  index: number
}

interface DailyJob {
  isSeasonal: boolean // always true
  seasonalType: string // always 'daily'
  startMonth: number // index of month (zero-based)
  endMonth: number // index of month (zero-based)
  name: string // Customer name
  address: string
  custID: string
  crews: string[] // List of crew ids
  notes: string
}

interface WeeklyJob {
  isSeasonal: boolean // always true
  seasonalType: string // always 'weekly'
  startMonth: number // index of month (zero-based)
  endMonth: number // index of month (zero-based)
  days: number[] // Indexes of selected days (0-Sunday, 1-Monday, etc...)
  name: string // Customer name
  address: string
  custID: string
  crews: string[] // List of crew ids
  notes: string
}

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

interface SingleJob {
  isSeasonal: boolean // always false
  seasonalType: string // always an empty string ''
  dateTimestamp: number // Unix timestamp
  name: string // Customer name
  address: string
  custID: string
  crews: string[] // List of crew ids
  notes: string
}

@Component({
  selector: 'app-add-job-modal',
  templateUrl: './add-job-modal.component.html',
  styleUrls: ['./add-job-modal.component.scss']
})
export class AddJobModalComponent {

  date: string
  months: string[]
  days: Day[]
  dayValues: number[]
  crews: Crew[]
  searchedCustomers: Customer[]
  custName: string
  custID: string
  custAddress: string
  showSearch: boolean
  seasonalType: string
  isSeasonal: boolean
  jobDate: string // Date of a single job (non-recurring)

  constructor(public activeModal: NgbActiveModal, public service: AuthService) {
    this.date = ""
    this.custID = ""
    this.custName = ""
    this.custAddress = ""
    this.showSearch = false
    this.seasonalType = ""
    this.isSeasonal = false
    this.jobDate = ""

    this.dayValues = []
    for(let i = 0; i < 28; i++) {
      this.dayValues.push(i + 1)
    }


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

    this.crews = []
    this.searchedCustomers = []

    this.service.getCrews().subscribe(
      {
        next: (resp: any) => {
          this.crews = resp

          for(let i = 0; i < this.crews.length; i++) {
            this.crews[i].selected = false
          }
        }
      }
    )

  }

  createYearlyJob(name: string, address: string, notes: string, month: string, day: number) {

    let crewIDs: string[] = []
    for(let i = 0; i < this.crews.length; i++) {
      let c = this.crews[i]
      if(c.selected) {
        crewIDs.push(c.crewID)
      }
    }

    let d: YearlyJob = {
      isSeasonal: this.isSeasonal,
      seasonalType: this.seasonalType,
      month: this.months.indexOf(month),
      day: day,
      name: name,
      address: address,
      notes: notes,
      crews: crewIDs,
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

  createMonthlyJob(name: string, address: string,
                   notes: string, startMonth: string,
                   endMonth: string, numOfWeeks: number,
                   day: string) {

    let crewIDs: string[] = []
    for(let i = 0; i < this.crews.length; i++) {
      let c = this.crews[i]
      if(c.selected) {
        crewIDs.push(c.crewID)
      }
    }

    let d: MonthlyJob = {
      isSeasonal: true,
      seasonalType: this.seasonalType,
      startMonth: this.months.indexOf(startMonth),
      endMonth: this.months.indexOf(endMonth),
      numOfWeeks: numOfWeeks,
      day: Object.keys(this.days).indexOf(day),
      name: name,
      address: address,
      custID: this.custID,
      notes: notes,
      crews: crewIDs,
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

  createWeeklyJob(name: string, address: string, notes: string,
                  startMonth: string, endMonth: string) {

    let crewIDs: string[] = []
    for(let i = 0; i < this.crews.length; i++) {
      let c = this.crews[i]
      if(c.selected) {
        crewIDs.push(c.crewID)
      }
    }

    let dayIndexes: number[] = []
    for(let i = 0; i < this.days.length; i++) {
      let day = this.days[i]
      if(day.selected) {
        dayIndexes.push(day.index)
      }
    }

    let d: WeeklyJob = {
      isSeasonal: true,
      seasonalType: this.seasonalType,
      startMonth: this.months.indexOf(startMonth),
      endMonth: this.months.indexOf(endMonth),
      days: dayIndexes,
      name: name,
      address: address,
      custID: this.custID,
      notes: notes,
      crews: crewIDs,
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

  createDailyJob(name: string, address: string, notes: string,
                 startMonth: string, endMonth: string) {


    let crewIDs: string[] = []
    for(let i = 0; i < this.crews.length; i++) {
      let c = this.crews[i]
      if(c.selected) {
        crewIDs.push(c.crewID)
      }
    }

    let d: DailyJob = {
      isSeasonal: true,
      seasonalType: this.seasonalType,
      startMonth: this.months.indexOf(startMonth),
      endMonth: this.months.indexOf(endMonth),
      name: name,
      address: address,
      custID: this.custID,
      notes: notes,
      crews: crewIDs,
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

  createJob(name: string, address: string, notes: string) {

    let crewIDs: string[] = []
    for(let i = 0; i < this.crews.length; i++) {
      let c = this.crews[i]
      if(c.selected) {
        crewIDs.push(c.crewID)
      }
    }

    let d: SingleJob = {
      isSeasonal: false,
      seasonalType: this.seasonalType,
      name: name,
      address: address,
      notes: notes,
      dateTimestamp: new Date(this.jobDate).getTime(),
      crews: crewIDs,
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

  searchCustomer(searchTerm: string) {
    this.service.searchCustomer(searchTerm).subscribe(
      {
        next: (resp: any) => {
          this.searchedCustomers = resp

          if(this.searchedCustomers.length > 0) {
            this.showSearch = true
          }

        }
      }
    )
  }

}
