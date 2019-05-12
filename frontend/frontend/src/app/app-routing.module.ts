import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {HomeComponent} from './home/home.component';
import {AppComponent} from './app.component';
import {AboutmeComponent} from './aboutme/aboutme.component';
import {NotificationsComponent} from './notifications/notifications.component';
import {ArrowComponent} from './arrow/arrow.component';

const routes: Routes = [{ path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'error', component: HomeComponent},
  { path: 'home', component: HomeComponent},
  { path: 'about', component: AboutmeComponent},
  { path: 'arrow', component: ArrowComponent},

  { path: 'notifications', component: NotificationsComponent}];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
