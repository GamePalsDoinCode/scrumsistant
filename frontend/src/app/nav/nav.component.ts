import {Component, Input} from '@angular/core'
import {AuthService} from '../auth.service'
@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.scss'],
})
export class NavComponent {
  @Input() showSecondaryLinks = true

  showTeamComponent = false
  toggleShowCurrentTeamInput = this.toggleShowCurrentTeam.bind(this)

  constructor(private authService: AuthService) {}

  isPM() {
    return this.authService.queryUser('is_PM')
  }

  toggleShowCurrentTeam() {
    this.showTeamComponent = !this.showTeamComponent
  }
}
