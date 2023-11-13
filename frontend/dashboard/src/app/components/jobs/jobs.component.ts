import { Component, OnInit } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/services/auth.service';

interface Job {
  jobID: string
  name: string
  address: string
  createdTimestamp: number
  lastUpdatedTimestamp: number
}

@Component({
  selector: 'app-jobs',
  templateUrl: './jobs.component.html',
  styleUrls: ['./jobs.component.scss']
})
export class JobsComponent implements OnInit {

  jobs: Job[]
  constructor(public modal: NgbModal, public service: AuthService) {

    this.jobs = []

    this.service.getJobs().subscribe(
      {
        next: (resp: any) => {
          console.log(resp)
          this.jobs = resp
        }
      }
    )

  }

  ngOnInit(): void {
  }


}
