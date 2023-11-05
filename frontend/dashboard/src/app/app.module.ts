import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

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
import { GroupComponent } from './components/group/group.component';
import { CalendarComponent } from './components/calendar/calendar.component';
import { AddCustomerModalComponent } from './components/add-customer-modal/add-customer-modal.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AddUserModalComponent } from './components/add-user-modal/add-user-modal.component';
import { AddCrewModalComponent } from './components/add-crew-modal/add-crew-modal.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CdkDrag, CdkDropList } from '@angular/cdk/drag-drop';
import { CreateJobModalComponent } from './components/create-job-modal/create-job-modal.component';
import { TimeTableModalComponent } from './time-table-modal/time-table-modal.component';
import { CalendarDayComponent } from './components/calendar-day/calendar-day.component';

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
    GroupComponent,
    CalendarComponent,
    AddCustomerModalComponent,
    AddUserModalComponent,
    AddCrewModalComponent,
    CreateJobModalComponent,
    TimeTableModalComponent,
    CalendarDayComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    BrowserAnimationsModule,
    CdkDropList,
    CdkDrag
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
