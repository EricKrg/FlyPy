import { Component, OnInit, EventEmitter } from '@angular/core';
import {
  latLng, Leaflet, tileLayer, map, Map, locationfound, geoJSON, polygon, circle, Path, DomEvent, DomUtil, control, InteractiveLayerOptions,
  CRS, Layer, GeoJSON, layerGroup, FeatureGroup, LayerGroup, LeafletMouseEvent, popup, circleMarker, TileLayer, latLngBounds,
  LatLng, GeoJSONOptions, SVG
} from 'leaflet';

import 'leaflet-routing-machine';
import { LocatorService } from '../locator.service';
import { DataFetcherService } from '../data-fetcher.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Port, Connection, Plane } from '../content_comps/home/home.component';

declare var L: Leaflet;

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit {
  private map: Map;
  private pos: number[];
  private geojsonLayers: LayerGroup = layerGroup();
  private tracker: LayerGroup = layerGroup();
  private route;


  // base maps
  cartoDB_DarkMatter: TileLayer = tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
    subdomains: 'abcd',
    maxZoom: 19
  });
  cartoDB_Voyager: TileLayer = tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
    subdomains: 'abcd',
    maxZoom: 19
  });

  baseMaps: any = {
    'light': this.cartoDB_Voyager,
    'dark': this.cartoDB_DarkMatter,

  };

  overlayMaps: any = {
  };

  locateCircle(e): void {
    this.pos = e.latLng;
    let radius = e.accuracy / 2;
    circle(e.latlng, radius).addTo(this.map);
  }

  constructor(
    private datafetcher: DataFetcherService,
  ) { 
   
  }

  ngOnInit(): void {
    
    console.log("map init")
    // inital map creation
    this.map = this.map = map('map', {
      center: [52.5, 13.4],
      zoom: 14,
      renderer: new SVG({
        padding: 1
      }),
      layers: [this.cartoDB_Voyager, this.geojsonLayers, this.tracker]
    });
    control.layers(this.baseMaps).addTo(this.map);

    this.map.locate({ setView: true, maxZoom: 16 });

    this.map.on('locationfound', (e) => {
      let radius = e.accuracy / 2;
      circle(e.latlng, { color: 'red', fillOpacity: 0.5, radius: radius }).addTo(this.map);
    });

    this.datafetcher.removeEmitter.subscribe((res) => {
      console.log("remove")
      this.geojsonLayers.clearLayers()
      this.tracker.clearLayers()
    })

    this.datafetcher.activePos.subscribe((res: Port) => {
      this.geojsonLayers.clearLayers()
      this.map.setView([res.lat,res.lon], 12)
      let portCircle = circle([res.lat,res.lon],{
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5,
        radius: 500
    })
      portCircle.addTo(this.geojsonLayers)    
    })

    this.datafetcher.hoverPos.subscribe((res: Port) => {
      this.map.setView([res.lat,res.lon], 12)   
    })

    // all aiports
    this.datafetcher.allPortsResponse.subscribe((res) => {
      this.map.setView([0, 0], 2)   
      for (var key in res.all) {
        if(isNaN(res.all[key][0]) || isNaN(res.all[key][0])){
          console.log("jump")  
        } else {
          let portCircle = circle([res.all[key][0],res.all[key][1]], 200)
          portCircle.addTo(this.geojsonLayers) 
        } 
      }
      this.geojsonLayers.addTo(this.map)
    })

    // all outbound/ connection
    this.datafetcher.allOutResponse.subscribe((res) => {
      this.geojsonLayers.clearLayers() 
      this.tracker.clearLayers()     
      for(var key in res){
        let lat1 = parseFloat(res[key]["destinationAirport"]["lat"])
        let lon1 = parseFloat(res[key]["destinationAirport"]["lon"])

        let home = res[key]["sourceAirport"]
        let lat0 = parseFloat(home["lat"])
        let lon0 = parseFloat(home["lon"])

        if(isNaN(lat1) || isNaN(lon1) || isNaN(lat0) || isNaN(lon0)){
          console.log("no")
        } else {
          let portCircle = circle([lat0,lon0], 200)
          var polyline = L.polyline([[lat1,lon1],[lat0,lon0]], {color: 'rgb(220, 53, 69)'}).bindPopup("Outbound to: " + key)
          polyline.addTo(this.geojsonLayers);
          portCircle.addTo(this.geojsonLayers) 
        }
        this.geojsonLayers.addTo(this.map)
      }
    })
    //flightplan
    this.datafetcher.connectionResponse.subscribe((res:Connection[]) => {
      this.geojsonLayers.clearLayers() 
      this.tracker.clearLayers()     
      for (const con of res) {
        let lat1 = con.destinationAirport.lat
        let lon1 = con.destinationAirport.lon
        let lat0 = con.sourceAirport.lat
        let lon0 = con.sourceAirport.lon
        let portCircle = circle([lat0,lon0], { color: 'green'})
        var polyline = L.polyline([[lat1,lon1],[lat0,lon0]], {color: '#ffc107' }).bindPopup(con.sourceAirport.IATA + " to: " + con.destinationAirport.IATA)
        polyline.addTo(this.geojsonLayers);
        portCircle.addTo(this.geojsonLayers)
      }
      this.geojsonLayers.addTo(this.map)
    })

    //Flighttracker
    this.datafetcher.trackPlanes.subscribe((res:Plane[]) => {
      this.tracker.clearLayers()
      for(const p of res){
        let planeCircle = circle([p.lat,p.lon], { color: 'black',  radius: 500}).bindPopup("<b>" +p.flightNr + "</b> " + p.status + "<br>" + "Alt.: " + p.alt) 
        planeCircle.addTo(this.tracker)
      }
      this.tracker.addTo(this.map)
    })
  }
  
}
