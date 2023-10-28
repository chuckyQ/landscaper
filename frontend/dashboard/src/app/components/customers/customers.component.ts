import { Component, OnInit } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { AddCustomerModalComponent } from '../add-customer-modal/add-customer-modal.component';


interface Customer {
  address: string
  city: string
  state: string
  zipCode: string
  phoneNumber: string
  contactName: string
}


function createCustomer(address: string, city: string, state: string,
  zipCode: string, phoneNumber: string, contactName: string) {
  let c: Customer = {
    address: address,
    city: city,
    state: state,
    zipCode: zipCode,
    phoneNumber: phoneNumber,
    contactName: contactName,
  }

  return c
}


@Component({
  selector: 'app-customers',
  templateUrl: './customers.component.html',
  styleUrls: ['./customers.component.scss']
})
export class CustomersComponent implements OnInit {

  customers: Customer[]

  constructor(public modal: NgbModal) {

    this.customers = [
      createCustomer("22637 Madison St", "St Clair Shores", "MI", "48081", "313-319-4742", "Charles"),
      createCustomer("22637 Madison St", "St Clair Shores", "MI", "48081", "313-319-4742", "Charles"),
      createCustomer("22637 Madison St", "St Clair Shores", "MI", "48081", "313-319-4742", "Charles"),
      createCustomer("22637 Madison St", "St Clair Shores", "MI", "48081", "313-319-4742", "Charles"),
      createCustomer("22637 Madison St", "St Clair Shores", "MI", "48081", "313-319-4742", "Charles"),
      createCustomer("22637 Madison St", "St Clair Shores", "MI", "48081", "313-319-4742", "Charles"),
      createCustomer("22637 Madison St", "St Clair Shores", "MI", "48081", "313-319-4742", "Charles"),
      createCustomer("22637 Madison St", "St Clair Shores", "MI", "48081", "313-319-4742", "Charles"),
      createCustomer("22637 Madison St", "St Clair Shores", "MI", "48081", "313-319-4742", "Charles"),
      createCustomer("22637 Madison St", "St Clair Shores", "MI", "48081", "313-319-4742", "Charles"),
      createCustomer("22637 Madison St", "St Clair Shores", "MI", "48081", "313-319-4742", "Charles"),
      createCustomer("22637 Madison St", "St Clair Shores", "MI", "48081", "313-319-4742", "Charles"),
      createCustomer("22637 Madison St", "St Clair Shores", "MI", "48081", "313-319-4742", "Charles"),
      createCustomer("22637 Madison St", "St Clair Shores", "MI", "48081", "313-319-4742", "Charles"),
    ]

   }

  ngOnInit(): void {
  }

  createCustomer() {
    this.modal.open(AddCustomerModalComponent)
  }

}
