import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {PointingComponent} from './pointing/pointing.component'
import {DashboardComponent} from './dashboard/dashboard.component'


const routes: Routes = [
  {path: '', redirectTo: 'dashboard', pathMatch: 'full'},
  {path: 'pointing', component: PointingComponent},
  {path: 'dashboard', component: DashboardComponent},

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
