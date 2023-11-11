import { Component, OnInit } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-add-user-modal',
  templateUrl: './add-user-modal.component.html',
  styleUrls: ['./add-user-modal.component.scss']
})
export class AddUserModalComponent implements OnInit {

  constructor(public modal: NgbActiveModal, public service: AuthService) { }

  ngOnInit(): void {
  }

  closeModal() {
    this.modal.close()
  }

  addUser(email: string, phoneNumber: string) {

    let d = {
      email: email,
      phoneNumber: phoneNumber,
    }
    this.service.postUser(d).subscribe(
      {
        next: (resp: any) => {
          alert("User added!")
          window.location.reload()
        }
      }
    )
  }

}
