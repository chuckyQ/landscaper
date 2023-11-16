import { Component, OnInit } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/services/auth.service';


interface Member {
  email: string
  imageJWT: string
  selected: boolean
}


@Component({
  selector: 'app-add-crew-modal',
  templateUrl: './add-crew-modal.component.html',
  styleUrls: ['./add-crew-modal.component.scss']
})
export class AddCrewModalComponent implements OnInit {

  members: Member[]

  constructor(public modal: NgbActiveModal, public service: AuthService) {

    this.members = []

    this.service.getMembers().subscribe(
      {
        next: (resp: any) => {
          this.members = resp
          for(let i = 0; i < this.members.length; i++) {
            this.members[i].selected = false
          }
        }
      }
    )


  }

  ngOnInit(): void {
  }

  closeModal() {
    this.modal.close()
  }

  addCrew(name: string, description: string) {

    let d = {
      name: name,
      description: description,
      members: this.members,
    }

    this.service.postCrew(d).subscribe(
      {
        next: (resp: any) => {
          alert("Crew created!")
          window.location.reload()
        }
      }
    )
  }

}
