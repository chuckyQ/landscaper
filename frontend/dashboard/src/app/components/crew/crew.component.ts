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
  color: string
  useBlackText: boolean
}

/**
 *Good info about black/white text color:
* https://graphicdesign.stackexchange.com/questions/62368/automatically-select-a-foreground-color-based-on-a-background-color
*/
function useBlack(r: number, g: number, b: number) {
  let gamma = 2.2
  return (0.2126 * Math.pow(r / 255, gamma) +
          0.7152 * Math.pow(g / 255, gamma) +
          0.0722 * Math.pow(b / 255, gamma) ) > Math.pow(0.5, gamma)
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
      color: "#000000",
      useBlackText: false,
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
    let d: Crew = {
      name: this.crew.name,
      description: this.crew.description,
      members: [], // Members are edited separately
      color: this.crew.color,
      useBlackText: this.useBlackText(this.crew.color),
      crewID: this.crew.crewID,


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

  useBlackText(rgb: string) {
    let rgbStr = rgb.substring(1) // Trim off the #
    let r = Number(`0x${rgbStr.substring(0, 2)}`)
    let g = Number(`0x${rgbStr.substring(2, 4)}`)
    let b = Number(`0x${rgbStr.substring(4, 6)}`)
    return useBlack(r, g, b)
  }

}
