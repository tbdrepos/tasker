export interface ContactFormData {
  name: string
  email: string
  subject: string
  message: string
}

export type ContactFieldKey = keyof ContactFormData
export type ContactFieldErrors = Partial<Record<ContactFieldKey, string>>
