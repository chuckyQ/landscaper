import { Component, OnInit } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { WorkImagesModalComponent } from '../work-images-modal/work-images-modal.component';

interface Image {
  data: string
  timestamp: number
}

@Component({
  selector: 'app-job',
  templateUrl: './job.component.html',
  styleUrls: ['./job.component.scss']
})
export class JobComponent implements OnInit {

  beforePhotos: Image[]
  afterPhotos: Image[]

  constructor(public modal: NgbModal) {

    this.beforePhotos = []
    this.afterPhotos = []

  }

  ngOnInit(): void {
  }

  openBeforePhotos(){
    let m = this.modal.open(WorkImagesModalComponent)
    m.componentInstance.photos = this.beforePhotos
    m.componentInstance.title = "Before Photos"
  }

  openAfterPhotos() {
    let m = this.modal.open(WorkImagesModalComponent)
    m.componentInstance.photos = this.afterPhotos
    m.componentInstance.title = "After Photos"
  }

}
