import { Component, OnInit } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { delay } from 'rxjs/operators';
import { DashboardService } from '../dashboard.service';
import { CookieService } from 'ngx-cookie-service';
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class DashboardComponent implements OnInit {
  socket: WebSocketSubject<any> | null = null;
  user: Scrum.User = {
    displayName: 'Punk',
    pk: null,
    email: '',
  };
  nameLocked = false;
  broadcastMsg = '';
  usernames: string[] = [];

  constructor(
    private dashboardService: DashboardService,
    private cookieService: CookieService
  ) {}

  ngOnInit(): void {
    this.socket = webSocket('ws://localhost:8000');
    this.socket.subscribe(
      (serverMsg) => this.handleIncoming(serverMsg),
      (err) => console.log(err),
      () => console.log('hey there! conn closed')
    );
    this.dashboardService.getCurrentUserNames().subscribe((usernames) => {
      console.log(usernames);
      console.log(usernames.filter((name) => name !== 'Uninitialized'));
      this.usernames = this.usernames.concat(
        usernames.filter((name) => name !== 'Uninitialized')
      );
      console.log(this.usernames);
    });
  }

  lockName(): void {
    this.nameLocked = true;
    this.dashboardService
      .userJoined(this.user)
      .subscribe((d) => console.log(d));
    // this.socket.next({
    //   type: 'userJoined',
    //   name: this.user.name,
    // })
    // this.socket.next({
    //   type: 'getUsernames',
    // })
  }

  handleIncoming(msg: any) {
    console.log(msg);
    if (msg.type === 'userJoined') {
      if (msg.name !== this.user.displayName) {
        this.broadcastMsg = `Say hello to ${msg.name}!`;
        console.log(this.broadcastMsg);
        this.usernames.push(msg.name);
      }
    } else if (msg.type === 'confirmJoined') {
      this.user.pk = msg.pk;
    } else if (msg.type === 'userLeft') {
      this.usernames = this.usernames.filter((name) => name !== msg.name);
    }
  }
}
