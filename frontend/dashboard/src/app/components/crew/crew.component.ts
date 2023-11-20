import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/services/auth.service';
import { EditCrewMembersModalComponent } from '../edit-crew-members-modal/edit-crew-members-modal.component';

interface Member {
  id: number
  userID: string
  username: string
  email: string
}

interface Crew {
  crewID: string
  name: string
  members: Member[]
  description: string
}

@Component({
  selector: 'app-crew',
  templateUrl: './crew.component.html',
  styleUrls: ['./crew.component.scss']
})
export class CrewComponent implements OnInit {

  crewID: string
  crew: Crew
  constructor(public ar: ActivatedRoute, public router: Router, public service: AuthService, public modal: NgbModal) {

    this.crewID = this.ar.snapshot.paramMap.get("crewID") as string
    this.crew = {
      name: "",
      description: "",
      members: [],
      crewID: "",
    }
    this.service.getCrew(this.crewID).subscribe(
      {
        next: (resp: any) => {
          this.crew = resp
        }
      }
    )

  }

  ngOnInit(): void {
  }

  editCrew() {
    let m = this.modal.open(EditCrewMembersModalComponent)
    m.componentInstance.crewID = this.crew.crewID
  }

  save() {
    let d = {
      name: this.crew.name,
      description: this.crew.description,
    }
    this.service.editCrew(this.crewID, d).subscribe(
      {
        next: (resp: any) => {
          alert("Crew saved!")
          window.location.reload()
        }
      }
    )
  }

  delete() {
    let resp = confirm("Are you sure you want to delete this crew?")

    if(!resp) {
      return
    }

    this.service.deleteCrew(this.crewID).subscribe(
      {
        next: (resp: any) => {
          alert("Crew deleted!")
          this.router.navigate(['/crews'])
        }
      }
    )

  }

}
