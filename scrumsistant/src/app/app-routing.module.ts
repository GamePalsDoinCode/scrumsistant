import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {PointingComponent} from './pointing/pointing.component'
import {DashboardComponent} from './dashboard/dashboard.component'
import {StandupComponent} from './standup/standup.component'


const routes: Routes = [
  {path: '', redirectTo: 'dashboard', pathMatch: 'full'},
  {path: 'pointing', component: PointingComponent},
  {path: 'standup', component: StandupComponent},
  {path: 'dashboard', component: DashboardComponent},
  {path: '**', component: DashboardComponent},

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
