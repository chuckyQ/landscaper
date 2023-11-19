import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/services/auth.service';

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

@Component({
  selector: 'add-job-daily',
  templateUrl: './add-job-daily.component.html',
  styleUrls: ['./add-job-daily.component.scss']
})
export class AddJobDailyComponent {

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

  constructor(public service: AuthService, public activeModal: NgbActiveModal) {
    this.custID = ""
    this.address = ""
    this.custName = ""
    this.mainFormIsValid = false
    this.notes = ""
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
  }

  createDailyJob(name: string, address: string, notes: string,
    startMonth: string, endMonth: string) {

    let d: DailyJob = {
      isSeasonal: true,
      seasonalType: "daily",
      startMonth: this.months.indexOf(startMonth),
      endMonth: this.months.indexOf(endMonth),
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
