import { Component, OnInit } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';
import { TimeTableModalComponent } from '../time-table-modal/time-table-modal.component';
import { AddJobModalComponent } from '../add-job-modal/add-job-modal.component';


function generateDates2(startYear: number, startMonth: number) {

  let monthStartDate = new Date(startYear, startMonth, 1)

  let dates: Date[] = []
  let monthStartDay = monthStartDate.getDay()
  // Add in the previous month's days to fill the first week
  let numOfPrevMonthDays = monthStartDay
  for(let i = numOfPrevMonthDays - 1; i >= 0; i--) {
    let d = new Date(startYear, startMonth, - i)
    dates.push(d)
  }

  let i = 0
  while(dates.length < 35) {
    dates.push(new Date(startYear, startMonth, 1 + i))
    i += 1
  }

  return dates

}

interface Job {
  jobID: string
  address: string
  workDateTimestamp: number
}


@Component({
  selector: 'calendar',
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.scss'],
})
export class CalendarComponent implements OnInit {

  weekdayNames: string[] = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

  jobMap: Map<string, string[]> // Maps dates to a list of job ids
  jobIDs: Map<string, Job>

  clickedJobID: string | null
  clickedDate: string | null

  destinationDate: string | null
  days: Date[]
  displayedMonth: Date
  jobs: Job[]

  currentMonth: number
  currentYear: number
  dragging: boolean

  constructor(public modal: NgbModal, public router: Router, public service: AuthService) {

    this.jobMap = new Map<string, string[]>;
    this.jobIDs = new Map<string, Job>;
    this.jobs = []

    this.clickedJobID = null
    this.clickedDate = null
    this.destinationDate = null

    let today = new Date()
    this.currentMonth = today.getMonth()
    this.currentYear = today.getFullYear()
    this.displayedMonth = today

    this.days = generateDates2(today.getFullYear(), today.getMonth())
    this.dragging = false

    this.service.getJobBetweenTimestamps(this.days[0].getTime(), this.days[this.days.length-1].getTime())
    .subscribe(
      {
        next: (resp: any) => {
          this.jobs = resp as Job[]

          for(let i = 0; i < this.jobs.length; i++) {
            let job = this.jobs[i]
            let dt = new Date(job.workDateTimestamp)
            let date = dt.toISOString().split("T")[0]

            if(!this.jobMap.has(date)) {
              this.jobMap.set(date, [])
            }

            let list = this.jobMap.get(date)

            if(list === undefined) {
              list = []
            }

            list.push(job.jobID)
            this.jobMap.set(date, list)
            this.jobIDs.set(job.jobID, job)

          }

        }
      }
    )

  }


  ngOnInit(): void {

  }

  openJobModal(dt: string) {
    let m = this.modal.open(AddJobModalComponent)
    m.componentInstance.startDate = dt
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


  shiftBack() {
    this.currentMonth -= 1

    if(this.currentMonth === 0) {
      this.currentMonth = 11
      this.currentYear -= 1
    }

    this.days = generateDates2(this.currentYear, this.currentMonth)

    let d = this.days[15]
    this.currentYear = d.getFullYear()
    this.displayedMonth = d

  }

  shiftForward() {
    this.currentMonth += 1

    if(this.currentMonth > 11) {
      this.currentMonth = 1
      this.currentYear += 1
    }

    this.days = generateDates2(this.currentYear, this.currentMonth)
    let d = this.days[15]
    this.currentYear = d.getFullYear()
    this.displayedMonth = d
  }

  goToDay(dt: Date) {
    // Months are zero-based and we want to be one based
    let month = dt.getMonth() + 1
    this.router.navigate(['calendar', dt.getFullYear(), month, dt.getDate()])
  }

}
