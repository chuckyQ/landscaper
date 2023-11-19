import { Component, Input } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';

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

  constructor(public service: AuthService) {
    this.custID = ""
    this.address = ""
    this.custName = ""
    this.notes = ""
    this.crewIDs = []
    this.mainFormIsValid = false
  }

}
