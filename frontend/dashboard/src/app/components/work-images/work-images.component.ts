import { Component } from '@angular/core';

@Component({
  selector: 'app-work-images',
  templateUrl: './work-images.component.html',
  styleUrls: ['./work-images.component.scss']
})
export class WorkImagesComponent {

  constructor() {

    // Not showing vendor prefixes.
    navigator.mediaDevices.getUserMedia({video: {
      width: 500,
      height: 500,
      frameRate: 10,
    }
      , audio: true})
    .then(stream => {
      let vid = <HTMLVideoElement>document!.getElementById('video')
      vid!.srcObject = stream
    })

  }

  ngOnInit() {
  }

}
