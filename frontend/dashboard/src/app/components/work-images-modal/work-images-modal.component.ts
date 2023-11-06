import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

interface Image {
  data: string
  timestamp: number
}

@Component({
  selector: 'app-work-images-modal',
  templateUrl: './work-images-modal.component.html',
  styleUrls: ['./work-images-modal.component.scss']
})
export class WorkImagesModalComponent {


  @Input()
  title: string

  @Input()
  photos: Image[]

  stream: MediaStream | null
  video: HTMLVideoElement | null

  images: Image[]

  constructor(public activeModal: NgbActiveModal) {

    this.stream = null
    this.video = null
    this.title = ""
    this.photos = []

    this.images = []

    navigator.mediaDevices.getUserMedia({video: {
      width: 10,
      height: 10,
      frameRate: 10,
    }, audio: false})
    .then(stream => {
      this.video = <HTMLVideoElement>document!.getElementById('video')
      this.video.srcObject = stream
      this.video.play()
      this.stream = stream
    })


  }

  takePicture() {

    let canvas = <HTMLCanvasElement>document.getElementById('canvas')

    const context = canvas.getContext("2d");
    context!.drawImage(this.video as CanvasImageSource, 0, 0, canvas.width, canvas.height);
    const data = canvas.toDataURL("image/png");

    let tstamp = new Date().getTime()
    let i: Image = {
      data: data,
      timestamp: tstamp / 1000 // Convert to seconds
    }

    this.photos.unshift(i)

  }

  ngOnInit() {
  }

  removeImage(i: number) {
    this.photos.splice(i, 1)
  }

  close() {
    this.activeModal.close()
    this.stream?.getTracks().forEach(function(track) {
      track.stop()
    })
  }

}
