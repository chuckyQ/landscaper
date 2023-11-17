import { Pipe, PipeTransform } from "@angular/core";

@Pipe(
    {name: "timeago"}
)
export class TimeagoPipe implements PipeTransform {

    ONE_MINUTE = 60
    ONE_HOUR = 60 * this.ONE_MINUTE
    ONE_DAY = 24 * this.ONE_HOUR
    ONE_WEEK = 7 * this.ONE_DAY
    ONE_MONTH = 30 * this.ONE_DAY
    ONE_YEAR = 365 * this.ONE_DAY

    transform(seconds: number, ...args: any[]) {

        let now = Math.floor(Date.now() / 1000)

        seconds = now - seconds

        if(seconds < 6) {
            return `just now`
        }

        if(seconds < this.ONE_MINUTE) {
            return `${Math.floor(seconds)} seconds ago`
        }

        if(seconds < 2 * this.ONE_MINUTE) {
            return `1 minute ago`
        }

        if(seconds < this.ONE_HOUR) {
            return `${Math.floor(seconds / this.ONE_MINUTE)} minutes ago`
        }

        if(seconds < 2 * this.ONE_HOUR) {
            return `1 hour ago`
        }

        if(seconds < this.ONE_DAY) {
            return `${Math.floor(seconds / this.ONE_HOUR)} hours ago`
        }

        if(seconds < 2 * this.ONE_DAY) {
            return `1 day ago`
        }

        if(seconds < this.ONE_WEEK) {
            return `${Math.floor(seconds / this.ONE_DAY)} days ago`
        }

        if(seconds < 2 * this.ONE_WEEK) {
            return `1 week ago`
        }

        if(seconds < this.ONE_MONTH) {
            return `${Math.floor(seconds / this.ONE_WEEK)} weeks ago`
        }

        if(seconds < 2 * this.ONE_MONTH) {
            return `1 month ago`
        }

        if(seconds < this.ONE_YEAR) {
            return `${Math.floor(seconds / this.ONE_MONTH)} months ago`
        }

        if(seconds < 2 * this.ONE_YEAR) {
            return `1 year ago`
        }

        return `${Math.floor(seconds / this.ONE_YEAR)} years ago`
    }
}
