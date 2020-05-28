declare namespace Scrum {
  interface User {
    displayName: string // TODO: change this to displayName
    pk: null | number
    email: string
    is_PM: boolean
    [index: string]: string | number | null | boolean
  }
}
