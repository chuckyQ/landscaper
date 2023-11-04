import { Component, OnInit } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { AddGroupModalComponent } from '../add-group-modal/add-group-modal.component';

interface Member {
  id: number
  userID: string
  username: string
  email: string
}

interface Group {
  id: number
  groupID: string
  name: string
  members: Member[]
  description: string
}

@Component({
  selector: 'app-groups',
  templateUrl: './groups.component.html',
  styleUrls: ['./groups.component.scss']
})
export class GroupsComponent implements OnInit {

  groups: Group[]

  constructor(public modal: NgbModal) {

    let g: Group = {
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

  addGroup() {
    this.modal.open(AddGroupModalComponent)
  }
}
