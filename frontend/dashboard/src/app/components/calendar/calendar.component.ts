import { Component, OnInit } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { CalendarCreateJobModalComponent } from '../calendar-create-job-modal/calendar-create-job-modal.component';


function generateDates2() {

  // Get first day of month (day of week)
  let today = new Date()
  let startYear = today.getFullYear()
  let startMonth = today.getMonth()
  let monthStartDate = new Date(startYear, startMonth, 1)

  let dates: Date[] = []
  let monthStartDay = monthStartDate.getDay()
  // Add in the previous month's days to fill the first week
  let numOfPrevMonthDays = monthStartDay
  for(let i = numOfPrevMonthDays - 1; i > 0; i--) {
    let d = new Date(startYear, startMonth, numOfPrevMonthDays - i)
    dates.push(d)
  }

  let i = 0
  while(dates.length < 35) {
    dates.push(new Date(startYear, startMonth, 1 + i))
    i += 1
  }

  return dates

}


@Component({
  selector: 'calendar',
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.scss'],
})
export class CalendarComponent implements OnInit {

  weekdayNames: string[] = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

  jobMap: Map<string, string[]>
  jobIDs: Map<string, string>

  clickedJobID: string | null
  clickedDate: string | null

  destinationDate: string | null
  days: Date[]

  dragging: boolean

  constructor(public modal: NgbModal) {

    this.jobMap = new Map<string, string[]>;
    this.jobIDs = new Map<string, string>;

    this.clickedJobID = null
    this.clickedDate = null
    this.destinationDate = null

    this.jobIDs.set("a", "123456")
    this.jobIDs.set("b", "10203040")

    this.jobMap.set("2023-10-23", ["a", "b"])
    this.jobMap.set("2023-10-24", [])
    this.jobMap.set("2023-10-25", [])

    this.days = generateDates2()

    this.dragging = false
  }


  getJobList(dt: Date) {
    let d = dt.toISOString()
    let date = d.split("T")[0]

    if(this.jobMap.has(date)){
      return this.jobMap.get(date)
    }

    return []

  }

  swapJob(toDate: string, fromDate: string, jobID: string) {

    if(!this.dragging) {
      return
    }

    if(jobID === null) {
      return
    }

    // Add to the new date and check if it has an array already
    if(this.jobMap.has(toDate)) {
      let arr = this.jobMap.get(toDate)
      arr?.push(jobID)
      this.jobMap.set(toDate, arr as string[])
    } else {
      this.jobMap.set(toDate, [jobID])
    }

    // Remove from the previous date array
    let arr = this.jobMap.get(fromDate)
    arr!.splice(arr!.indexOf(jobID), 1)
    this.jobMap.set(fromDate, arr as string[])

  }

  ngOnInit(): void {
  }

  startDragging(event: any, dt: Date, jobID: string) {
    event.target.style.position = "absolute"
    this.clickedDate = event.target.getAttribute('date')
    this.clickedJobID = event.target.getAttribute("jobID")
  }

  changePosition(event: any, dt: Date) {
    event.target.style.position = "absolute"
  }

  dragDrop(event: any, dt: Date) {

    if(!this.dragging) {
      return
    }

    if(this.clickedDate === null) {
      return
    }

    let currDate = this.clickedDate
    this.swapJob(this.destinationDate as string, currDate, this.clickedJobID as string)

    this.clickedDate = null
    this.destinationDate = null
    this.clickedJobID = null
    this.dragging = false

  }

  startHover(event: any, dt: Date) {

    this.clickedDate = dt.toISOString().split("T")[0]
    this.clickedJobID = event.target.getAttribute("jobID")

  }

  stopHover(event: any, dt: Date) {
    this.clickedDate = null
    this.destinationDate = null
    this.dragging = false
  }

  getJobs(dt: Date) {
    let d = dt.toISOString().split('T')[0]

    if(this.jobMap.has(d)) {
      return this.jobMap.get(d)
    }

    return []

  }

  startEnter(event: any, dt: Date) {
  }

  showEvent(event: any, dt: Date) {
  }

  dropEvent(event: any, dt: Date) {


    this.dragging = false

    if(this.clickedDate === null) {
      return
    }

    let isoDate = this.clickedDate
    let arr = this.jobMap.get(isoDate)
    if(arr === undefined) {
      arr = []
    }
    // Remove the job from the current date
    arr?.splice(arr.indexOf(this.clickedJobID as string))
    this.jobMap.set(isoDate, arr as string[])

    // Place it in the new date
    let newDate = event.target.getAttribute("name") // date as string
    let arr2 = this.jobMap.get(newDate)
    if(arr2 === undefined || arr2 === null) {
      arr2 = []
    }

    arr2.push(this.clickedJobID as string)
    this.jobMap.set(newDate, arr2)
    this.clickedDate = null
    this.clickedJobID = null
    event.target.style.position = "inherit"
  }

  dragAway(event: any, dt: Date) {
    if(!this.dragging) {
      return
    }

    this.destinationDate = null

  }

  dragOver(event: any, dt: Date) {

    if(!this.dragging) {
      return
    }

    this.destinationDate = event.target.getAttribute("date")

  }

  hoverOver(event: any, dt: Date) {

    if(!this.dragging) {
      return
    }

    this.destinationDate = event.getAttribute("date")

  }

  openModal(dt: Date, jobs: string[] | undefined) {
    let m = this.modal.open(CalendarCreateJobModalComponent)
    m.componentInstance.dt = dt

    if(jobs === undefined) {
      jobs = []
    }

    m.componentInstance.jobs = jobs
  }



}
