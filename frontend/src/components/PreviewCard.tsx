import type { PreviewResponse } from "../types"
import { useState } from "react"
import DOMPurify from "dompurify"
import "../App.css"

interface Props {
  data: PreviewResponse | null
  loading: boolean
  error: string | null
}

export default function PreviewCard({ data, loading, error }: Props) {
  const [showArticle, setShowArticle] = useState(false)

  if (loading) return <div className="pc-status pc-status--loading">Fetching preview…</div>
  if (error) return <div className="pc-status pc-status--error">{error}</div>
  if (!data) return <div className="pc-status pc-status--empty">No preview yet.</div>

  return (
    <div className="preview-card">
      {data.imageUrl && (
        <img
          src={data.imageUrl}
          alt={data.title ?? "Preview image"}
          className="preview-card__image"
        />
      )}

      <div className="preview-card__body">
        <div className="preview-card__site">{data.siteName ?? ""}</div>
        <h2 className="preview-card__title">{data.title ?? "(no title)"}</h2>
        {data.description && (
          <p className="preview-card__description">{data.description}</p>
        )}
      </div>

      {data.articleContent && (
        <div className="preview-card__article">
          <button
            type="button"
            onClick={() => setShowArticle(!showArticle)}
            className="preview-card__toggle"
            aria-expanded={showArticle}
          >
            {showArticle ? "Hide Full Article" : "Show Full Article"}
          </button>

          {showArticle && (
            <div
              className="preview-card__content prose-like"
              // content is sanitized before injection
              dangerouslySetInnerHTML={{
                __html: DOMPurify.sanitize(data.articleContent),
              }}
            />
          )}
        </div>
      )}
    </div>
  )
}