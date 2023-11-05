import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WorkImagesComponent } from './work-images.component';

describe('WorkImagesComponent', () => {
  let component: WorkImagesComponent;
  let fixture: ComponentFixture<WorkImagesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WorkImagesComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(WorkImagesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
