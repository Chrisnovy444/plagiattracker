import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Upload, FileText, CheckCircle, AlertCircle, Loader } from 'lucide-react'
import { authAPI, uploadAPI, reportAPI } from '../utils/api'
import { useUserStore } from '../utils/store'

export default function Home() {
  const navigate = useNavigate()
  const { user, email, setUser } = useUserStore()

  const [file, setFile] = useState(null)
  const [loginEmail, setLoginEmail] = useState('')
  const [password, setPassword] = useState('')
  const [activationCode, setActivationCode] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [showLogin, setShowLogin] = useState(false)

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0]
    setFile(selectedFile)
    setError(null)
  }

  const handleLogin = async () => {
    setLoading(true)
    setError(null)

    try {
      // Try login first
      let response
      try {
        response = await authAPI.login(loginEmail, password)
      } catch (loginError) {
        // If login fails, register
        response = await authAPI.register(loginEmail, password, null)
      }

      setUser(response.data)
      setShowLogin(false)
      setError(null)
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur de connexion')
    } finally {
      setLoading(false)
    }
  }

  const handleActivateCode = async () => {
    if (!email || !activationCode) return

    setLoading(true)
    setError(null)

    try {
      const response = await authAPI.activateCode(email, activationCode)
      setUser(response.data)
      setActivationCode('')
    } catch (err) {
      setError(err.response?.data?.detail || 'Code invalide')
    } finally {
      setLoading(false)
    }
  }

  const handleUpload = async () => {
    if (!file) return

    if (!email) {
      setShowLogin(true)
      return
    }

    setLoading(true)
    setError(null)

    try {
      // Upload document
      const uploadResponse = await uploadAPI.uploadDocument(email, file)
      const documentId = uploadResponse.data.document_id

      // Start analysis
      await reportAPI.analyze(email, documentId)

      // Navigate to report (will poll for results)
      navigate(`/report/${documentId}`)
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur lors de l\'upload')
      setLoading(false)
    }
  }

  if (showLogin && !email) {
    return (
      <div className="max-w-md mx-auto">
        <div className="card">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Connexion</h2>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
              {error}
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
              <input
                type="email"
                value={loginEmail}
                onChange={(e) => setLoginEmail(e.target.value)}
                className="input"
                placeholder="votre@email.com"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Mot de passe</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input"
                placeholder="••••••••"
              />
            </div>

            <button
              onClick={handleLogin}
              disabled={loading || !loginEmail || !password}
              className="btn btn-primary w-full"
            >
              {loading ? <Loader className="w-5 h-5 animate-spin mx-auto" /> : 'Se connecter / S\'inscrire'}
            </button>

            <button
              onClick={() => setShowLogin(false)}
              className="btn btn-outline w-full"
            >
              Retour
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-12 animate-fadeIn">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          Détectez le plagiat et le contenu IA
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Analysez vos documents en toute confidentialité. Résultats en quelques minutes.
        </p>

        {/* User info */}
        {user && (
          <div className="card bg-primary-50 border-primary-200 mb-8">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Connecté : {email}</p>
                <p className="font-semibold text-primary-700">
                  {user.analyses_remaining} analyse(s) restante(s)
                </p>
              </div>
              <button onClick={() => setUser(null)} className="text-sm text-gray-600 hover:text-gray-900">
                Déconnexion
              </button>
            </div>
          </div>
        )}

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div className="card">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-3">
              <FileText className="w-6 h-6 text-primary-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Détection Plagiat</h3>
            <p className="text-sm text-gray-600">
              Comparaison avec 200M+ articles académiques et sources web
            </p>
          </div>

          <div className="card">
            <div className="w-12 h-12 bg-secondary-100 rounded-lg flex items-center justify-center mx-auto mb-3">
              <AlertCircle className="w-6 h-6 text-secondary-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Détection IA</h3>
            <p className="text-sm text-gray-600">
              Identifiez le contenu généré par ChatGPT, Claude, etc.
            </p>
          </div>

          <div className="card">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-3">
              <CheckCircle className="w-6 h-6 text-primary-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Correction Auto</h3>
            <p className="text-sm text-gray-600">
              Suggestions de citation et reformulation intelligente
            </p>
          </div>
        </div>
      </div>

      {/* Error display */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {typeof error === 'object' ? JSON.stringify(error) : error}
        </div>
      )}

      {/* Upload Section */}
      <div className="card mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Analysez votre document
        </h2>

        {/* Activation Code */}
        {user && (
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Code d'activation (optionnel)
            </label>
            <div className="flex space-x-2">
              <input
                type="text"
                placeholder="STU-XXXXX-XXXXX"
                value={activationCode}
                onChange={(e) => setActivationCode(e.target.value.toUpperCase())}
                className="input flex-1"
              />
              <button
                onClick={handleActivateCode}
                disabled={loading || !activationCode}
                className="btn btn-primary"
              >
                Activer
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-1">
              Pas de code ? WhatsApp : +237 690895735
            </p>
          </div>
        )}

        {/* File Upload */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Document à analyser
          </label>
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary-400 transition cursor-pointer">
            <input
              type="file"
              accept=".pdf,.docx,.txt"
              onChange={handleFileSelect}
              className="hidden"
              id="file-upload"
            />
            <label htmlFor="file-upload" className="cursor-pointer">
              <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              {file ? (
                <p className="text-sm text-gray-700 font-medium">{file.name}</p>
              ) : (
                <>
                  <p className="text-sm text-gray-600 mb-2">
                    Cliquez pour sélectionner ou glissez votre fichier
                  </p>
                  <p className="text-xs text-gray-500">
                    PDF, DOCX ou TXT (max 50 MB)
                  </p>
                </>
              )}
            </label>
          </div>
        </div>

        {/* Upload Button */}
        <button
          onClick={handleUpload}
          disabled={!file || loading}
          className="btn btn-primary w-full text-lg py-3"
        >
          {loading ? (
            <Loader className="w-5 h-5 animate-spin mx-auto" />
          ) : (
            'Analyser le document'
          )}
        </button>
      </div>

      {/* Pricing CTA */}
      <div className="card bg-gradient-to-br from-primary-50 to-secondary-50 border-primary-200">
        <h3 className="text-xl font-bold text-gray-900 mb-4">
          Besoin d'un abonnement ?
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="text-center">
            <p className="text-2xl font-bold text-primary-600">0 FCFA</p>
            <p className="text-sm text-gray-600">Essai (3 analyses)</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-primary-600">2,500</p>
            <p className="text-sm text-gray-600">Étudiant</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-primary-600">5,000</p>
            <p className="text-sm text-gray-600">Enseignant</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-primary-600">10,000</p>
            <p className="text-sm text-gray-600">Chercheur</p>
          </div>
        </div>
        <a
          href="https://wa.me/237690895735"
          target="_blank"
          rel="noopener noreferrer"
          className="btn btn-secondary w-full"
        >
          Acheter une licence sur WhatsApp
        </a>
      </div>
    </div>
  )
}
