import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { FileText, Download, ArrowLeft, Loader } from 'lucide-react'
import { reportAPI } from '../utils/api'
import { useUserStore, useReportStore } from '../utils/store'
import ScoreGauge from '../components/ScoreGauge'
import SourceList from '../components/SourceList'
import CorrectionPanel from '../components/CorrectionPanel'
import HighlightedText from '../components/HighlightedText'

export default function Report() {
  const { documentId } = useParams()
  const navigate = useNavigate()
  const { email } = useUserStore()
  const { currentReport, loading, setReport, setLoading } = useReportStore()
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!email) {
      navigate('/')
      return
    }

    loadReport()
  }, [documentId, email])

  const loadReport = async () => {
    setLoading(true)
    setError(null)

    try {
      const response = await reportAPI.getReport(email, documentId)
      setReport(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur lors du chargement du rapport')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="flex flex-col items-center justify-center py-20">
          <Loader className="w-12 h-12 text-primary-600 animate-spin mb-4" />
          <p className="text-gray-600">Chargement du rapport...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="card bg-red-50 border-red-200">
          <p className="text-red-700">{error}</p>
          <button onClick={() => navigate('/')} className="btn btn-primary mt-4">
            Retour à l'accueil
          </button>
        </div>
      </div>
    )
  }

  if (!currentReport) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="card">
          <p className="text-gray-600">Aucun rapport disponible</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto animate-fadeIn">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <button
          onClick={() => navigate('/')}
          className="flex items-center space-x-2 text-gray-600 hover:text-primary-600 transition"
        >
          <ArrowLeft className="w-5 h-5" />
          <span>Retour</span>
        </button>

        <button
          onClick={() => window.print()}
          className="btn btn-outline flex items-center space-x-2"
        >
          <Download className="w-4 h-4" />
          <span>Exporter PDF</span>
        </button>
      </div>

      {/* Document Info */}
      <div className="card mb-8">
        <div className="flex items-center space-x-3">
          <FileText className="w-8 h-8 text-primary-600" />
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{currentReport.filename}</h1>
            <p className="text-sm text-gray-600">
              {currentReport.word_count} mots • Analysé le {new Date(currentReport.created_at).toLocaleString('fr-FR')}
            </p>
          </div>
        </div>
      </div>

      {/* Scores */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="card">
          <ScoreGauge
            score={currentReport.plagiarism.score}
            label="Plagiat Détecté"
            type="plagiarism"
          />
          <p className="text-center text-sm text-gray-600 mt-4">
            {currentReport.plagiarism.sources.length} source(s) trouvée(s)
          </p>
        </div>

        <div className="card">
          <ScoreGauge
            score={currentReport.ai_detection.score}
            label="Contenu IA"
            type="ai"
          />
          <p className="text-center text-sm text-gray-600 mt-4">
            Perplexité: {currentReport.ai_detection.details.metrics.perplexity}
          </p>
        </div>
      </div>

      {/* Highlighted Plagiarism Passages */}
      {currentReport.plagiarism.highlighted_passages?.length > 0 && (
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">🔍 Passages Plagiés</h2>
          <div className="card">
            <HighlightedText
              passages={currentReport.plagiarism.highlighted_passages}
              type="plagiarism"
            />
          </div>
        </div>
      )}

      {/* Highlighted AI Passages */}
      {currentReport.ai_detection.highlighted_passages?.length > 0 && (
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">🤖 Passages IA Détectés</h2>
          <div className="card">
            <HighlightedText
              passages={currentReport.ai_detection.highlighted_passages}
              type="ai"
            />
          </div>
        </div>
      )}

      {/* Sources */}
      {currentReport.plagiarism.sources.length > 0 && (
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">📚 Sources Similaires</h2>
          <SourceList sources={currentReport.plagiarism.sources} />
        </div>
      )}

      {/* Corrections */}
      <div>
        <CorrectionPanel corrections={currentReport.corrections} />
      </div>
    </div>
  )
}
