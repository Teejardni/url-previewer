import { useState } from "react"
import "../App.css"

interface Props {
  onSubmit: (url: string) => void
  loading?: boolean
}

export default function UrlForm({ onSubmit, loading }: Props) {
  const [url, setUrl] = useState("")
  const [error, setError] = useState<string | null>(null)

  function isValidUrl(input: string) {
    try {
      const u = new URL(input)
      return u.protocol === "http:" || u.protocol === "https:"
    } catch {
      return false
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!isValidUrl(url)) {
      setError("Please enter a valid http/https URL")
      return
    }
    setError(null)
    onSubmit(url)
  }

  return (
    <form onSubmit={handleSubmit} className="url-form" noValidate>
      <div className="url-form__field">
        <label htmlFor="url-input" className="url-form__label">
          URL
        </label>
        <input
          id="url-input"
          className="url-form__input"
          type="url"
          placeholder="https://example.com"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
          aria-invalid={!!error}
          aria-describedby={error ? "url-error" : undefined}
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="url-form__button"
      >
        {loading ? "Loading..." : "Fetch Preview"}
      </button>

      {error && (
        <div id="url-error" className="url-form__error" role="alert" aria-live="polite">
          {error}
        </div>
      )}
    </form>
  )
}
