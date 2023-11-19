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

  getSelectedCrews() {

    let crewIDs: string[] = []
    for(let i = 0; i < this.crews.length; i++) {
      let c = this.crews[i]
      if(c.selected) {
        crewIDs.push(c.crewID)
      }
    }

    return crewIDs

  }

}
