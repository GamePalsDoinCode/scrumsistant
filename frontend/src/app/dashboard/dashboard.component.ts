import { Component, OnInit } from '@angular/core';
import {webSocket, WebSocketSubject} from 'rxjs/webSocket'
import {delay} from 'rxjs/operators'
import {DashboardService} from '../dashboard.service'

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  socket: WebSocketSubject<any> | null = null
  user: Scrum.User = {
    username: "Punk",
    pk: null,
  }
  nameLocked = false
  broadcastMsg = ''
  usernames: string[] = []

  constructor(private dashboardService: DashboardService) { }

  ngOnInit(): void {
    this.socket = webSocket('ws://localhost:8000')
    this.socket.subscribe(
      serverMsg => this.handleIncoming(serverMsg),
      err => console.log(err),
      () => console.log('hey there! conn closed'),
    )
    this.dashboardService.getCurrentUserNames().subscribe(
        d => console.log(d)
      )
  }

  lockName(): void{
    this.nameLocked = true
    this.dashboardService.userJoined(this.user).subscribe(
      d => console.log(d)
    )
    // this.socket.next({
    //   type: 'userJoined',
    //   name: this.user.name,
    // })
    // this.socket.next({
    //   type: 'getUsernames',
    // })
  }

  handleIncoming(msg: any){
    console.log(msg)
    if (msg.type == 'userJoined') {
      if (msg.name != this.user.username){
        this.broadcastMsg = `Say hello to ${msg.name}!`
        console.log(this.broadcastMsg)
        this.usernames.push(msg.name)
      }
    } else if (msg.type == 'confirmJoined'){
      this.user.pk = msg.pk

    }
  }

}
