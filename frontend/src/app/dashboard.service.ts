import {Injectable} from '@angular/core'
import {HttpClient} from '@angular/common/http'
import {webSocket, WebSocketSubject} from 'rxjs/webSocket'

const BASE_URL = 'api/current_users'

@Injectable({
  providedIn: 'root',
})
export class DashboardService {
  constructor(private http: HttpClient) {}

  getCurrentUserNames() {
    return this.http.get<string[]>(BASE_URL)
  }

  userJoined(user: Scrum.User) {
    return this.http.post(BASE_URL, {
      displayName: user.displayName,
      pk: user.pk,
    })
  }
}
