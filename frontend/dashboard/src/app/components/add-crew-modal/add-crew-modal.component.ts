import { Component, OnInit } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/services/auth.service';


interface Member {
  email: string
  imageJWT: string
  selected: boolean
}

interface Crew {
  name: string
  description: string
  color: string
  useBlackText: boolean
  members: Member[]
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

function useBlackText(rgb: string) {
  let rgbStr = rgb.substring(1) // Trim off the #
  let r = Number(`0x${rgbStr.substring(0, 2)}`)
  let g = Number(`0x${rgbStr.substring(2, 4)}`)
  let b = Number(`0x${rgbStr.substring(4, 6)}`)
  return useBlack(r, g, b)
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

  addCrew(name: string, description: string, color: string) {

    let useBlack = useBlackText(color)

    let d: Crew = {
      name: name,
      description: description,
      members: this.members,
      useBlackText: useBlack,
      color: color,
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
