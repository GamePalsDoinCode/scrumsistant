import {Component, OnInit, Input} from '@angular/core'
import {AuthService} from '../auth.service'
@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.scss'],
})
export class NavComponent implements OnInit {
  @Input() showSecondaryLinks = true
  constructor(private authService: AuthService) {}

  ngOnInit(): void {}

  isPM() {
    return this.authService.queryUser('is_PM')
  }
}
