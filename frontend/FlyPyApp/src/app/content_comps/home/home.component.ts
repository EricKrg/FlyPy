import { Component, OnInit } from '@angular/core';
import { DataFetcherService } from 'src/app/data-fetcher.service';
import { LocationData } from 'src/app/shared/locationData';

export class Port {
  constructor(public name: String,
    public IATA: string, public lat: number, public lon: number) { };
}

export class exPort extends Port {
  constructor(
    public IATA: string, public ICAO: String,
    public airportID: String, altitude: String, public city: String,
    public continent: String, public country: String, dst: String, lat: number,
    lon: number, name: String, source: String, public timezone: String,
    type: String, public tz: String
  ) { super(name, IATA, lat, lon) }
}

export class Connection {
  constructor(
    public airline: string[], public destinationAirport: exPort, public direction: number,
    public distance: number, public equipment: string[], public sourceAirport: exPort
  ) { }
}

export class Plane {
  constructor(
    public status: string, public lat: number, public lon: number, public alt: number,
    public flightNr: string, public airline: string
  ) { }
}
export class TimeTable {
  constructor(
    public start_time: string, public end_time: string, public total_time: number, public wating_time: number
  ) { }
}


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})

export class HomeComponent implements OnInit {
  total: number = 0;
  ports: Port[];
  timetable: TimeTable;
  start: string = ''
  end: string = '';
  step: string = '';
  tempStart: string = '';
  tempEnd: string = '';
  compDist: number = 0;
  isLoading = false;
  connectionList: Connection[] = [];
  activePort: exPort;
  planeList: Plane[] = [];
  constructor(
    private dataFetcher: DataFetcherService
  ) { }

  ngOnInit() {
    this.dataFetcher.activePos.subscribe((res: exPort) => {
      console.log(res.name)
      this.reset()
      this.activePort = res;
      this.start = this.activePort.IATA
    })

    // longest route
    this.dataFetcher.longestCon.subscribe((res: Connection) => {
      let conList: Connection[] = [];
      this.compDist = this.compDist + res.distance
      this.dataFetcher.connectionResponse.emit(conList)
    })
    // shortest route
    this.dataFetcher.shortestCon.subscribe((res: Connection) => {
      let conList: Connection[] = [];
      conList.push(res)
      this.compDist = this.compDist + res.distance
      this.dataFetcher.connectionResponse.emit(conList)
    })

    // tracking 
    this.dataFetcher.trackerResponse.subscribe((res) => {
      let planeList: Plane[] = []
      this.planeList = []
      for (var p in res) {
        let ap: Plane = res[p]
        planeList.push(ap)
      }
      console.log(planeList)
      this.planeList = planeList
      if (this.planeList.length == 0) alert("No active Flights");
      else {
        this.dataFetcher.trackPlanes.emit(planeList)
      }
      
    })
  }

  allPortsClick() {
    console.log("All ports")
    this.ports = []
    this.dataFetcher.fetchAllPorts().subscribe((res) => {
      console.log(res);
      this.dataFetcher.allportEmitter(res)
      console.log("after emit")
      for (var key in res.all) {
        this.ports.push(new Port(key, res.all[key][2],
          res.all[key][0], res.all[key][1]))
      }
    })
  }
  remove() {
    this.dataFetcher.removeEmitter.emit(true)
    this.reset()
  }
  mouseOver(el: Port): void {
    console.log(el)
    if (isNaN(el.lat) || isNaN(el.lon)) {
      console.log("next")
    } else {
      this.dataFetcher.hoverPos.emit(el);
    }
  }
  reset(): void {
    this.connectionList = []
    this.ports = []
    this.planeList = []
    this.activePort = null;
  }

  allOut(iata: string) {
    this.connectionList = []
    let url = "/allcon/" + this.activePort.IATA + "?goingin=False"
    this.dataFetcher.requester(url, this.dataFetcher.allOutResponse)
  }
  getCon() {
    this.compDist = 0
    this.connectionList = []
    this.planeList = []
    this.isLoading = true;
    this.dataFetcher.getConnection(this.start, this.end, this.step).subscribe((res) => {
      for (var key in res) {
        if (key == 'time') {
          this.timetable = res[key]
        } else {
          let con: Connection = res[key]
          this.connectionList.push(con)
          this.compDist = this.compDist + con.distance
        }
      }
      this.dataFetcher.connectionResponse.emit(this.connectionList)
      this.isLoading = false;
    }, error1 => {
      alert("sorry something went wrong :(")
      this.isLoading = false;
    });
  }
  getWorldTour() {
    this.compDist = 0
    this.connectionList = []
    this.isLoading = true;
    this.dataFetcher.getWorldTour(this.start).subscribe((res) => {
      for (var key in res) {
        if (key == 'time') {
          this.timetable = res[key]
        } else {
          let con: Connection = res[key]
          this.connectionList.push(con)
          this.compDist = this.compDist + con.distance
        }
      }
      this.end = this.start
      this.dataFetcher.connectionResponse.emit(this.connectionList)
      this.isLoading = false;
    },error1 => {
      alert("sorry something went wrong :(")
      this.isLoading = false;
    });
  }
  longestClick() {
    this.compDist = 0
    this.connectionList = []
    this.dataFetcher.requester("/connect/longest/" + this.activePort.IATA, this.dataFetcher.longestCon)
  }
  shortestClick() {
    this.compDist = 0
    this.connectionList = []
    this.dataFetcher.requester("/connect/shortest/" + this.activePort.IATA, this.dataFetcher.shortestCon)
  }
  getTracking(start: string, end: string) {
    this.tempStart = start
    this.tempEnd = end
    console.log(start, end)
    const url = "/tracker?start=" + start + "&end=" + end;
    this.dataFetcher.requester(url, this.dataFetcher.trackerResponse)
  }
}
