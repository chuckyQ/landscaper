import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { TimeTableModalComponent } from 'src/app/time-table-modal/time-table-modal.component';

interface Timeslot {
  time: string
  hasEvent: boolean
  length: number // Number of rows to span
}

@Component({
  selector: 'app-calendar-day',
  templateUrl: './calendar-day.component.html',
  styleUrls: ['./calendar-day.component.scss']
})
export class CalendarDayComponent {

  timeslots: Timeslot[]
  timeArray: string[]
  dragStartSlot: number
  dragEndSlot: number
  year: number | null
  month: number | null
  day: number | null

  constructor(public modal: NgbModal, public ar: ActivatedRoute) {

    this.dragStartSlot = -1
    this.dragEndSlot = -1

    this.timeArray = [
        "00:00",
        "00:30",
        "01:00",
        "01:30",
        "02:00",
        "02:30",
        "03:00",
        "03:30",
        "04:00",
        "04:30",
        "05:00",
        "05:30",
        "06:00",
        "06:30",
        "07:00",
        "07:30",
        "08:00",
        "08:30",
        "09:00",
        "09:30",
        "10:00",
        "10:30",
        "11:00",
        "11:30",
        "12:00",
        "12:30",
        "13:00",
        "13:30",
        "14:00",
        "14:30",
        "15:00",
        "15:30",
        "16:00",
        "16:30",
        "17:00",
        "17:30",
        "18:00",
        "18:30",
        "19:00",
        "19:30",
        "20:00",
        "20:30",
        "21:00",
        "21:30",
        "22:00",
        "22:30",
        "23:00",
        "23:30",
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

    this.year = null
    this.month = null
    this.day = null

    let year = this.ar.snapshot.paramMap.get('year')
    let month = this.ar.snapshot.paramMap.get('month')
    let day = this.ar.snapshot.paramMap.get('day')

    if(year === null || month === null || day === null) {
      return
    }

    this.year = +year
    this.month = +month - 1 // Month is coming in 1-indexed and for dates to work, we need 0-indexed
    this.day = +day

  }

  createEvent(event: any, ts: Timeslot) {
    ts.hasEvent = !ts.hasEvent
    this.dragStartSlot = event.target.id
  }

  dragStart(event: any, ts: Timeslot) {
    this.dragStartSlot = this.timeArray.indexOf(event.target.id)
  }

  dragEnd(event: any) {
    this.dragEndSlot = this.timeArray.indexOf(event.target.id)
  }

  stretchEvent(event: any) {

  }

  scheduleTask(time: string, date: string) {

    let m = this.modal.open(TimeTableModalComponent)
    m.componentInstance.date = date
    m.componentInstance.time = time
  }


}

