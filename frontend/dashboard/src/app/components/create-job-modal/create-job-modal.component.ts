import { Component } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-create-job-modal',
  templateUrl: './create-job-modal.component.html',
  styleUrls: ['./create-job-modal.component.scss']
})
export class CreateJobModalComponent {

  constructor(public activeModal: NgbActiveModal) {

  }

}
