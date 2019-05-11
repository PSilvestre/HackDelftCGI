import { Component } from '@angular/core';
import { ApiService} from './api.service';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: [ApiService]
})
export class AppComponent {
  switches = [];
	
  constructor(private api: ApiService) {
	  this.getSwitches();
  }
  
  getSwitches = () => {
	  this.api.getAllSwitches().subscribe(
	  	  data => {
			  this.switches = data;
				},
		  error => {
			  console.log(error);
		  }
	  )

  }
}
