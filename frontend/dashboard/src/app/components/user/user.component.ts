import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';

interface User {
  email: string
  phoneNumber: string | null
}

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.scss']
})
export class UserComponent implements OnInit {

  user: User

  constructor(public service: AuthService, public ar: ActivatedRoute) {


    this.user = {
      email: "",
      phoneNumber: ""
    }

    let userID = this.ar.snapshot.paramMap.get('userID')

    if(userID !== null) {
      this.service.getUser(userID).subscribe(
        {
          next: (resp: any) => {
            this.user = resp
          }
        }
      )
    }

   }

  ngOnInit(): void {
  }

}
