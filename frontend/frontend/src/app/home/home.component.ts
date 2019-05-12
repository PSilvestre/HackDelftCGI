import { Component, OnInit } from '@angular/core';
import {ApiService} from '../api.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  switches = [];
  anomalies: number;
  constructor(private api: ApiService) { }

  ngOnInit() {
   this.getSwitches();
  }

  getSwitches = () => {
    this.api.getAllSwitches().subscribe(
      data => {
        this.switches = data;
        this.anomalies = this.switches.length;
      },
      error => {
        console.log(error);
      }
    );

  }

}
