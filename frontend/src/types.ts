export type PreviewResponse = {
    title: string | null
    description: string | null
    imageUrl: string | null
    siteName: string | null
    articleContent: string | null
  }
  
  export type ErrorResponse = { detail: string }