import { Component } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/services/auth.service';

interface Crew {
  crewID: string
  name: string
  selected: boolean
}

@Component({
  selector: 'app-add-job-modal',
  templateUrl: './add-job-modal.component.html',
  styleUrls: ['./add-job-modal.component.scss']
})
export class AddJobModalComponent {

  date: string

  crews: Crew[]

  constructor(public activeModal: NgbActiveModal, public service: AuthService) {
    this.date = ""

    this.crews = []

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

  createJob(name: string, date: string, address: string, notes: string) {

    let d = {
      name: name,
      address: address,
      notes: notes,
      dateTimestamp: new Date(date).getTime(),
      crews: this.crews,
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
