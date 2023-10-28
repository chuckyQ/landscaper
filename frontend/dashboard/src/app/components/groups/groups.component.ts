import { Component, OnInit } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { AddGroupModalComponent } from '../add-group-modal/add-group-modal.component';

@Component({
  selector: 'app-groups',
  templateUrl: './groups.component.html',
  styleUrls: ['./groups.component.scss']
})
export class GroupsComponent implements OnInit {

  constructor(public modal: NgbModal) { }

  ngOnInit(): void {
  }

  addGroup() {
    this.modal.open(AddGroupModalComponent)
  }
}
