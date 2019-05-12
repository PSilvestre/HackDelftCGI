import { Component, OnInit } from '@angular/core';
import {ApiService} from '../api.service';

@Component({
  selector: 'app-notifications',
  templateUrl: './notifications.component.html',
  styleUrls: ['./notifications.component.css']
})
export class NotificationsComponent implements OnInit {

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
