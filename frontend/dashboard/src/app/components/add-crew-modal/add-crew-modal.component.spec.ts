import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddGroupModalComponent } from './add-crew-modal.component';

describe('AddGroupModalComponent', () => {
  let component: AddGroupModalComponent;
  let fixture: ComponentFixture<AddGroupModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddGroupModalComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddGroupModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
