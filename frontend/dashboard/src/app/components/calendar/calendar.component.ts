import { Component, OnInit } from '@angular/core';
import {CdkDragDrop, CdkDropList, CdkDrag, moveItemInArray} from '@angular/cdk/drag-drop';

let DAY = 24 * 60 * 60 * 1000 // Milliseconds in a day

function generateDates2() {
  let today = new Date()
  let day = today

  // We take the current day and month and figure
  // out when the previous month starts.
  // The goal of this is to have 35 dates (5 weeks * 7 days each)
  // visible to the user.
  let days: Date[] = []
  days.push(today)
  while(day.getDate() !== 1) {
      let tmp = day.getTime()
      tmp -= DAY
      day = new Date(tmp)
      days.push(day)
  }

  let earliestDate = days[days.length - 1]
  if(earliestDate.getDay() !== 0) {
    // Backtrack until we reach a Sunday
    var tmp = earliestDate
    while (day.getDay() !== 0) {
      tmp = new Date(day.getTime() - DAY)
      days.push(tmp)
      day = tmp
    }

  }

  days.reverse()

  var i = 1
  let mostRecentDay = days[days.length - 1]
  while(days.length < 35) {
    let tmp = new Date(mostRecentDay.getTime() + DAY * i)
    i++
    days.push(tmp)
  }

  let weeks = []

  for(let i = 0; i < days.length; i += 7) {
    weeks.push(days.slice(i, i + 7))
  }
  return weeks
}


@Component({
  selector: 'calendar',
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.scss'],
})
export class CalendarComponent implements OnInit {

  movies = [
    'Episode I - The Phantom Menace',
    'Episode II - Attack of the Clones',
    'Episode III - Revenge of the Sith',
    'Episode IV - A New Hope',
    'Episode V - The Empire Strikes Back',
    'Episode VI - Return of the Jedi',
    'Episode VII - The Force Awakens',
    'Episode VIII - The Last Jedi',
    'Episode IX – The Rise of Skywalker',
  ];

  drop(event: any) {
    moveItemInArray(this.movies, event.previousIndex, event.currentIndex);
  }

  weeks: Date[][]
  weekdayNames: string[] = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

  jobMap: Map<string, string[]>

  constructor() {

    this.jobMap = new Map<string, string[]>;
    this.jobMap.set("Oct 23, 2023", ["a", "b", "c"])

    this.weeks = generateDates2()

   }

  ngOnInit(): void {
  }

}
