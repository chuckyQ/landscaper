import { Component, OnInit } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';


interface Member {
  email: string
  imageJWT: string
}


@Component({
  selector: 'app-add-crew-modal',
  templateUrl: './add-crew-modal.component.html',
  styleUrls: ['./add-crew-modal.component.scss']
})
export class AddCrewModalComponent implements OnInit {

  members: Member[]

  constructor(public modal: NgbActiveModal) {

    this.members = []

  }

  ngOnInit(): void {
  }

  closeModal() {
    this.modal.close()
  }

}
