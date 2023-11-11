import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http'

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { CustomersComponent } from './components/customers/customers.component';
import { JobsComponent } from './components/jobs/jobs.component';
import { UsersComponent } from './components/users/users.component';
import { HomeComponent } from './components/home/home.component';
import { JobComponent } from './components/job/job.component';
import { UserComponent } from './components/user/user.component';
import { CustomerComponent } from './components/customer/customer.component';
import { CrewsComponent } from './components/crews/crews.component';
import { CrewComponent } from './components/crew/crew.component';
import { CalendarComponent } from './components/calendar/calendar.component';
import { AddCustomerModalComponent } from './components/add-customer-modal/add-customer-modal.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AddUserModalComponent } from './components/add-user-modal/add-user-modal.component';
import { AddCrewModalComponent } from './components/add-crew-modal/add-crew-modal.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { TimeTableModalComponent } from './components/time-table-modal/time-table-modal.component';
import { CalendarDayComponent } from './components/calendar-day/calendar-day.component';
import { WorkImagesModalComponent } from './components/work-images-modal/work-images-modal.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    CustomersComponent,
    JobsComponent,
    UsersComponent,
    HomeComponent,
    JobComponent,
    UserComponent,
    CustomerComponent,
    CrewsComponent,
    CrewComponent,
    CalendarComponent,
    AddCustomerModalComponent,
    AddUserModalComponent,
    AddCrewModalComponent,
    TimeTableModalComponent,
    CalendarDayComponent,
    WorkImagesModalComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
