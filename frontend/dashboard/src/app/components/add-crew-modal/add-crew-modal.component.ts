import { Component, OnInit } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-add-crew-modal',
  templateUrl: './add-crew-modal.component.html',
  styleUrls: ['./add-crew-modal.component.scss']
})
export class AddCrewModalComponent implements OnInit {

  constructor(public modal: NgbActiveModal) { }

  ngOnInit(): void {
  }

  closeModal() {
    this.modal.close()
  }

}
