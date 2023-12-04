import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/services/auth.service';

interface DailyJob {
  isRecurring: boolean // always true
  recurringType: string // always 'daily'

  startDate: string // ISO date
  endDate: string // ISO date
  useEndDate: boolean
  recurrences: number
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
  custID: string

  @Input()
  notes: string

  @Input()
  mainFormIsValid: boolean | null

  @Input()
  startDate: string

  endDate: string

  useEndAfter: boolean

  recurrences: number

  @Input()
  crewIDs: string[]

  @Input()
  formIsValid: boolean

  recurringIsValid: boolean


  constructor(public service: AuthService, public activeModal: NgbActiveModal) {
    this.custID = ""
    this.mainFormIsValid = false
    this.notes = ""
    this.crewIDs = []
    this.startDate = ""
    this.endDate = ""
    this.useEndAfter = false
    this.recurrences = 1
    this.formIsValid = false
    this.recurringIsValid = false

  }

  createDailyJob() {

    let d: DailyJob = {
      isRecurring: true,
      recurringType: "daily",
      startDate: this.startDate.split("T")[0],
      endDate: this.endDate.split("T")[0],
      recurrences: this.recurrences,
      custID: this.custID,
      notes: this.notes,
      crews: this.crewIDs,
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

  setValid(event: boolean) {
    this.formIsValid = event
  }

}
