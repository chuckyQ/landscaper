import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { CustomersComponent } from './components/customers/customers.component';
import { CustomerComponent } from './components/customer/customer.component';
import { JobComponent } from './components/job/job.component';
import { JobsComponent } from './components/jobs/jobs.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { TasksComponent } from './components/tasks/tasks.component';
import { TaskComponent } from './components/task/task.component';
import { UserComponent } from './components/user/user.component';
import { UsersComponent } from './components/users/users.component';
import { GroupsComponent } from './components/groups/groups.component';
import { GroupComponent } from './components/group/group.component';

const routes: Routes = [
  {path: "customers/:customerID", component: CustomerComponent},
  {path: "customers", component: CustomersComponent},
  {path: "groups", component: GroupsComponent},
  {path: "groups/:groupID", component: GroupComponent},
  {path: "", component: HomeComponent},
  {path: "jobs/:jobID", component: JobComponent},
  {path: "jobs", component: JobsComponent},
  {path: "login", component: LoginComponent},
  {path: "register", component: RegisterComponent},
  {path: "tasks/:taskID", component: TaskComponent},
  {path: "tasks", component: TasksComponent},
  {path: "users/:userID", component: UserComponent},
  {path: "users", component: UsersComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
