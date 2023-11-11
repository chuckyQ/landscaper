import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
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
}

@Component({
  selector: 'app-crew',
  templateUrl: './crew.component.html',
  styleUrls: ['./crew.component.scss']
})
export class CrewComponent implements OnInit {

  crewID: string
  crew: Crew
  constructor(public ar: ActivatedRoute, public service: AuthService) {

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

}
