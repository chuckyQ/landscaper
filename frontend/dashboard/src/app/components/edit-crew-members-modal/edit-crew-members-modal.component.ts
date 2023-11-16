import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/services/auth.service';

interface CrewMember {
  email: string
  inCrew: boolean
}


@Component({
  selector: 'app-edit-crew-members-modal',
  templateUrl: './edit-crew-members-modal.component.html',
  styleUrls: ['./edit-crew-members-modal.component.scss']
})
export class EditCrewMembersModalComponent {

  crewID: string

  crewMembers: CrewMember[]

  constructor(public modal: NgbActiveModal, public service: AuthService) {
    this.crewID = ""
    this.crewMembers = []

  }

  ngOnInit() {
    this.service.getCrewMembers(this.crewID).subscribe(
      {
        next: (resp: any) => {
          this.crewMembers = resp
        }
      }
    )
  }

  saveMembers() {

    let crewMembers: CrewMember[] = []
    for(let i = 0; i < this.crewMembers.length; i++) {
      let c = this.crewMembers[i]
      if(c.inCrew) {
        crewMembers.push(c)
      }
    }

    this.service.postCrewMembers(this.crewID, crewMembers).subscribe(
      {
        next: (resp: any) => {
          this.modal.close()
          window.location.reload()
        }
      }
    )

  }

}
