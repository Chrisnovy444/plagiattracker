import { ExternalLink } from 'lucide-react'

export default function SourceList({ sources }) {
  if (!sources || sources.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        Aucune source similaire trouvée
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {sources.map((source, index) => (
        <div
          key={index}
          className="card flex items-start justify-between hover:border-primary-300 transition"
        >
          <div className="flex-1">
            <div className="flex items-center space-x-2 mb-2">
              <span className="badge badge-warning text-xs">
                {source.similarity}% similarité
              </span>
              <span className="text-xs text-gray-500">{source.type}</span>
            </div>
            <h4 className="font-medium text-gray-900 mb-1">{source.source}</h4>
            {source.url && (
              <a
                href={source.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-primary-600 hover:text-primary-700 flex items-center space-x-1"
              >
                <span>Voir la source</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            )}
          </div>
          <div className="ml-4">
            <div className="w-16 h-16 rounded-lg bg-secondary-100 flex items-center justify-center">
              <span className="text-2xl font-bold text-secondary-600">
                {Math.round(source.similarity)}
              </span>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
