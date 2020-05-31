import {Component, OnInit} from '@angular/core'
import {UserService, DisplayAndID} from '../user.service'
import {AuthService} from '../auth.service'
import {concat} from 'rxjs'
@Component({
  selector: 'app-current-team',
  templateUrl: './current-team.component.html',
  styleUrls: ['./current-team.component.scss'],
})
export class CurrentTeamComponent implements OnInit {
  currentTeam: DisplayAndID[]
  currentUser: Scrum.User

  constructor(
    private userService: UserService,
    private authService: AuthService
  ) {}

  async ngOnInit() {
    this.currentTeam = await this.userService.currentlyLoggedIn().toPromise()
    console.log(this.currentTeam)
  }
}
