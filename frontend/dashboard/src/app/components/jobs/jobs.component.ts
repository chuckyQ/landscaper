import { Component, OnInit } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { CreateJobModalComponent } from '../create-job-modal/create-job-modal.component';

@Component({
  selector: 'app-jobs',
  templateUrl: './jobs.component.html',
  styleUrls: ['./jobs.component.scss']
})
export class JobsComponent implements OnInit {

  constructor(public modal: NgbModal) {

  }

  ngOnInit(): void {
  }

  modalOpen() {
    this.modal.open(CreateJobModalComponent)
  }

}
