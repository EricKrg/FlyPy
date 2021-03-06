import { Injectable, EventEmitter } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { LocatorService } from './locator.service';

@Injectable({
  providedIn: 'root'
})
export class DataFetcherService {
  removeEmitter: EventEmitter<boolean> = new EventEmitter<boolean>();

  allPorts: string = "/api/allairports";
  allPortsResponse: EventEmitter<any> = new EventEmitter<any>();

  allInResponse: EventEmitter<any> = new EventEmitter<any>();
  allOutResponse: EventEmitter<any> = new EventEmitter<any>();

  searchPort: String = "/api/airport/"

  connection : string = "/api/connect"
  connectionResponse: EventEmitter<any> = new EventEmitter<any>();
  
  longestCon: EventEmitter<any> = new EventEmitter<any>();
  shortestCon: EventEmitter<any> = new EventEmitter<any>();

  activePos: EventEmitter<any> = new EventEmitter<any>();
  hoverPos: EventEmitter<any> = new EventEmitter<any>();
  route: EventEmitter<any> = new EventEmitter<any>();
  trackerResponse: EventEmitter<any> = new EventEmitter<any>();
  trackPlanes:EventEmitter<any> = new EventEmitter<any>();

  constructor(private http: HttpClient, private locService: LocatorService) { }

  // airport search
  findPorts(searchTerm: string): Observable<any> {
    console.log(this.searchPort + searchTerm)
    return this.http.get(this.searchPort + searchTerm).pipe(
      map(res => res as JSON)
    )
  }
  // all airports
  allportEmitter(res:any) {
    this.allPortsResponse.emit(res)
  }
  fetchAllPorts(): Observable<any> {
    return this.http.get(this.allPorts).pipe(
      map(res => res as JSON)
    )
  }
  // connection
  getConnection(start: string, end:string, steps: string): Observable<any> {
    return this.http.get(this.connection + "?start="+start+"&end="+end+"&steps="+steps).pipe(
      map(res => res as JSON)
    )
  }

  getWorldTour(start:string): Observable<any> {
    return this.http.get("/api/aroundtheworld/"+ start).pipe(
      map(res => res as JSON)
    )
  }

  requester(url: string, emitter: EventEmitter<any>) {
    return this.http.get("/api/"+url).pipe(
      map(res => res as JSON)
    ).subscribe((res) => emitter.emit(res), error1 => alert("sorry something went wrong :(") )
  }


}
