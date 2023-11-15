import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/services/auth.service';

interface Crew {
  name: string
  selected: boolean
}

@Component({
  selector: 'app-time-table-modal',
  templateUrl: './time-table-modal.component.html',
  styleUrls: ['./time-table-modal.component.scss']
})
export class TimeTableModalComponent {

  @Input()
  date: string

  crews: Crew[]

  constructor(public activeModal: NgbActiveModal, public service: AuthService) {
    this.date = ""

    this.crews = [
      {
        name: "Gutters",
        selected: false,
      },
      {
        name: "Lawn Care",
        selected: false,
      }
    ]

  }

  createJob(name: string, address: string, notes: string) {

    let d = {
      name: name,
      address: address,
      notes: notes,
      dateTimestamp: new Date(this.date).getTime(),
      crews: [],

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
