import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { CustomersComponent } from './components/customers/customers.component';
import { JobsComponent } from './components/jobs/jobs.component';
import { TasksComponent } from './components/tasks/tasks.component';
import { CrewsComponent } from './components/crews/crews.component';
import { UsersComponent } from './components/users/users.component';
import { HomeComponent } from './components/home/home.component';
import { CrewComponent } from './components/crew/crew.component';
import { JobComponent } from './components/job/job.component';
import { TaskComponent } from './components/task/task.component';
import { UserComponent } from './components/user/user.component';
import { CustomerComponent } from './components/customer/customer.component';
import { GroupsComponent } from './components/groups/groups.component';
import { GroupComponent } from './components/group/group.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    CustomersComponent,
    JobsComponent,
    TasksComponent,
    CrewsComponent,
    UsersComponent,
    HomeComponent,
    CrewComponent,
    JobComponent,
    TaskComponent,
    UserComponent,
    CustomerComponent,
    GroupsComponent,
    GroupComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
