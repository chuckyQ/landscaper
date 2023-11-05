import { Component } from '@angular/core';

interface Image {
  data: string
  timestamp: number
}

@Component({
  selector: 'app-work-images',
  templateUrl: './work-images.component.html',
  styleUrls: ['./work-images.component.scss']
})
export class WorkImagesComponent {

  stream: MediaStream | null
  video: HTMLVideoElement | null

  images: Image[]

  constructor() {

    this.stream = null
    this.video = null

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

    this.images.unshift(i)

  }

  ngOnInit() {
  }

  removeImage(i: number) {
    console.log(i)
    this.images.splice(i, 1)
  }

}
