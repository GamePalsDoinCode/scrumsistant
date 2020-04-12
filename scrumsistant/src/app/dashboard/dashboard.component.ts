import { Component, OnInit } from '@angular/core';
import {webSocket, WebSocketSubject} from 'rxjs/webSocket'
import {delay} from 'rxjs/operators'
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  socket: WebSocketSubject<any> | null = null
  user = {name: "Punk"}
  nameLocked = false
  broadcastMsg = ''

  constructor() { }

  ngOnInit(): void {
    this.socket = webSocket('ws://localhost:8000')
    this.socket.subscribe(
      serverMsg => this.handleIncoming(serverMsg),
      err => console.log(err),
      () => console.log('connection closed'),
     )
  }

  lockName(): void{
    this.nameLocked = true
    this.socket.next({type: 'userJoined', name: this.user.name})
  }

  handleIncoming(msg){
    console.log(msg)
    if (msg.type == 'userJoined') {
      if (msg.name != this.user.name){
        this.broadcastMsg = `Say hello to ${msg.name}!`
        console.log(this.broadcastMsg)
      }
    }
  }

}
