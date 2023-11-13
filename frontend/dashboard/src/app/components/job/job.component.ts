import { Component, OnInit } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { WorkImagesModalComponent } from '../work-images-modal/work-images-modal.component';
import { AuthService } from 'src/app/services/auth.service';
import { ActivatedRoute } from '@angular/router';
import * as io from "socket.io-client";
import { environment } from 'src/environments/environment';


interface Image {
  data: string
  timestamp: number
}

interface Comment {
  text: string
  author: string
  userJWT: string
  timestamp: number
}

interface Job {
  address: string
  notes: string
  comments: Comment[]
  started: boolean
  completed: boolean
  completeTimestamp: number
  startTimestamp: number
}

@Component({
  selector: 'app-job',
  templateUrl: './job.component.html',
  styleUrls: ['./job.component.scss']
})
export class JobComponent implements OnInit {

  beforePhotos: Image[]
  afterPhotos: Image[]
  comment: string
  job: Job
  socket: io.Socket | null


  constructor(public modal: NgbModal, public ar: ActivatedRoute, public service: AuthService) {

    this.beforePhotos = []
    this.afterPhotos = []
    this.comment = ""
    this.socket = null

    this.job = {
      address: "",
      notes: "",
      started: false,
      completed: false,
      comments: [],
      startTimestamp: 0,
      completeTimestamp: 0,
    }

    let jobID = this.ar.snapshot.paramMap.get('jobID') as string

    this.service.getJob(jobID as string).subscribe(
      {
        next: (resp: any) => {
          // this.job = resp
        }
      }
    )

    this.connect(jobID)

  }

  ngOnInit(): void {
  }

  openBeforePhotos(){
    let m = this.modal.open(WorkImagesModalComponent)
    m.componentInstance.title = "Before Photos"
  }

  openAfterPhotos() {
    let m = this.modal.open(WorkImagesModalComponent)
    m.componentInstance.title = "After Photos"
  }

  postComment() {

    this.socket?.emit('postComment', {text: this.comment, userJWT: this.service.token})
    let c: Comment = {
      text: this.comment,
      author: this.service.currentUser,
      userJWT: this.service.token as string,
      timestamp: new Date().getTime()
    }
    this.job.comments.unshift(c)
    this.comment = "" // Clear out the comment after submitting
  }

  startJob() {

  }

  connect(jobID: string) {

    this.socket = io.connect(`${environment.websocketURL}`,  {extraHeaders: {'X-Access-Token' : this.service.token as string, 'X-Job-Id' : jobID }})

    this.socket.on('startJob', (startJob: any) => {
      this.job.started = true
    })

    this.socket.on('completeJob', (completeJob: any) => {
      this.job.completed = true
    })

    this.socket.on('emitComment', (postComment: any) => {
      let c: Comment = {
        author: "",
        text: postComment.text,
        timestamp: postComment.timestamp,
        userJWT: "",
      }

      this.job.comments.unshift(c)

    })

  }

}
