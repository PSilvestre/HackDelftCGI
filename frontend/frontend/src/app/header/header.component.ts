import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  constructor() {}

  ngOnInit() {
  }
}
export class DropdownElem {
  private _display: string;
  private _link: string;

  constructor(display: string, link: string){
    this._display = display;
    this._link = link;
  }


  get display(): string {
    return this._display;
  }

  set display(value: string) {
    this._display = value;
  }

  get link(): string {
    return this._link;
  }

  set link(value: string) {
    this._link = value;
  }
}
