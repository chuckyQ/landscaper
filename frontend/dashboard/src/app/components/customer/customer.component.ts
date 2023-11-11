import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';

interface Customer {
  custID: string
  name: string
  address: string
  phoneNumber: string | null
}


@Component({
  selector: 'app-customer',
  templateUrl: './customer.component.html',
  styleUrls: ['./customer.component.scss']
})
export class CustomerComponent implements OnInit {

  customer: Customer

  constructor(public service: AuthService, public ar: ActivatedRoute) {

    this.customer = {
      custID: "",
      name: "",
      address: "",
      phoneNumber: ""
    }

    let custID = this.ar.snapshot.paramMap.get('customerID')

    if(custID !== null) {
      this.service.getCustomer(custID).subscribe(
        {
          next: (resp: any) => {
            this.customer = resp
          }
        }
      )
    }

   }

  ngOnInit(): void {
  }

}
