import { Mail, Phone, Globe } from 'lucide-react'

export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-gray-900 text-gray-300 mt-auto">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* About */}
          <div>
            <h3 className="text-white font-bold text-lg mb-4">PLAGIATTRACKER</h3>
            <p className="text-sm text-gray-400 leading-relaxed">
              Détecteur de plagiat + contenu IA + correction automatique.
              Analysez vos documents académiques en toute confidentialité.
            </p>
          </div>

          {/* Contact */}
          <div>
            <h3 className="text-white font-bold text-lg mb-4">Contact & Support</h3>
            <div className="space-y-3">
              <a
                href="mailto:checkone076@gmail.com"
                className="flex items-center space-x-3 text-sm hover:text-primary-400 transition"
              >
                <Mail className="w-5 h-5" />
                <span>checkone076@gmail.com</span>
              </a>
              <a
                href="https://wa.me/237690895735"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center space-x-3 text-sm hover:text-primary-400 transition"
              >
                <Phone className="w-5 h-5" />
                <span>+237 690895735 (WhatsApp)</span>
              </a>
              <div className="flex items-center space-x-3 text-sm text-gray-400">
                <Globe className="w-5 h-5" />
                <span>Paiement: Mobile Money, Virement</span>
              </div>
            </div>
          </div>

          {/* Plans */}
          <div>
            <h3 className="text-white font-bold text-lg mb-4">Plans Tarifaires</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-400">Essai</span>
                <span className="text-primary-400 font-medium">0 FCFA</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Étudiant</span>
                <span className="text-primary-400 font-medium">2,500 FCFA</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Enseignant</span>
                <span className="text-primary-400 font-medium">5,000 FCFA</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Chercheur</span>
                <span className="text-primary-400 font-medium">10,000 FCFA</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Institution</span>
                <span className="text-secondary-400 font-medium">Sur devis</span>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-8 pt-6 border-t border-gray-800">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <p className="text-sm text-gray-500">
              © {currentYear} PLAGIATTRACKER. Tous droits réservés.
            </p>
            <div className="flex items-center space-x-6 text-sm">
              <a href="#" className="text-gray-400 hover:text-primary-400 transition">
                Confidentialité
              </a>
              <a href="#" className="text-gray-400 hover:text-primary-400 transition">
                Conditions
              </a>
              <a href="#" className="text-gray-400 hover:text-primary-400 transition">
                Documentation
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}
