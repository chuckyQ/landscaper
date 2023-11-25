import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/services/auth.service';

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
  selector: 'add-job-single',
  templateUrl: './add-job-single.component.html',
  styleUrls: ['./add-job-single.component.scss']
})
export class AddJobSingleComponent {

  @Input()
  custName: string

  @Input()
  address: string

  @Input()
  custID: string

  @Input()
  notes: string

  @Input()
  crewIDs: string[]

  @Input()
  mainFormIsValid: boolean | null

  @Input()
  startDate: string

  constructor(public service: AuthService, public activeModal: NgbActiveModal) {
    this.custID = ""
    this.address = ""
    this.custName = ""
    this.notes = ""
    this.crewIDs = []
    this.mainFormIsValid = false
    this.startDate = ""
  }

  createJob() {

  }

}
