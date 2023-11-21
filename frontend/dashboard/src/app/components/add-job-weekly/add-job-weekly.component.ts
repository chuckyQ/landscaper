import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/services/auth.service';

interface Day {
  name: string
  selected: boolean
  index: number
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


@Component({
  selector: 'add-job-weekly',
  templateUrl: './add-job-weekly.component.html',
  styleUrls: ['./add-job-weekly.component.scss']
})
export class AddJobWeeklyComponent {

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

  days: Day[]
  months: string[]

  startMonth: number
  endMonth: number

  constructor(public service: AuthService, public activeModal: NgbActiveModal) {
    this.custID = ""
    this.address = ""
    this.custName = ""
    this.notes = ""
    this.mainFormIsValid = false

    this.startMonth = 3
    this.endMonth = 7

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

  createWeeklyJob(startMonth: number, endMonth: number) {

    let dayIndexes: number[] = []
    for(let i = 0; i < this.days.length; i++) {
      let day = this.days[i]
      if(day.selected) {
        dayIndexes.push(day.index)
      }
    }

    let d: WeeklyJob = {
      isSeasonal: true,
      seasonalType: "weekly",
      startMonth: startMonth,
      endMonth: endMonth,
      days: dayIndexes,
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

  get weekdayIsSelected() {
    for(let i = 0; i < this.days.length; i++) {
      if(this.days[i].selected) {
        return true
      }
    }

    return false
  }

  getWeekRange() {

    let values: number[] = []

    // Just give a max of 10 weeks for recurrence
    for(let i = 0; i < 10; i++) {
      values.push(i + 1)
    }


    return values

  }

}
