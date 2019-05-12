import { Component, OnInit } from '@angular/core';
import {ApiService} from '../api.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  switches = [];
  anomalies = 5;
  constructor(private api: ApiService) { }

  ngOnInit() {
   this.getSwitches();
   this.anomalies = this.switches.length;
  }

  getSwitches = () => {
    this.api.getAllSwitches().subscribe(
      data => {
        this.switches = data;
      },
      error => {
        console.log(error);
      }
    );

  }

}
