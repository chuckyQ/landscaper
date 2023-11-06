import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

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
  selector: 'app-crew',
  templateUrl: './crew.component.html',
  styleUrls: ['./crew.component.scss']
})
export class GroupComponent implements OnInit {

  crewID: string
  constructor(public ar: ActivatedRoute) {

    this.crewID = this.ar.snapshot.paramMap.get("crewID") as string

  }

  ngOnInit(): void {
  }

}
