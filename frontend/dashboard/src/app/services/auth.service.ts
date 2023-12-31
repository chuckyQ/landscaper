import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Router } from '@angular/router';
import { map } from 'rxjs';
import { JwtHelperService } from '@auth0/angular-jwt'
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  jwt: JwtHelperService;

  constructor(private http: HttpClient, private router: Router) {
    this.http = http;
    this.router = router
    this.jwt = new JwtHelperService()
  }

  navigateTo(url: string) {
    this.router.navigate([url])
  }

  refreshToken() {

    let headers = {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }

    this.http.get(`${environment.backendURL}/token`, {headers: headers}).subscribe(
      {
        next: (response: any) => {
          localStorage.setItem('access_token', response.access_token)
        }
      }
    )

  }


  get(url: string, params?: any, fullResp?: boolean) {

    this.refreshToken()

    let headers = {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }

    if(!params) {
      params = {};
    }

    let fullUrl = `${environment.backendURL}${url}`

    if(fullResp) {
      return this.http.get(fullUrl, {headers: headers, params: params, responseType: 'blob'})
    }

    return this.http.get(fullUrl, {headers: headers, params: params})
  }

  post(url: string, params?: any, refresh?: boolean) {

    // if(refresh !== null) {

    //   if(refresh) {
    //     this.refreshToken()
    //   }
    // }

    let headers = {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }

    if(!params) {
      params = {};
    }

    let fullUrl = `${environment.backendURL}${url}`

    return this.http.post(fullUrl, params, {headers: headers})
  }

  delete(url: string, param: any) {

    // this.refreshToken()

    let headers = {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }

    if(Object.keys(param).length > 0) {
      url = `${url}/${param}`
    }

    let fullUrl = `${environment.backendURL}${url}`

    return this.http.delete(fullUrl, {headers: headers})
  }

  login(username: string, password: string) {

    let data = {username: username, password: password}
    return this.post('/login', data)
            .pipe(map( (response: any) => {
              if (response && response.access_token) {
                localStorage.setItem('access_token', response.access_token)
                localStorage.setItem('isAccountOwner', response.isAccountOwner)
                return true
              }
              return false;
            }))
  }

  get currentUser() {
    let token = localStorage.getItem('access_token')

    if(!token) {
      return null;
    }

    return this.jwt.decodeToken(token)
  }

  logout() {
    localStorage.clear()
  }

  get token() {
    return localStorage.getItem('access_token')
  }

  isLoggedIn() {

    let token = localStorage.getItem('access_token')
    if(!token){
      return false;
    }

    let isExpired = this.jwt.isTokenExpired(token)
    return !isExpired
  }

  getCrews() {
    return this.http.get(`${environment.backendURL}/crews`)
  }

  postCrew(data: any) {
    return this.http.post(`${environment.backendURL}/crews`, data)
  }

  getCrew(crewID: string) {
    return this.http.get(`${environment.backendURL}/crews/${crewID}`)
  }

  editCrew(crewID: string, data: any) {
    return this.http.post(`${environment.backendURL}/crews/${crewID}`, data)
  }

  deleteCrew(crewID: string) {
    return this.http.delete(`${environment.backendURL}/crews/${crewID}`)
  }

  postCustomer(data: any) {
    return this.http.post(`${environment.backendURL}/customers`, data)
  }

  editCustomer(custID: string, data: any) {
    return this.http.post(`${environment.backendURL}/customers/${custID}`, data)
  }

  getCustomers() {
    return this.http.get(`${environment.backendURL}/customers`)
  }

  getCustomer(custID: string) {
    return this.http.get(`${environment.backendURL}/customers/${custID}`)
  }

  getJobsForCalendarDay(year: number, month: number, day: number) {
    return this.http.get(`${environment.backendURL}/calendar/${year}/${month}/${day}`)
  }

  getJob(jobID: string) {
    return this.http.get(`${environment.backendURL}/jobs/${jobID}`)
  }

  getJobBetweenDates(startDate: string, endDate: string) {
    return this.http.get(`${environment.backendURL}/jobs?startDate=${startDate}&endDate=${endDate}`)
  }

  getJobsOnDate(date: string) {
    return this.http.get(`${environment.backendURL}/jobs?date=${date}`)
  }

  getJobs() {
    return this.http.get(`${environment.backendURL}/jobs`)
  }

  postUser(data: any) {
    return this.http.post(`${environment.backendURL}/users`, data)
  }

  editUser(id: string, data: any) {
    return this.http.post(`${environment.backendURL}/users/${id}`, data)
  }

  postJob(data: any) {
    return this.http.post(`${environment.backendURL}/jobs`, data)
  }

  editJob(jobID: string, data: any) {
    return this.http.post(`${environment.backendURL}/jobs/${jobID}`, data)
  }

  deleteJob(id: string) {
    return this.http.delete(`${environment.backendURL}/jobs/${id}`)
  }

  postJobComment(jobID: string, data: any) {
    return this.http.post(`${environment.backendURL}/jobs/${jobID}/comments`, data)
  }

  getUsers() {
    return this.http.get(`${environment.backendURL}/users`)
  }

  getUser(userID: string) {
    return this.http.get(`${environment.backendURL}/users/${userID}`)
  }

  getCrewMembers(crewID: string) {
    return this.http.get(`${environment.backendURL}/crews/${crewID}/members`)
  }

  postCrewMembers(crewID: string, data: any) {
    return this.http.post(`${environment.backendURL}/crews/${crewID}/members`, data)
  }

  getMembers() {
    return this.http.get(`${environment.backendURL}/account/members`)
  }

  searchCustomer(searchTerm: string) {
    return this.http.get(`${environment.backendURL}/account/customers?searchTerm=${searchTerm}`)
  }
}

