import { Component, OnInit } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { AddUserModalComponent } from '../add-user-modal/add-user-modal.component';
import { AuthService } from 'src/app/services/auth.service';

interface User{
  userID: string
  email: string
  phoneNumber: string
}


@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss']
})
export class UsersComponent implements OnInit {

  users: User[]

  constructor(public modal: NgbModal, public service: AuthService) {

    this.users = []

    this.service.getUsers().subscribe(
      {
        next: (resp: any) => {
          this.users = resp
        }
      }
    )

   }

  ngOnInit(): void {
  }

  addUser() {
    this.modal.open(AddUserModalComponent)
  }

}
