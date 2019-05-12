import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {HomeComponent} from './home/home.component';
import {AppComponent} from './app.component';
import {AboutmeComponent} from './aboutme/aboutme.component';

const routes: Routes = [{ path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'error', component: HomeComponent},
  { path: 'home', component: HomeComponent},
  { path: 'about', component: AboutmeComponent},

  { path: 'notifications', component: AppComponent}];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
