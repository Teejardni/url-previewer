import type { PreviewResponse } from "../types"

interface Props {
  data: PreviewResponse | null
  loading: boolean
  error: string | null
}

export default function PreviewCard({ data, loading, error }: Props) {
  if (loading) return <div className="mt-6 text-center">Fetching preview…</div>
  if (error) return <div className="mt-6 text-center text-red-700">{error}</div>
  if (!data) return <div className="mt-6 text-center text-gray-500">No preview yet.</div>

  return (
    <div className="mt-6 max-w-2xl mx-auto border rounded-2xl overflow-hidden shadow-sm">
      {data.imageUrl && (
        <img src={data.imageUrl} alt={data.title ?? "Preview image"} className="w-full max-h-72 object-cover" />
      )}
      <div className="p-4">
        <div className="text-xs uppercase tracking-wide text-gray-500">{data.siteName ?? ""}</div>
        <h2 className="text-xl font-semibold mt-1">{data.title ?? "(no title)"}</h2>
        {data.description && <p className="mt-2 text-sm text-gray-700">{data.description}</p>}
      </div>
    </div>
  )
}