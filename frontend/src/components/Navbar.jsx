import { Link } from 'react-router-dom'
import { FileSearch, Settings, Mail, Phone } from 'lucide-react'

export default function Navbar() {
  return (
    <nav className="bg-white border-b border-gray-200 shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center">
              <FileSearch className="w-6 h-6 text-white" />
            </div>
            <div className="flex flex-col">
              <span className="text-xl font-bold text-gray-900">PLAGIATTRACKER</span>
              <span className="text-xs text-gray-500">Détection Plagiat & IA</span>
            </div>
          </Link>

          {/* Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link to="/" className="text-gray-700 hover:text-primary-600 font-medium transition">
              Accueil
            </Link>
            <Link to="/settings" className="flex items-center space-x-2 text-gray-700 hover:text-primary-600 font-medium transition">
              <Settings className="w-4 h-4" />
              <span>Paramètres</span>
            </Link>

            {/* Contact Info */}
            <div className="flex items-center space-x-4 pl-4 border-l border-gray-300">
              <a
                href="mailto:checkone076@gmail.com"
                className="flex items-center space-x-1 text-sm text-gray-600 hover:text-primary-600 transition"
                title="Support email"
              >
                <Mail className="w-4 h-4" />
                <span className="hidden lg:inline">Support</span>
              </a>
              <a
                href="https://wa.me/237690895735"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center space-x-1 text-sm text-gray-600 hover:text-primary-600 transition"
                title="WhatsApp partenaire"
              >
                <Phone className="w-4 h-4" />
                <span className="hidden lg:inline">+237 690895735</span>
              </a>
            </div>
          </div>

          {/* Mobile Menu Button */}
          <button className="md:hidden p-2 rounded-lg hover:bg-gray-100">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>
    </nav>
  )
}
