import { Component, OnInit } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { AddCustomerModalComponent } from '../add-customer-modal/add-customer-modal.component';
import { AuthService } from 'src/app/services/auth.service';


interface Customer {
  custID: string
  address: string
  phoneNumber: string
  name: string
}


@Component({
  selector: 'app-customers',
  templateUrl: './customers.component.html',
  styleUrls: ['./customers.component.scss']
})
export class CustomersComponent implements OnInit {

  customers: Customer[]

  constructor(public modal: NgbModal, public service: AuthService) {

    this.customers = []

    this.service.getCustomers().subscribe(
      {
        next: (resp: any) => {
          this.customers = resp
        }
      }
    )


   }

  ngOnInit(): void {
  }

  createCustomer() {
    this.modal.open(AddCustomerModalComponent)
  }

}
