import {NgModule} from '@angular/core'
import {Routes, RouterModule} from '@angular/router'
import {PointingComponent} from './pointing/pointing.component'
import {DashboardComponent} from './dashboard/dashboard.component'
import {StandupComponent} from './standup/standup.component'
import {LoginPageComponent} from './login-page/login-page.component'
import {PmToolsComponent} from './pm-tools/pm-tools.component'
import {AuthService} from './auth.service'
import {PmCanActivateService} from './pm-can-activate.service'

const routes: Routes = [
  {path: '', redirectTo: 'app/dashboard', pathMatch: 'full'},
  {path: 'login', component: LoginPageComponent}, // TODO: canActivate: [NonAuthedGuard]

  {
    path: 'pm_tools',
    component: PmToolsComponent,
    canActivate: [PmCanActivateService],
  },

  {
    path: 'app',
    canActivate: [AuthService],
    children: [
      {path: 'pointing', component: PointingComponent},
      {path: 'standup', component: StandupComponent},
      {path: 'dashboard', component: DashboardComponent},
    ],
  },

  {
    path: '**',
    redirectTo: 'app/dashboard',
    pathMatch: 'full',
    canActivate: [AuthService],
  },
]

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
