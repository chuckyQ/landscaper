import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditCrewMembersModalComponent } from './edit-crew-members-modal.component';

describe('EditCrewMembersModalComponent', () => {
  let component: EditCrewMembersModalComponent;
  let fixture: ComponentFixture<EditCrewMembersModalComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [EditCrewMembersModalComponent]
    });
    fixture = TestBed.createComponent(EditCrewMembersModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
