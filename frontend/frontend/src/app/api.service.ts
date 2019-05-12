import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
	
  baseurl = "http://127.0.0.1:8000";
  httpHeaders = new HttpHeaders({'Content-type': 'application/json'});

  constructor( private http: HttpClient) { }
  
  getAllSwitches(): Observable<any>{
	  return this.http.get(this.baseurl + '/switches/?format=json', {headers: this.httpHeaders});
  }
}
