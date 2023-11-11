import { Component, OnInit } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-add-customer-modal',
  templateUrl: './add-customer-modal.component.html',
  styleUrls: ['./add-customer-modal.component.scss']
})
export class AddCustomerModalComponent implements OnInit {

  constructor(public modal: NgbActiveModal, public service: AuthService) { }

  ngOnInit(): void {
  }

  closeModal() {
    this.modal.close()
  }

  addCustomer(name: string, address: string, phoneNumber: string) {

    let d = {
      name: name,
      address: address,
      phoneNumber: phoneNumber || "",
    }

    this.service.postCustomer(d).subscribe(
      {
        next: (resp: any) => {
          alert("Customer added!")
        }
      }
    )
  }

}
