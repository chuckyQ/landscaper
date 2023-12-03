import { Component, Input, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'recurring',
  templateUrl: './recurring.component.html',
  styleUrls: ['./recurring.component.scss']
})
export class RecurringComponent {


  @Input() startDate: string
  @Output() startDateChange = new EventEmitter<string>()

  @Input() endDate: string
  @Output() endDateChange = new EventEmitter<string>()

  @Input() endAfterRecurrence: boolean
  @Output() endAfterRecurrenceChange = new EventEmitter<boolean>()

  @Input() recurrences: number
  @Output() recurrencesChange = new EventEmitter<number>()

  useEndDate: boolean
  useEndAfter: boolean
  isValid: boolean

  @Output('valid')
  formIsValid = new EventEmitter<boolean>()

  constructor() {
    this.isValid = false
    this.useEndDate = true
    this.useEndAfter = false
    this.endAfterRecurrence = false
    this.recurrences = 1
    this.startDate = ""
    this.endDate = ""

  }

  valid() {

      let valid = (this.endDate < this.startDate) && this.useEndDate ||
                  (this.recurrences < 1 || this.recurrences === null) && this.useEndAfter

      this.formIsValid.emit(!valid)
      this.startDateChange.emit(this.startDate)
      this.endDateChange.emit(this.endDate)
      this.endAfterRecurrenceChange.emit(this.endAfterRecurrence)
      this.recurrencesChange.emit(this.recurrences)
  }

  toggle() {
    this.useEndAfter = !this.useEndAfter
    this.useEndDate = !this.useEndDate
  }

}
