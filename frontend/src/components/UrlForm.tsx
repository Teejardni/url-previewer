import { useState } from "react"

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
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto flex gap-2">
      <input
        className="flex-1 border rounded-xl px-3 py-2 outline-none focus:ring-2"
        type="url"
        placeholder="https://example.com"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        required
      />
      <button
        type="submit"
        disabled={loading}
        className="px-4 py-2 rounded-xl border font-medium disabled:opacity-60"
      >
        {loading ? "Loading..." : "Fetch Preview"}
      </button>
      {error && <div className="text-red-600 text-sm ml-2 self-center">{error}</div>}
    </form>
  )
}