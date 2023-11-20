import { Component, OnInit } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { WorkImagesModalComponent } from '../work-images-modal/work-images-modal.component';
import { AuthService } from 'src/app/services/auth.service';
import { ActivatedRoute, Router } from '@angular/router';
import * as io from "socket.io-client";
import { environment } from 'src/environments/environment';


interface Image {
  data: string
  timestamp: number
}

interface Comment {
  text: string
  email: string
  userJWT: string
  timestamp: number
}

interface Member {
  email: string
  jwt: string
}

interface Job {
  jobID: string
  name: string
  address: string
  notes: string
  comments: Comment[]
  started: boolean
  completed: boolean
  completeTimestamp: number
  startTimestamp: number
  members: Member[]
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


  constructor(public modal: NgbModal, public router: Router, public ar: ActivatedRoute, public service: AuthService) {

    this.beforePhotos = []
    this.afterPhotos = []
    this.comment = ""
    this.socket = null

    this.job = {
      name: "",
      jobID: "",
      address: "",
      notes: "",
      started: false,
      completed: false,
      comments: [],
      startTimestamp: 0,
      completeTimestamp: 0,
      members: []
    }

    let jobID = this.ar.snapshot.paramMap.get('jobID') as string

    this.service.getJob(jobID as string).subscribe(
      {
        next: (resp: any) => {
          this.job = resp
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
      email: "myemail",
      userJWT: this.service.token as string,
      timestamp: new Date().getTime()
    }
    this.job.comments.unshift(c)

    this.comment = ''
    this.service.postJobComment(this.job.jobID, c).subscribe(
      {
        next: (resp: any) => {
          // Empty
        }
      }
    )


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
        email: postComment.email,
        text: postComment.text,
        timestamp: postComment.timestamp,
        userJWT: "",
      }

      this.job.comments.unshift(c)

    })

  }

  delete() {

    let resp = confirm("Do you want to cancel this job?")
    if(!resp) {
      return
    }

    this.service.deleteJob(this.job.jobID).subscribe(
      {
        next: (resp: any) => {
          alert("Job canceled!")
          this.router.navigate(['/jobs'])
        }
      }
    )

  }

  save() {

    let d = {
      name: this.job.name,
      address: this.job.address,
      notes: this.job.notes,
    }

    this.service.editJob(this.job.jobID, d).subscribe(
      {
        next: (resp: any) => {
          alert("Job sucessfully updated!")
          window.location.reload()
        }
      }
    )
  }

}
