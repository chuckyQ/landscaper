import { Component, OnInit } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { AddCrewModalComponent } from '../add-crew-modal/add-crew-modal.component';
import { AuthService } from 'src/app/services/auth.service';

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
  color: string
  useBlackText: boolean
}

@Component({
  selector: 'app-crews',
  templateUrl: './crews.component.html',
  styleUrls: ['./crews.component.scss']
})
export class CrewsComponent implements OnInit {

  crews: Crew[]

  constructor(public modal: NgbModal, public service: AuthService) {

    this.crews = []

    this.service.getCrews().subscribe(
      {
        next: (resp: any) => {
          this.crews = resp
        }
      }
    )

   }

  ngOnInit(): void {
  }

  addCrew() {
    this.modal.open(AddCrewModalComponent)
  }
}
