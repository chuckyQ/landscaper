import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { CustomersComponent } from './components/customers/customers.component';
import { JobsComponent } from './components/jobs/jobs.component';
import { TasksComponent } from './components/tasks/tasks.component';
import { UsersComponent } from './components/users/users.component';
import { HomeComponent } from './components/home/home.component';
import { JobComponent } from './components/job/job.component';
import { TaskComponent } from './components/task/task.component';
import { UserComponent } from './components/user/user.component';
import { CustomerComponent } from './components/customer/customer.component';
import { GroupsComponent } from './components/groups/groups.component';
import { GroupComponent } from './components/group/group.component';
import { CalendarComponent } from './components/calendar/calendar.component';
import { AddCustomerModalComponent } from './components/add-customer-modal/add-customer-modal.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AddUserModalComponent } from './components/add-user-modal/add-user-modal.component';
import { AddGroupModalComponent } from './components/add-group-modal/add-group-modal.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CdkDrag, CdkDropList } from '@angular/cdk/drag-drop';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    CustomersComponent,
    JobsComponent,
    TasksComponent,
    UsersComponent,
    HomeComponent,
    JobComponent,
    TaskComponent,
    UserComponent,
    CustomerComponent,
    GroupsComponent,
    GroupComponent,
    CalendarComponent,
    AddCustomerModalComponent,
    AddUserModalComponent,
    AddGroupModalComponent
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
