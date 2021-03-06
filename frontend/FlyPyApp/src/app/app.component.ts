import { Component } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { DataFetcherService } from './data-fetcher.service';
import { exPort } from './content_comps/home/home.component';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  constructor(private router: Router, 
    private route: ActivatedRoute,
    private dataFetcher: DataFetcherService
    ){}
  title = 'FlyPy';

  searchPort(searchString: string) {
    let reg: RegExp = RegExp('[0-9]')
    if(reg.test(searchString) && searchString.length > 4){
      const url = "/tracker?fnr=" + searchString;
      this.dataFetcher.requester(url, this.dataFetcher.trackerResponse)
    } else {
    this.dataFetcher.findPorts(searchString).subscribe((res: exPort) => {
      this.dataFetcher.activePos.emit(res)
    })
  }
  }
}
