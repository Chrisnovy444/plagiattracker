import { AlertCircle, CheckCircle, Lightbulb } from 'lucide-react'

export default function CorrectionPanel({ corrections }) {
  if (!corrections || corrections.total_corrections === 0) {
    return (
      <div className="card bg-primary-50 border-primary-200">
        <div className="flex items-center space-x-3">
          <CheckCircle className="w-6 h-6 text-primary-600" />
          <div>
            <h3 className="font-semibold text-gray-900">Aucune correction nécessaire</h3>
            <p className="text-sm text-gray-600">Votre document semble original !</p>
          </div>
        </div>
      </div>
    )
  }

  const allCorrections = [
    ...(corrections.plagiarism_corrections || []),
    ...(corrections.ai_corrections || [])
  ]

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-bold text-gray-900">
          Corrections suggérées ({corrections.total_corrections})
        </h3>
      </div>

      {allCorrections.map((correction, index) => (
        <div
          key={index}
          className={`card border-l-4 ${
            correction.severity === 'high'
              ? 'border-l-danger-500 bg-red-50'
              : correction.severity === 'medium'
              ? 'border-l-secondary-500 bg-orange-50'
              : 'border-l-primary-500 bg-green-50'
          }`}
        >
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0">
              {correction.severity === 'high' ? (
                <AlertCircle className="w-5 h-5 text-danger-500" />
              ) : (
                <Lightbulb className="w-5 h-5 text-secondary-500" />
              )}
            </div>
            <div className="flex-1">
              <div className="flex items-center space-x-2 mb-2">
                <span className={`badge ${
                  correction.severity === 'high' ? 'badge-danger' : 'badge-warning'
                }`}>
                  {correction.type}
                </span>
                <span className="text-xs text-gray-500 uppercase">
                  {correction.severity}
                </span>
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">
                {correction.suggestion}
              </h4>
              <p className="text-sm text-gray-700 whitespace-pre-line">
                {correction.details}
              </p>
              {correction.source && (
                <p className="text-sm text-gray-600 mt-2">
                  <strong>Source :</strong> {correction.source}
                </p>
              )}
            </div>
          </div>
        </div>
      ))}

      {/* Contact info */}
      <div className="card bg-primary-50 border-primary-200">
        <div className="flex items-start space-x-3">
          <Lightbulb className="w-5 h-5 text-primary-600 flex-shrink-0 mt-1" />
          <div>
            <h4 className="font-semibold text-gray-900 mb-1">
              Besoin d'aide avec les corrections ?
            </h4>
            <p className="text-sm text-gray-700 mb-2">
              {corrections.contact?.message}
            </p>
            <div className="flex flex-wrap gap-3 text-sm">
              <a
                href={`mailto:${corrections.contact?.email}`}
                className="text-primary-600 hover:text-primary-700 font-medium"
              >
                📧 {corrections.contact?.email}
              </a>
              <a
                href={`https://wa.me/${corrections.contact?.phone?.replace(/[^0-9]/g, '')}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary-600 hover:text-primary-700 font-medium"
              >
                📱 {corrections.contact?.phone}
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
