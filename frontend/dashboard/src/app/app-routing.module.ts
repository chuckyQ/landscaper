import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { CustomersComponent } from './components/customers/customers.component';
import { CustomerComponent } from './components/customer/customer.component';
import { JobComponent } from './components/job/job.component';
import { JobsComponent } from './components/jobs/jobs.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { UserComponent } from './components/user/user.component';
import { UsersComponent } from './components/users/users.component';
import { CrewsComponent } from './components/crews/crews.component';
import { GroupComponent } from './components/group/group.component';
import { CalendarComponent } from './components/calendar/calendar.component';
import { CalendarDayComponent } from './components/calendar-day/calendar-day.component';

const routes: Routes = [
  {path: "calendar", component: CalendarComponent},
  {path: "calendar/:year/:month/:day", component: CalendarDayComponent},
  {path: "customers/:customerID", component: CustomerComponent},
  {path: "customers", component: CustomersComponent},
  {path: "crews", component: CrewsComponent},
  {path: "crews/:groupID", component: GroupComponent},
  {path: "", component: HomeComponent},
  {path: "jobs/:jobID", component: JobComponent},
  {path: "jobs", component: JobsComponent},
  {path: "login", component: LoginComponent},
  {path: "register", component: RegisterComponent},
  {path: "users/:userID", component: UserComponent},
  {path: "users", component: UsersComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
