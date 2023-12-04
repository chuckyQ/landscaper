import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/services/auth.service';

interface Day {
  name: string
  selected: boolean
}

interface WeeklyJob {
  isRecurring: boolean // always true
  recurringType: string // always 'weekly'
  startDate: string // ISO date
  endDate: string // ISO date
  useEndDate: boolean
  recurrences: number
  custID: string
  crews: string[] // List of crew ids
  notes: string
  nWeeks: number

  sunday: boolean
  monday: boolean
  tuesday: boolean
  wednesday: boolean
  thursday: boolean
  friday: boolean
  saturday: boolean

}


@Component({
  selector: 'add-job-weekly',
  templateUrl: './add-job-weekly.component.html',
  styleUrls: ['./add-job-weekly.component.scss']
})
export class AddJobWeeklyComponent {

  @Input()
  custID: string

  @Input()
  notes: string

  @Input()
  mainFormIsValid: boolean | null

  @Input()
  crewIDs: string[]

  days: Day[]

  @Input()
  startDate: string
  endDate: string

  useEndDate: boolean
  useEndAfter: boolean

  recurringIsValid: boolean
  recurrences: number


  constructor(public service: AuthService, public activeModal: NgbActiveModal) {
    this.custID = ""
    this.notes = ""
    this.mainFormIsValid = false
    this.recurrences = 1

    this.useEndDate = true
    this.useEndAfter = false
    this.recurringIsValid = false

    this.startDate = ""
    this.endDate = ""

    this.crewIDs = []


    this.days = [
      { name: "Sunday", selected: false},
      { name: "Monday", selected: false},
      { name: "Tuesday", selected: false},
      { name: "Wednesday", selected: false},
      { name: "Thursday", selected: false},
      { name: "Friday", selected: false},
      { name: "Saturday", selected: false},
    ]

  }

  createWeeklyJob(nWeeks: number) {


    let d: WeeklyJob = {
      isRecurring: true,
      recurringType: "weekly",
      custID: this.custID,
      notes: this.notes,
      crews: this.crewIDs,
      startDate: this.startDate,
      endDate: this.endDate,
      nWeeks: nWeeks,
      useEndDate: !this.useEndAfter,
      recurrences: this.recurrences,
      sunday: this.days[0].selected,
      monday: this.days[1].selected,
      tuesday: this.days[2].selected,
      wednesday: this.days[3].selected,
      thursday: this.days[4].selected,
      friday: this.days[5].selected,
      saturday: this.days[6].selected,

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

  setValid(event: boolean) {
    this.recurringIsValid = event
  }

}
