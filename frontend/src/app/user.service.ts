import {Injectable} from '@angular/core'
import {HttpClient} from '@angular/common/http'

export type DisplayAndID = [string, number]

@Injectable({
  providedIn: 'root',
})
export class UserService {
  constructor(private http: HttpClient) {}

  save(user: Scrum.User) {
    return this.http.post<void>(`api/users/${user.id}`, user)
  }

  query(ids: number[]) {}

  currentlyLoggedIn() {
    return this.http.get<DisplayAndID[]>('api/current_users')
  }
}
