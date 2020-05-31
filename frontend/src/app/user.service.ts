import {Injectable} from '@angular/core'
import {HttpClient} from '@angular/common/http'

@Injectable({
  providedIn: 'root',
})
export class UserService {
  constructor(private http: HttpClient) {}

  save(user: Scrum.User) {
    return this.http.post<void>(`api/users/${user.id}`, user)
  }
}
