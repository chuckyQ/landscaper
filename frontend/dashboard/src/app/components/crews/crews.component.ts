import { Component, OnInit } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { AddCrewModalComponent } from '../add-crew-modal/add-crew-modal.component';

interface Member {
  id: number
  userID: string
  username: string
  email: string
}

interface Crew {
  id: number
  groupID: string
  name: string
  members: Member[]
  description: string
}

@Component({
  selector: 'app-crews',
  templateUrl: './crews.component.html',
  styleUrls: ['./crews.component.scss']
})
export class CrewsComponent implements OnInit {

  groups: Crew[]

  constructor(public modal: NgbModal) {

    let g: Crew = {
      id: 1,
      groupID: "group_asdfjasdfadsf",
      name: "Tree Trimming",
      description: "Team for performing gutter cleanings",
      members: [
        {
          id: 1,
          userID: "user_fjfjaiwjfiwpfwf",
          username: "bob",
          email: "bob@bob.com",
        },
        {
          id: 1,
          userID: "user_fjfjaiwjfiwpfwf",
          username: "bob",
          email: "bob@bob.com",
        },
        {
          id: 1,
          userID: "user_fjfjaiwjfiwpfwf",
          username: "bob",
          email: "bob@bob.com",
        },
        {
          id: 1,
          userID: "user_fjfjaiwjfiwpfwf",
          username: "bob",
          email: "bob@bob.com",
        },
        {
          id: 1,
          userID: "user_fjfjaiwjfiwpfwf",
          username: "bob",
          email: "bob@bob.com",
        },
        {
          id: 1,
          userID: "user_fjfjaiwjfiwpfwf",
          username: "bob",
          email: "bob@bob.com",
        },
      ]
    }

    this.groups = [g, g, g, g, g, g, g]



   }

  ngOnInit(): void {
  }

  addCrew() {
    this.modal.open(AddCrewModalComponent)
  }
}
