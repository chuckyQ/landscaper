import { Component } from '@angular/core';

interface Timeslot {
  time: string
  hasEvent: boolean
  length: number // Number of rows to span
}

@Component({
  selector: 'app-time-table',
  templateUrl: './time-table.component.html',
  styleUrls: ['./time-table.component.scss']
})
export class TimeTableComponent {

  timeslots: Timeslot[]
  timeArray: string[]
  dragStartSlot: number
  dragEndSlot: number

  constructor() {

    this.dragStartSlot = -1
    this.dragEndSlot = -1

    this.timeArray = [
        "12:00 AM",
        "12:30 AM",
        "01:00 AM",
        "01:30 AM",
        "02:00 AM",
        "02:30 AM",
        "03:00 AM",
        "03:30 AM",
        "04:00 AM",
        "04:30 AM",
        "05:00 AM",
        "05:30 AM",
        "06:00 AM",
        "06:30 AM",
        "07:00 AM",
        "07:30 AM",
        "08:00 AM",
        "08:30 AM",
        "09:00 AM",
        "09:30 AM",
        "10:00 AM",
        "10:30 AM",
        "11:00 AM",
        "11:30 AM",
        "12:00 PM",
        "12:30 PM",
        "01:00 PM",
        "01:30 PM",
        "02:00 PM",
        "02:30 PM",
        "03:00 PM",
        "03:30 PM",
        "04:00 PM",
        "04:30 PM",
        "05:00 PM",
        "05:30 PM",
        "06:00 PM",
        "06:30 PM",
        "07:00 PM",
        "07:30 PM",
        "08:00 PM",
        "08:30 PM",
        "09:00 PM",
        "09:30 PM",
        "10:00 PM",
        "10:30 PM",
        "11:00 PM",
        "11:30 PM",
    ]

    this.timeslots = []

    for(let i = 0; i < this.timeArray.length; i++) {
      this.timeslots.push(
        {
          time: this.timeArray[i],
          hasEvent: false,
          length: 2,
        }
      )
    }

  }

  createEvent(event: any, ts: Timeslot) {
    ts.hasEvent = !ts.hasEvent
    this.dragStartSlot = event.target.id
  }

  dragStart(event: any, ts: Timeslot) {
    console.log(event.target.id)
    this.dragStartSlot = this.timeArray.indexOf(event.target.id)
  }

  dragEnd(event: any) {
    this.dragEndSlot = this.timeArray.indexOf(event.target.id)


  }

  stretchEvent(event: any) {

  }

}
