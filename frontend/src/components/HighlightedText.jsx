import { useState } from 'react'
import { ChevronDown, ChevronUp } from 'lucide-react'

export default function HighlightedText({ passages, type = 'plagiarism' }) {
  const [expanded, setExpanded] = useState(false)

  if (!passages || passages.length === 0) {
    return (
      <div className="text-sm text-gray-500 italic">
        Aucun passage suspect détecté
      </div>
    )
  }

  const displayedPassages = expanded ? passages : passages.slice(0, 5)

  const getColorClasses = (score, level) => {
    if (type === 'plagiarism') {
      if (level === 'exact' || score > 80) return 'bg-red-100 border-red-300 text-red-900'
      if (level === 'paraphrase' || score > 50) return 'bg-orange-100 border-orange-300 text-orange-900'
      return 'bg-yellow-100 border-yellow-300 text-yellow-900'
    } else {
      // AI detection
      if (level === 'high' || score > 70) return 'bg-purple-100 border-purple-300 text-purple-900'
      if (level === 'medium' || score > 40) return 'bg-blue-100 border-blue-300 text-blue-900'
      return 'bg-gray-100 border-gray-300 text-gray-900'
    }
  }

  const getLabel = (score, level) => {
    if (type === 'plagiarism') {
      if (level === 'exact') return '🔴 Copie exacte'
      if (level === 'paraphrase') return '🟠 Paraphrase'
      return '🟡 Similaire'
    } else {
      if (level === 'high') return '🟣 IA probable'
      if (level === 'medium') return '🔵 IA possible'
      return '⚪ IA faible'
    }
  }

  return (
    <div className="space-y-3">
      {displayedPassages.map((passage, index) => (
        <div
          key={index}
          className={`p-4 rounded-lg border-2 ${getColorClasses(passage.similarity || passage.ai_score, passage.type || passage.level)}`}
        >
          <div className="flex items-start justify-between mb-2">
            <span className="text-xs font-semibold">
              {getLabel(passage.similarity || passage.ai_score, passage.type || passage.level)}
            </span>
            <span className="text-xs font-mono">
              {Math.round(passage.similarity || passage.ai_score)}%
            </span>
          </div>

          <p className="text-sm leading-relaxed mb-2">
            "{passage.text || passage.sentence}"
          </p>

          {passage.source && (
            <div className="text-xs opacity-75">
              Source : {passage.source}
            </div>
          )}
        </div>
      ))}

      {passages.length > 5 && (
        <button
          onClick={() => setExpanded(!expanded)}
          className="w-full flex items-center justify-center space-x-2 py-2 text-sm text-primary-600 hover:text-primary-700 font-medium transition"
        >
          {expanded ? (
            <>
              <ChevronUp className="w-4 h-4" />
              <span>Voir moins</span>
            </>
          ) : (
            <>
              <ChevronDown className="w-4 h-4" />
              <span>Voir {passages.length - 5} passage(s) de plus</span>
            </>
          )}
        </button>
      )}
    </div>
  )
}
