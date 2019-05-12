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
  image : string;
  pathToImage: string;
  constructor(private api: ApiService) { }

  ngOnInit() {
    this.getSwitches();
    this.anomalies = this.switches.length;
    //setInterval(this.getSwitches, 20000);
  }

  getSwitches = () => {
    this.api.getAllSwitches().subscribe(
      data => {
        this.switches = data.reverse();
        this.switches.forEach(function(e) {
          e.show = false;
          e.switch_id += 1;
          const hours = Math.round(( new Date().getTime() - new Date(e.timestamp).getTime()) / 1000 / 60 / 60);
          e.timestamp = hours + "hours ago.";
          console.log(e.timestamp);
        });
      },
      error => {
        console.log(error);
      }
    );



  }

  expand(event: Event, i: number) {
    if(this.switches[i].show == true) {
      this.switches[i].show = false;
    }else {
      this.switches[i].show = true;
    }

   this.pathToImage = this.switches[i].file_name;
  }
}
